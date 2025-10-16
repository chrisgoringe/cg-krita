import torch
import numpy as np
from PIL import Image
import os, time, random
from comfy.model_management import throw_exception_if_processing_interrupted
from comfy_api.latest import io
from typing import Any

PAD_TIME = 0.25

if os.path.exists( defaults_file:=os.path.join(os.path.dirname(__file__), "default.txt") ):
    with open(defaults_file, 'r') as fh: 
        DEFAULT_DIRECTORY = fh.readline().strip()
else:
    APPDATA = os.getenv('APPDATA') or ""
    DEFAULT_DIRECTORY = os.path.join(APPDATA,"krita","pykrita","wait_and_open")

if not os.path.exists(DEFAULT_DIRECTORY):
    print('''

\033[91m ***WARNING*** Edit with Krita - Default directory not located. \033[0m

This means one of three things:
          
- You haven't copied the required files into the Krita resource folder
- The Krita resource folder isn't in the default Windows location, and you haven't created the file default.txt
- You have created the file default.txt, and you've got the wrong file path 

\033[91m Check out the node installation instructions at https://github.com/chrisgoringe/cg-krita \033[0m
                    
          ''')
else: print(f"Edit in Krita using directory {DEFAULT_DIRECTORY}")

class EditWithKrita(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id  = "Edit with Krita",
            category = "krita",
            inputs   = [
                io.String.Input("directory", default=DEFAULT_DIRECTORY),
                io.Image.Input("images"),
                io.String.Input("active", default="if this is blank, don't run", tooltip="leave blank (or just whitespace) to disable"),
                io.Int.Input("timeout", default=300, min=10, max=100000),
            ],
            outputs = [
                io.Image.Output("edited"),
            ],
        )
    @classmethod
    def fingerprint_inputs(cls, **kwargs) -> Any:
        return random.random()
    
    @classmethod
    def execute(cls, directory:str, images:torch.Tensor, active:str, timeout:int) -> io.NodeOutput: # type: ignore
        if not active.strip(): return io.NodeOutput(images,)
        
        output_images:list[torch.Tensor] = [ cls.edit_image(i, directory, timeout) for i in images ]
        cls.cleanup_directory(directory)

        return io.NodeOutput(torch.cat(output_images),)
    
    @classmethod
    def edit_image(cls, image:torch.Tensor, directory:str, timeout:int) -> torch.Tensor:
        filepath = cls.save_image(image, directory)
        cls.wait_until_changed(filepath, timeout)
        image = cls.open_image(filepath)
        os.remove(filepath)
        return image  

    @classmethod
    def save_image(cls, image, directory):
        filepath = os.path.join(directory, f"__{random.randint(1000000,9999999)}.png")
        i = 255. * image.cpu().numpy()
        Image.fromarray(np.clip(i, 0, 255).astype(np.uint8)).save(filepath)
        return filepath   

    @classmethod
    def wait_until_changed(cls, filepath, timeout_at):
        time.sleep(PAD_TIME) # give the filesystem time to ensure the modification time is accurate 
        timeout_at = time.monotonic() + timeout_at
        mtime = os.path.getmtime(filepath)
        while time.monotonic() < timeout_at and mtime == os.path.getmtime(filepath): 
            throw_exception_if_processing_interrupted()
            time.sleep(1)
        time.sleep(PAD_TIME) # give the filesystem time to ensure krita has finished saving

    @classmethod
    def open_image(cls, filepath):
        img = Image.open(filepath).convert("RGB")
        image = np.array(img).astype(np.float32) / 255.0
        return torch.from_numpy(image)[None,]
    
    @classmethod
    def cleanup_directory(cls, directory):
        removable = lambda f: (f.startswith('__') and (f.endswith('.png') or f.endswith('png~')))
        for f in [ os.path.join(directory, f) for f in os.listdir(directory) if removable(f) ]:
            os.remove(f)
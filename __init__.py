from .edit_with_krita import EditWithKrita
from comfy_api.latest import ComfyExtension, io

async def comfy_entrypoint() -> ComfyExtension:
    class EditWithKritaExtension(ComfyExtension):
        async def get_node_list(self) -> list[type[io.ComfyNode]]:
            return [ EditWithKrita, ]
        
    return EditWithKritaExtension()

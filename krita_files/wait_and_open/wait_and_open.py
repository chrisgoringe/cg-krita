
import os, time

DIRECTORY = os.path.dirname(__file__)

CLOSE_ON_SAVE = True
SLEEP = 1

def log(s):
    with open(os.path.join(DIRECTORY,"log.txt"), 'a') as fh: print(s, file=fh, flush=True)
def clear_log():
    os.remove(os.path.join(DIRECTORY,"log.txt"))

try:
    from krita import Extension
    from PyQt5.QtCore import QObject, QThread, pyqtSignal
    import time
    from typing import Optional
except Exception as e:
    log(f"{e} in imports")

EXTENSION_ID = 'pykrita_wait_and_open'
MENU_ENTRY = 'Wait and Open'

class Worker(QObject):
    filepath_signal = pyqtSignal(str)
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.last = None
     
    def find_file(self) -> Optional[str]:
        l = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if os.path.splitext(f)[1]=='.png']
        l.sort()
        if not l: return None
        if l[0]==self.last: return None
        self.last = l[0]
        log(f"returning {os.path.split(self.last)[1]}")
        return self.last

    def run(self):
        try:
            while True:
                while not (f:=self.find_file()): time.sleep(SLEEP)
                self.filepath_signal.emit(f)
        except Exception as e:
            log(f"{e} in run")

class WaitAndOpen(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_opened:Optional[str] = None
        self.doc = None
        self.thread = None

    def setup(self):
        clear_log()

    def createActions(self, window):
        log('create actions')
        self.action_triggered()
        #action = window.createAction(EXTENSION_ID, MENU_ENTRY, "tools/scripts")
        #action.triggered.connect(self.action_triggered)

    def open_file(self, f:str):
        log(f"Opening {f}")
        time.sleep(SLEEP)
        self.doc = Krita.instance().openDocument(f)
        Krita.instance().activeWindow().addView(self.doc)
        Krita.instance().setActiveDocument(self.doc)
        self.file_opened = f
    
    def on_save(self, f:str):
        log(f"on_save {f}")
        if f==self.file_opened:
            log(f"closing {f}")
            self.doc.close()
            self.file_opened = None

    def action_triggered(self):
        if self.thread is not None: 
            log("Already started")
            return
        try:
            log("Starting Wait and Open")
            self.thread = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.filepath_signal.connect(self.open_file)
            self.thread.start()

            if CLOSE_ON_SAVE: Krita.instance().notifier().imageSaved.connect(self.on_save)
        except Exception as e:
            log(f"{e}")


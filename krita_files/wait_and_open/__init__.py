from .wait_and_open import WaitAndOpen

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
extension = WaitAndOpen(parent = app)
app.addExtension(extension)

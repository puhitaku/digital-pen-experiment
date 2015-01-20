import BasePlugin

class SerialParser(BasePlugin.ParserPlugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        self.debug('Successfully loaded', 'smile')

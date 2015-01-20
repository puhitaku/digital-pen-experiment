import BasePlugin

class SerialParser(BasePlugin.ParserPlugin):
    def __init__(self):
        super().__init__()

    def invoke(self):
        self.log.debug('Successfully loaded :)')

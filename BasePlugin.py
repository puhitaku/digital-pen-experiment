from yapsy.IPlugin import IPlugin
from Logger import Logger

class BasePlugin(Logger, IPlugin):
    def __init__(self):
        super().__init__()

class ParserPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

class DrawPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

class LogTest():
    def __init__(self):
        lg.getLogger(__name__).warning('Doh')
        print(__name__)
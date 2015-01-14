from yapsy.IPlugin import IPlugin
import logging as log_global

class BasePlugin(IPlugin):
    def __init__(self):
        super().__init__()
        self.log = log_global.getLogger(self.__class__.__name__)
        self.log.setLevel(log_global.DEBUG)

        log_handler = log_global.StreamHandler()
        log_handler.setLevel(log_global.DEBUG)

        log_formatter = log_global.Formatter(
            '%(levelname)s  %(asctime)s - %(name)s : %(message)s')
        log_handler.setFormatter(log_formatter)
        
        self.log.addHandler(log_handler)


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
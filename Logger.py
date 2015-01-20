import logging as log_global

class Logger:
    def __init__(self, name=''):
        if name == '':
            self.log = log_global.getLogger(self.__class__.__name__)
        else:
            self.log = log_global.getLogger(name)
            
        self.log.setLevel(log_global.DEBUG)

        log_handler = log_global.StreamHandler()
        log_handler.setLevel(log_global.DEBUG)

        log_formatter = log_global.Formatter(
            '%(levelname)s  %(asctime)s - %(name)s : %(message)s')
        log_handler.setFormatter(log_formatter)
        
        self.log.addHandler(log_handler)

    def get_logger_object(self):
        return self.log

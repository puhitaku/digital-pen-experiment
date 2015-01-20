import logging as log_global
from random import shuffle

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

    def debug(self, msg, f=''):
        self.log.debug(msg + self.fancy(f))

    def info(self, msg, f=''):
        self.log.info(msg + self.fancy(f))

    def warning(self, msg, f=''):
        self.log.warning(msg + self.fancy(f))

    def error(self, msg, f=''):
        self.log.warning(msg + self.fancy(f))

    def critical(self, msg, f=''):
        self.log.critical(msg + self.fancy(f))

    def fancy(self, f):
        if f == 'smile':
            return ' ' + self.smile()
        elif f == 'ouch':
            return ' ' + self.ouch()
        else:
            return ''

    def smile(self):
        e, m = [':', ';', '=', 'X'], [')', 'D', '3', '>', ']']
        shuffle(e)
        shuffle(m)
        return e[0] + m[0]

    def ouch(self):
        e, m = [':', 'X', ":'"], ['(', '<', '[', '/', 'O', 'P']
        shuffle(e)
        shuffle(m)
        return e[0] + m[0]
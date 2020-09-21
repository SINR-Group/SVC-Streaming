import logging

class logger(logging.Logger):
    def __init__(self, name):
        super(logger, self).__init__(name)  
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] p%(process)s <%(filename)s:%(lineno)d> %(name)s %(levelname)s - %(message)s','%m-%d %H:%M:%S')

        ch.setFormatter(formatter)
        self.addHandler(ch)

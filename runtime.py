class Runtime:

    def schedule_next(self, delay_ms, callback):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
    
    def add(self, strip, x, y):
        raise NotImplementedError()

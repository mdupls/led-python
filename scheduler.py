class Scheduler:
    def __init__(self, interval_ms, callback):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

class Timer:
    def __init__(self, delay_ms, callback):
        raise NotImplementedError

    def after(self):
        raise NotImplementedError

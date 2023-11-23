class State():
    def __init__(self):
        self.GO = False
        self.BRAKE = False
        self.K = .5 #brake sensitivity
        self.brakes = 0
        self.RIGHT= False
        self.LEFT = False
        self.REVERSE = False
        # self.keys = key.KeyStateHandler()
        # window.push_handlers(keys)
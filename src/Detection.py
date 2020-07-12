class Detection:
    def __init__(self, name, isExist, top_left, botton_right):
        self.exists = isExist
        self.name = name
        self.top_left = top_left
        self.botton_right = botton_right
    
    @property
    def Name(self):
        return self.name

    @property
    def IsExist(self):
        return self.exists
    
    @property
    def LocalPosition(self):
        return [ self.top_left, self.botton_right]
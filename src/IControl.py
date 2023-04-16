from abc import ABCMeta, abstractmethod

class IControl(metaclass=ABCMeta):
    def __init__(self, window):
        self.window = window

    @abstractmethod
    def Update(self, top, left, bottom, right):
        pass

    @abstractmethod
    def MouseLeftClick(self, top_left, bottom_right):
        pass
    
    @abstractmethod
    def SwipeUp(self, abovePosition, belowPosition, delay=0.05):        
        pass

    @abstractmethod
    def SwipeDown(self, abovePosition, belowPosition, delay=0.05):        
        pass

    @abstractmethod
    def OsoujiPathSlides(self, delay=0.05):
        center = [177, 356]
        osoujiPaths = [[198, 286], [267, 343], [265, 435], [246, 526], [166, 518], [86, 474], [75, 385], [126, 300]]
        pass
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
        pass

from .section import Section, Signal

class Timer(Section):
    """Emits on_timer events
    
    my_timer = Timer(interval_seconds=10, on_timer=my_callback)
    
    def my_callback(**kwargs):
        actual_interval_seconds = kwargs.get('actual_interval_seconds')
    
    Relies on scene tree on_frame events so it needs to be inserted into scene tree to work.
    """
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)        
        self._passed_seconds = 0
        self.interval_seconds = kwargs.get('interval_seconds',1)

        self.on_timer = Signal()
        timer_callback = kwargs.get('on_timer')
        if timer_callback: self.on_timer.connect(timer_callback)

        self.on_frame.connect(self.frame_handler)
    
    def frame_handler(self,**kwargs):
        delta_ms = kwargs.get('delta_ms')
        self._passed_seconds += delta_ms/1000
        if self._passed_seconds > self.interval_seconds:
            self.on_timer.emit(actual_interval_seconds=self._passed_seconds)
            self._passed_seconds -= self.interval_seconds

import threading
import time

from .logger import Logger

class Timer:
    def __init__(self,activity:str):
        self.stop_timer_event = False
        self.timer_seconds = 0
        self.time_reports = 30 #sec
        self.time_increments = 1
        self.activity_str = activity

    def _timer_func(self):
        while not self.stop_timer_event:
            time.sleep(self.time_increments)
            self.timer_seconds += self.time_increments
            
            if (self.timer_seconds/self.time_reports).is_integer():
                message = f"{self.activity_str}: Timer = {self.timer_seconds} sec"
                print(message)
                
            
    def start(self):
        self.thread = threading.Thread(target = self._timer_func)
        self.thread.start()

        message = f'STARTS:{self.activity_str}'
        print(message)
        
    
    def end(self):
        self.stop_timer_event = True
        if self.thread:
            self.thread.join()
        
        message = f"ENDS:{self.activity_str}, TIME TAKEN = {self.timer_seconds} sec"
        print(message)  




    
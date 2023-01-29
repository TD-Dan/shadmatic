
"""Basic logger"""
import os
import datetime

from enum import Enum

from multiprocessing import Lock

class LOG_LEVEL(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class LogEntry:
    def __init__(self,level:LOG_LEVEL, str:str, exception:Exception=None) -> None:
        self.level = level
        self.str = str
        self.exception = exception
        self.time = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())


# Global state shared by all Log instances across threads
log_history : list = []
logfile = None
log_instances = 0

log_mutex = Lock()

class Log:
    def __init__(self,logger_name:str) -> None:
        did_open_file = False
        
        #local state
        self._listeners: list[callable] = []
        self.echo = True
        self.logger_name=logger_name

        #global state
        global log_mutex
        log_mutex.acquire()
        try:
            global logfile
            global log_instances
            log_instances += 1

            if not logfile:
                log_date = '{date:%Y-%m-%d-%H_%M}'.format(date=datetime.datetime.now())
                _logfile_name = '_logs/'+log_date+".txt"
                if not os.path.exists("_logs"):
                    os.makedirs("_logs")
                logfile = open(_logfile_name, "w")
                did_open_file = True
        finally:
            log_mutex.release()
        
        if did_open_file:    
            self._write("Opened logfile.")
        self._write("Started logging, total logs:"+str(log_instances))
    
    def __del__(self):
        do_close_file = False
        instances = None

        #global state
        global log_mutex
        log_mutex.acquire()
        try:
            global log_instances
            log_instances -= 1
            instances = log_instances
            if log_instances == 0:
                do_close_file = True
        finally:    
            log_mutex.release()

        #local state
        self._write(self.logger_name+"Stopped logging, logs left: "+str(instances))
        if do_close_file:    
            self._write("Closing logfile.")

        if do_close_file:
            #back to global state
            log_mutex.acquire()
            try:
                global logfile
                logfile.close()
            finally:    
                log_mutex.release()

        
    def add_listener(self,call:callable):
        self._listeners.append(call)

    def info(self,str:str,exception:Exception=None):
        self._broadcast_new(LogEntry(LOG_LEVEL.INFO,str,exception))

    def warning(self,str:str,exception:Exception=None):
        self._broadcast_new(LogEntry(LOG_LEVEL.WARNING,str,exception))

    def error(self,str:str,exception:Exception=None):
        self._broadcast_new(LogEntry(LOG_LEVEL.ERROR,str,exception))

    def _write(self, str):
        global log_mutex
        log_mutex.acquire()
        try:
            str = '['+self.logger_name+']'+str
            if self.echo:
                print(str)
            if logfile:
                logfile.write(str+"\n")
                logfile.flush()
        finally:
            log_mutex.release()
        
    def _broadcast_new(self, entry:LogEntry):
        logline = ""
        end_str : str = ""
        e = entry.exception 
        if e:
            end_str = " with exception:\n"+f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
        logline = "\t["+entry.time+"] "+entry.level.name+": \t"+entry.str + end_str
        self._write(logline)
        for call in self._listeners:
            call(str=entry.str, exception=entry.exception)
        
        global log_mutex
        log_mutex.acquire()
        try:
            log_history.append(entry)
        finally:
            log_mutex.release()
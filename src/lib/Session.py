import uuid
import time


class Session:
    
    def __init__(self, ip):
        self.ip = ip
        self.id = str(uuid.uuid4())
        self.started = time.time()
        self.updated = time.time()
        
        self.game = None
        
    def update(self, coordinates:tuple=None):
        self.updated = time.time()
        
        # returns field and queue, maybe steps
        
    def check(self):
        current_time = time.time()
        delta = int(current_time - self.updated)
        
        return delta < 60 * 30 # if older than 30min, return false
    
    def __repr__(self):
        return self.id
    
    
if __name__ == '__main__':    
    session = Session('1.2.3.4')
    print(session)
    
    time.sleep(3)
    session.check()
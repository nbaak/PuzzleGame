import uuid
import time
import Game


class Session:
    
    def __init__(self, ip):
        self.ip = ip
        self.id = str(uuid.uuid4())
        self.started = time.time()
        self.updated = time.time()
        self.closed = None
    
        self.points = 0
        self.username = None
        
        self.game:Game = None
        
    def update(self, coordinates:tuple[int]):
        self.updated = time.time()
        
        _, points, gameover = self.game.play(coordinates)        
        
        return self.game.field, gameover
        
    def check(self, max_age:int=30) -> bool:
        """
            check
            checks if session is older than max_age
            max_age:int : age in minutes
            @return: bool
            
        """
        if not self.game:
            return False
        
        current_time = time.time()
        delta = int(current_time - self.updated)
        
        return delta < 60 * max_age # if older than 30min, return false
        
    def close(self):
        self.closed = time.time()
        self.points = self.game.points
    
    def __repr__(self):
        return self.id
    
    
if __name__ == '__main__':    
    session = Session('1.2.3.4')
    print(session)
    
    time.sleep(3)
    session.check()
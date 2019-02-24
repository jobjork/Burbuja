class StateCollection:
    BASE = 0
    FOCUSED = 1
    TO_FOCUSED = 2
    FROM_FOCUSED = 3
    
    @staticmethod
    def time_to_switch_state(current_state, time_ms):

        if current_state == StateCollection.BASE:
            time_limit_ms = 1000
        elif current_state == StateCollection.FOCUSED:
            time_limit_ms = 1000
        elif current_state == StateCollection.TO_FOCUSED:
            time_limit_ms = 4000
        elif current_state == StateCollection.FROM_FOCUSED:
            time_limit_ms = 2000
        
        return time_ms >= time_limit_ms
    
    @staticmethod
    def next_state(current_state):
        return (current_state + 1) % 4


class State:

    def __init__(self, b_list):
        self.time = 0
        self.dt_s = 0.0  # Time in seconds
        self.started = False
        self.b_list = b_list
        self.ball_count = 0
        self.ball_locked = False
        self.state = StateCollection.BASE
        self.millis_of_last_switch = 0

    def update(self):
        if not self.started:
            self.started = True
            return
        new_time = millis()
        self.dt_s = (new_time - self.time) / 1000.0
        self.time = new_time
        
        time_this_state_ms = millis() - self.millis_of_last_switch
        if StateCollection.time_to_switch_state(self.state, time_this_state_ms):
            self.state = StateCollection.next_state(self.state)   
            self.millis_of_last_switch = millis()
            
    def resize_ball_in_list(self, b_list):
        if self.state == 2 and not self.ball_locked:
            self.ball_count +=1
            self.ball_locked = True
            self.ball_count = self.ball_count % len(b_list)
            b_list[self.ball_count].start_growth()
        elif self.state == 3:
            b_list[self.ball_count].start_shrinkage()
            self.ball_locked = False            

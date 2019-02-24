enum StateCollection {
    BASE(0),
    TO_FOCUSED(1),
    FOCUSED(2),
    FROM_FOCUSED(3);
    
    private final Integer level;
    
    private StateCollection(Integer level) {
      this.level = level;
    }
    
    static StateCollection getState(Integer level) {
      if (level == 0 ) { 
        return StateCollection.BASE;
      }
      if (level == 1 ) { 
        return StateCollection.TO_FOCUSED;
      }
      if (level == 2 ) { 
        return StateCollection.FOCUSED;
      }
      if (level == 3 ) { 
        return StateCollection.FROM_FOCUSED;
      }
      return StateCollection.BASE;
    }

    static boolean timeToSwitchState(StateCollection currentState, Integer timeMs) {
      Integer timeLimitMs = 0;
      if (currentState.equals(StateCollection.BASE)) {
        timeLimitMs = 1000;
      }
      if (currentState.equals(StateCollection.TO_FOCUSED)) {
         timeLimitMs = 5000;
      }
      if (currentState.equals(StateCollection.FOCUSED)) {
        timeLimitMs = 5000;
      }
      if (currentState.equals(StateCollection.FROM_FOCUSED)) {
         timeLimitMs = 1000;
      }
        return timeMs >= timeLimitMs;
    }

    static StateCollection nextState(StateCollection currentState) {
      return getState((currentState.level + 1) % 4);
    }
}

class State {

  Integer time;
  Float dtSeconds;
  Boolean started;
  List<Burbuja> bList;
  Integer ballCount;
  Boolean ballLocked;
  StateCollection state;
  Integer millisOfLastSwitch;
  
  State() {
    this.time = 0;
    this.dtSeconds = 0.0;
    this.started = false;
    this.ballCount = 0;
    this.ballLocked = false;
    this.state = StateCollection.BASE;
    this.millisOfLastSwitch = 0;
  }

  void update() {
    if (!this.started) {
      this.started = true;
      return;
    }
    Integer newTime = millis();
    this.dtSeconds = (newTime - this.time) / 1000.0;
    this.time = newTime;
    
    Integer timeThisStateMs = millis() - this.millisOfLastSwitch;

    if (StateCollection.timeToSwitchState(this.state, timeThisStateMs)) {
      this.state = StateCollection.nextState(this.state);
      this.millisOfLastSwitch = millis();
    }
  }
  
  void resizeBallInlist(List<Burbuja> bList) {
    Boolean lockBall = this.state.equals(StateCollection.TO_FOCUSED) && !this.ballLocked;
    if (lockBall) {
      this.ballCount += 1;
      this.ballLocked = true;
      this.ballCount = this.ballCount % bList.size();
      bList.get(this.ballCount).startGrowth();

    } else if (this.state.equals(StateCollection.FROM_FOCUSED)) {
      bList.get(this.ballCount).startShrinkage();
      this.ballLocked = false;
    } else if (this.state.equals(StateCollection.FOCUSED)) {
      bList.get(this.ballCount).stopGrowth();      
    }
  }
}

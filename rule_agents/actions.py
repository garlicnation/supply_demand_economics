class Action(object):
    "This rule is evaluated if requirements are met and changes the state if they are"
    def __init__(self, state):
        self.state = state
      
    """evaluate()
          Returns true if the rule was evaluated
          Returns false if the rule wasn't evaluated
          
          If evaluate returns true, the rule shouldn't effect the simulation 
          until the current queue of rules been emptied"""
    def evaluate(self):
        
        precondition_met = self.precondition()
        if not precondition_met:
            return False
        self.consequences()
        return True
    
    #We simply check to see if certain facts are present in our rul
    def precondition(self, reqs):
        for req in reqs:
            if self.state[req] == None:
                return False
        return True
        
    #precondition met. Let's effect the state as we will
    def consequences(self):
        pass
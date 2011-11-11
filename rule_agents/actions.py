class DieException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Agent is dead! Maybe he should suck less next time')

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
    
class DieAction(Action):
    def precondition(self):
        if self.state['energy'] <= 0:
            return True
        
    def consequences(self):
        self.state['dead'] = "True"
        raise DieException
    
class RunAction(Action):
    def precondition(self):
        if self.state['energy'] >= 10:
            return True
        
    def consequences(self):
        self.state['energy'] -= 10
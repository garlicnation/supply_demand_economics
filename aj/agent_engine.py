class NoneDict(dict):
    def __missing__(self,key):
        return None

class Action(object):
    "This rule is evaluated if requirements are met and changes the state if they are"
    def __init__(self, state):
        self.state = state
      
    """Returns a tuple containing reqmet. 
        reqmet = We were ready to evaluate the rule
            If true, the state was changed and the rule can be discarded"""
    def check(self):
        #See if we're ready to evaluate the rule
        reqmet = self.precondition()
        if not reqmet:
            return reqmet
        self.result()
        return True
    
    #Precondition checks to see if we want to execute the rule
    def precondition(self, reqs):
        for req in reqs:
            if self.state[req] == None:
                return False
        return True
    
    #Once the precondition has passed, result modifies the state accordingly
    def result(self):
        pass
        
    
    
class TransportModeAction(Action):
        
    def precondition(self):
        return super(TransportModeAction, self).precondition(['av_speed'])
        
    def rule(self):
        if self.state['av_speed'] > 60:
            self.state['fly'] = True
        else:
            self.state['drive'] = True
            
class AirplaneChoiceAction(Action):
        
    def precondition(self):
        reqs = ['fly', 'is_pilot']
        return super(AirplaneChoiceAction, self).precondition(reqs)
        
    def rule(self):
        if self.state['fly']:
            if not self.state['is_pilot']:
                self.state['fly_commercial'] = True
                
            if (self.state['like_scenery'] and 
                    self.state['av_speed'] < 200 and
                    self.state['av_speed'] > 100):
                self.state['fly_bon'] = True
                
            if (self.state['like_scenery'] and 
                    self.state['av_speed'] < 100):
                    self.state['fly_tcart'] = True
                
            if (self.state['like_scenery'] and 
                    self.state['av_speed'] < 200 and
                    self.state['av_speed'] > 100):
                self.state['fly_bon'] = True
            
class CarAction(Action):
        
    def precondition(self):
        reqs = ['drive', 'motorcycle']
        return super(CarAction, self).precondition(reqs)
        
    def rule(self):
        self.state['car'] = self.state['drive'] and not self.state['motorcycle']
        
class MotorcycleAction(Action):
        
    def precondition(self):
        reqs = ['drive']
        return super(MotorcycleAction, self).precondition(reqs)
        
    def rule(self):
        self.state['motorcycle'] = self.state['drive'] and self.state['like_scenery']
            
class Agent(object):
    def __init__(self, rules=[], state = {'energy': 100, 'time': 0, 'money': 100, 'skills':['S1', 'S2']}):
        "A list of the rules to be considered"
        self.rules = rules
        self.state = NoneDict(state)
        self.inbox = {}
        self.outbox = {}
        
    """Modify the state based on our rules
       Returns false if the agent dies and should be removed from the queue"""
    def do_turn(self):
        to_evaluate = []
        for rule in self.rules:
            to_evaluate.append(rule(self.state))
        
        self.state['inbox'] = self.inbox
        self.inbox = {}
        self.outbox = {}
            
        finished = False
        while len(to_evaluate) > 0 and not finished:
            finished = True
            to_delete = []
            for rule in to_evaluate:
                print "Trying a rule"
                if rule.check():
                    print "We evaluated %s!" % (rule)
                    to_delete.append(rule)
                    finished = False
            
            
                    
            print "%d rules left" % (len(to_evaluate))
                    
        return True


def main():
    
    rb = Agent([AirplaneChoiceAction, CarAction, MotorcycleAction, TransportModeAction])
    
    state = rb.query({"like_scenery": True, "pilot": False, "av_speed": 45})
    
    print state

if __name__ == "__main__":
    main()
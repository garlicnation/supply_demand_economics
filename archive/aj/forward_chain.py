class NoneDict(dict):
    def __missing__(self,key):
        return None

class Rule(object):
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
            return False
        self.rule()
        return True
    
    def precondition(self, reqs):
        for req in reqs:
            if self.state[req] == None:
                return False
        return True
        
    
    
class TransportModeRule(Rule):
        
    def precondition(self):
        return super(TransportModeRule, self).precondition(['av_speed'])
        
    def rule(self):
        if self.state['av_speed'] > 60:
            self.state['fly'] = True
        else:
            self.state['drive'] = True
            
class AirplaneChoiceRule(Rule):
        
    def precondition(self):
        reqs = ['fly', 'is_pilot']
        return super(AirplaneChoiceRule, self).precondition(reqs)
        
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
            
class CarRule(Rule):
        
    def precondition(self):
        reqs = ['drive', 'motorcycle']
        return super(CarRule, self).precondition(reqs)
        
    def rule(self):
        self.state['car'] = self.state['drive'] and not self.state['motorcycle']
        
class MotorcycleRule(Rule):
        
    def precondition(self):
        reqs = ['drive']
        return super(MotorcycleRule, self).precondition(reqs)
        
    def rule(self):
        self.state['motorcycle'] = self.state['drive'] and self.state['like_scenery']
            
class RuleBase(object):
    def __init__(self, rules=[]):
        "A list of the rules to be considered"
        self.rules = rules
        self.state = None
        
    "Modify the state based on our rules"
    def query(self, state):
        none_state = NoneDict(state)
        to_evaluate = []
        for rule in self.rules:
            to_evaluate.append(rule(none_state))
            
        finished = False
        while len(to_evaluate) > 0 and not finished:
            finished = True
            for rule in to_evaluate[:]:
                print "Trying a rule"
                if rule.check():
                    print "We evaluated %s!" % (rule)
                    to_evaluate.remove(rule)
                    finished = False
                    
            print "%d rules left" % (len(to_evaluate))
                    
        return none_state


def main():
    
    rb = RuleBase([AirplaneChoiceRule, CarRule, MotorcycleRule, TransportModeRule])
    
    state = rb.query({"like_scenery": True, "pilot": False, "av_speed": 45})
    
    print state

if __name__ == "__main__":
    main()
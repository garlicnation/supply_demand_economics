from actions import *
agentid = 0
class Agent(object):
    def __init__(self, actions, state, name = "Agent %d" % agentid):
        "An agent's actions are the collection of rules and consequences that govern an agent's behavior"
        global agentid 
        agentid += 1
        self.name = name
        actionID = 0
        self.actions = {}
        self.state = {'energy':100, 'money':40, 'time':0, 'capabilities':["minning"], 'materials':[], 'tools':["book"]}
        for action in actions:
            self.actions["%s%d" % (str(action), actionID)] = action(self.state)
            actionID += 1
        
        """An agent's state is the collection of keys and values that 
           define an agent's internal representation of the world"""
        self.state.update(state)
        
        """An agent's inbox is the collection of messages that an agent has
           received in the last turn. This collection is processed once for every call to do_turn"""
        self.state['inbox'] = {}
        self.inbox = self.state['inbox']
        
        """An agent's outbox is a sort of 'poster board' for letting the world
           know what we want them to know"""
        self.state['outbox'] = {}
        self.outbox = self.state['outbox']
        
        
    
    """Executes a turn.
       Evaluates all the actions we're going to this turn.
       Throws a DieException if the agent is unable to continue 
       acting in the simulation"""
    def do_turn(self): 
          
        finished = False
        currentActions = set(self.actions.itervalues())
        while len(currentActions) > 0 and not finished:
            finished = True
            toRemove = set()
            for action in currentActions:
                print "Trying a rule"
                try:
                    if action.evaluate():
                        print "We evaluated %s!" % (action)
                        #If the action requires sending a message, we send it, making sure to reference ourselves if necessary
                        if action.message is not None:
                            msg, receiver = action.message
                            receiver.inbox.append((msg, self))


                        #If the action takes time, we return
                        if action.time_required is not None:
                            return action.time_required
                        toRemove.add(action)
                        finished = False
                except DieException:
                    print "%s has died" % self.name
                    return None 
            
            currentActions -= toRemove
            print "Agent %s has Money: %d" % (self.name ,self.state['money'])   
            print "Agent " + self.name +  " has Materials: " 
            print self.state['materials']
            print "%d rules left" % (len(currentActions))
                    
        return True

    
class CitizenAgent(Agent):
    def __init__(self, state, name):
        actions = [RunAction, DieAction, MineAction]
        Agent.__init__(self, actions, state, name)
        
class BankAgent(Agent):
    def __init__(self, state, name):
        actions = [RunAction, DieAction, GiveLoanAction]
        Agent.__init__(self, actions, state, name)
        

class FarmerAgent(Agent):
    def __init__(self, state, name):
        actions = [RunAction, DieAction, FarmAction, NeedLoanAction]
        Agent.__init__(self, actions, state, name)
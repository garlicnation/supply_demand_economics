def Agent(object):
    
    def __init__(self, actions, state):
        "An agent's actions are the collection of rules and consequences that govern an agent's behavior"
        actionID = 0
        self.actions = {}
        self.state = {'energy':100, 'money':100, 'time':0, 'capabilities':[], 'materials':[]}
        for action in actions:
            self.actions["%s%d" % (action(self.state), actionID)] = action
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
                if action.evaluate():
                    print "We evaluated %s!" % (action)
                    toRemove.add(action)
                    finished = False
            
            currentActions -= toRemove        
            print "%d rules left" % (len(currentActions))
                    
        return True
    
    
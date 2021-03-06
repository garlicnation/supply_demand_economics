import agents


msg = ''

class DieException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Agent is dead! Maybe he should suck less next time')

class Action(object):
    "This rule is evaluated if requirements are met and changes the state if they are"
    def __init__(self, state):
        self.state = state
        self.time_required = 10
        self.message = None
        # This should look like (message, target), that is, ("Give me a loan", bank_agent)
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
            if self.state[req] is None:
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
        self.time_required = None
        raise DieException

class RunAction(Action):
    def precondition(self):
        if self.state['energy'] >= 10:
            return True

    def consequences(self):
        self.state['energy'] -= 10
        self.time_required = 20


class NeedLoanAction(Action):
    def precondition(self):
        # Need money if you have less than minimum
        if self.state['money'] < 50:
            if 'pending_loans' not in self.state or self.state['pending_loans'] ==0:
                return True

    def consequences(self):
    # Must Put in the inbox of the banker Agent that we need money
    # Then when the banker sees it. He will evaluate the request
    # and then give the money or not
        print "bank"
        self.message = ('I need a loan', self.state['bank_agent'])
        if 'pending_loans' not in self.state:
            self.state['pending_loans'] = 1
        else:
            self.state['pending_loans'] += 1
        #  banker.state['inbox'] = self.id, "need a loan"
        self.time_required = 2


class GiveLoanAction(Action):   # for the banker


    def precondition(self):
        # check who needs a loan
        self.agents = []  # List of agents that need a loan

        #i = 0
        #print self.state['inbox']
        #try:
        #    agent = self.state['inbox']['I need a loan']
        #    self.agents.append(agent)
        #    print agent
        #    return True
        #except:
        #    print "None"

        for msg, agent in self.state['inbox']:
            if msg == 'I need a loan':
                print self.state['inbox']
                self.agents.append(agent)

        if  len(self.agents) > 0 :
            return True

      #  agent, msg in self.state['inbox']
      #  print msg
      #  print agent
      #  if msg == 'I need a loan':
      #      agents.append(agent)
      #      return True




    def consequences(self):
        #Give Loans to the asking agent

        for agent in self.agents:
            agent.state['money'] += 20


       # print str(agent) + " is getting a loan"
       # agent.state['money'] = 10000

            # Record the loam in a loan class
        self.time_required = 2



class SellAction(Action):
    def precondition(self):
        # Requires Time, Energy, tools   How to decide which tool to sell
        if self.state['energy'] >= 10 and self.state['tools'] >= 1 :
            return True

    def consequences(self):
        self.state['energy'] -= 10
        self.state['tools'] -= 1
        self.time_required = 15


class BuyAction(Action):
    def precondition(self):
        # Requires Time, Energy, money   How to decide which tool to sell
        if self.state['energy'] >= 10 and self.state['money'] >= 50 :
            return True

    def consequences(self):
        self.state['energy'] -= 10
        self.state['tools'].append("New tool")
        # We can also add material
        self.time_required = 10


class FarmAction(Action):
    def precondition(self):
        # Requires Time, Energy, capability , tools, material and money
        if self.state['energy'] >= 10 and self.state['money'] >= 10:
            for item in self.state['capabilities']:
                if item == "farming":
                    return True

    def consequences(self):
        self.state['energy'] += 10
        self.time_required = 40


class LearnAction(Action):
    def precondition(self):
        # Requires Time, Energy, material and money
        if self.state['energy'] >= 10 and self.state['money'] >= 10:
            for item in self.state['tools']:
                if item == "book":
                    return True

    def consequences(self):
        self.state['energy'] -= 10
        self.state['capabilities'].append("New Capability")
        self.time_required = 20


class ManufactureAction(Action):
    def precondition(self):
        # Requires Time, Energy, material, money, and capability
        if self.state['energy'] >= 10 and self.state['money'] >= 10 and self.state['materials'] == "rawmaterials":
            for item in self.state['capabilities']:
                if item == "manufacturing":
                    return True

    def consequences(self):
        self.state['energy'] -= 10
        self.state['tools'].append("New tool")
        self.time_required = 50




class MineAction(Action):
    def precondition(self):
        # Requires Time, Energy, money, and capability
        if self.state['energy'] >= 10 and self.state['money'] >= 10 :
            for item in self.state['capabilities']:
                if item == "minning":
                    return True
                    # return time
    def consequences(self):
        self.state['energy'] -= 10
        self.state['materials'].append("New materials")
        self.time_required = 100
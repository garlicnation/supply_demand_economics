# Based o:n forward_chain.py and agent_engine.py/
# Provides the control structure that starts a general rule-based multi-agent simulation
# Along with a reference implementation attempting to model the economy
# new


from agents import CitizenAgent
from heapq import *


class AgentEngine(object):
    
    def __init__(self, agents):
        self.agents = agents

class EconomicAgentEngine(AgentEngine):
    
    def __init__(self):
        agents = []
        for i in range(10):
            state = {}
            a = CitizenAgent(state, "Agent %d" % i)
            agents.append((0, a))
            
        AgentEngine.__init__(self, agents)
            
        
    def run_engine(self, turns=100):
        heapify(self.agents)
        while turns > 0 and len(self.agents) >0:
            current_time, agent = heappop(self.agents)
            time_for_turn = agent.do_turn()
            if time_for_turn != None:
                heappush(self.agents, (current_time+time_for_turn, agent))
                
            turns -=1
            
        print "Simulation over"

if __name__=="__main__":
    engine = EconomicAgentEngine()
    engine.run_engine()                
# Based o:n forward_chain.py and agent_engine.py/
# Provides the control structure that starts a general rule-based multi-agent simulation
# Along with a reference implementation attempting to model the economy


from agents import CitizenAgent


class AgentEngine(object):
    
    def __init__(self, agents):
        self.agents = agents

class EconomicAgentEngine(AgentEngine):
    
    def __init__(self):
        agents = {}
        for i in range(10):
            state = {}
            a = CitizenAgent(state, "Agent %d" % i)
            agents[a.name] = a
        AgentEngine.__init__(self, agents)
            
        
    def run_engine(self, turns=100):
        
        while turns > 0 and len(self.agents) >0:
            dead = []
            for agent in self.agents:
                print "In run_engine", agent
                if self.agents[agent].do_turn() == False:
                    dead.append(agent)
            
            for agent in dead:
                self.agents.pop(agent)
                
            turns -=1
            
        print "Simulation over"

if __name__=="__main__":
    engine = EconomicAgentEngine()
    engine.run_engine()                
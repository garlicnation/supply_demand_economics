# Based on forward_chain.py and agent_engine.py/
# Provides the control structure that starts a general rule-based multi-agent simulation
# Along with a reference implementation attempting to model the economy





class AgentEngine(object):
    
    def __init__(self, agents):
        self.agents = agents

class EconomicAgentEngine(AgentEngine):
    pass
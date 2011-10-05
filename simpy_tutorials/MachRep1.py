import SimPy.Simulation
import random

class G:
    Rnd = random.Random()
    
class MachineClass(SimPy.Simulation.Process):
    UpRate = 1/1.0
    RepairRate = 1/0.5
    TotalUpTime = 0.0
    NextID = 0
    def __init__(self):
        SimPy.Simulation.Process.__init__(self)
        
        self.StartUpTime = 0.0
        self.ID = MachineClass.NextID
        MachineClass.NextID += 1
        
    def Run(self):
        while True:
            self.StartUpTime = SimPy.Simulation.now()
            
            UpTime = G.Rnd.expovariate(MachineClass.UpRate)
            yield SimPy.Simulation.hold, self, UpTime
            
            MachineClass.TotalUpTime += SimPy.Simulation.now() - self.StartUpTime
            RepairTime = G.Rnd.expovariate(MachineClass.RepairRate)
            
            yield SimPy.Simulation.hold, self, RepairTime

def main():
    SimPy.Simulation.initialize()
    
    machines = 2
    
    for i in range(machines):
        M = MachineClass()
        SimPy.Simulation.activate(M, M.Run())
        
    MaxSimtime = 10000.0
    SimPy.Simulation.simulate(until=MaxSimtime)
    print "the percentage of up time was", MachineClass.TotalUpTime/(machines*MaxSimtime)
    
if __name__ == '__main__':
    main()
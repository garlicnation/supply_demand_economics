import SimPy.Simulation
import random

class G:
    Rnd = random.Random()
    
class MachineClass(SimPy.Simulation.Process):
    UpRate = 1/1.0
    RepairRate = 1/0.5

    TotalUpTime = 0.0
    NextID = 0
    def __init__(self, StartUpTime=0.0):
        SimPy.Simulation.Process.__init__(self)
        
        self.StartUpTime = StartUpTime
        self.ID = MachineClass.NextID
        MachineClass.NextID += 1
        
    def Run(self):
        RepairTime = 0.0
        while True:
            self.StartUpTime = SimPy.Simulation.now()
            
            print "T= %8.2f\tMachine %d working. Took %f to repair" % (SimPy.Simulation.now(),self.ID, RepairTime)

            UpTime = G.Rnd.expovariate(MachineClass.UpRate)
            yield SimPy.Simulation.hold, self, UpTime

            print "T= %8.2f\tMachine %d broke down after %f minutes" % (SimPy.Simulation.now(),self.ID, UpTime)
            
            MachineClass.TotalUpTime += SimPy.Simulation.now() - self.StartUpTime
            RepairTime = G.Rnd.expovariate(MachineClass.RepairRate)
            
            yield SimPy.Simulation.hold, self, RepairTime

def main():
    SimPy.Simulation.initialize()
    
    machines = 2
    
    for i in range(machines):
        M = MachineClass()
        SimPy.Simulation.activate(M, M.Run())
        
    MaxSimtime = 10.0
    SimPy.Simulation.simulate(until=MaxSimtime)
    print "the percentage of up time was", MachineClass.TotalUpTime/(machines*MaxSimtime)
    
if __name__ == '__main__':
    main()
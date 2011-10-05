from  SimPy.Simulation import *
from random import Random, expovariate, uniform

class G: # globals
    Rnd = Random(12345)
    RepairPerson = Resource(1)
    
class MachineClass(Process):
    UpRate = 1/1.0 #Breakdown rate
    RepairRate = 1/0.5 #Repair rate
    TotalUpTime = 0.0
    
    NRep = 0 #Times machiens repaired
    NImmedRep = 0 #Number of breakdowns that were completed immediately
    NextID = 0 #Next unique ID for machines
    NUp = 0 #Total machines up
    def __init__(self):
        Process.__init__(self)
        
        self.StartUpTime = 0.0
        self.ID = MachineClass.NextID
        MachineClass.NextID += 1
        MachineClass.NUp += 1
        
    def Run(self):
        while True:
            print "Machine %d up" % (self.ID)
            UpTime = G.Rnd.expovariate(MachineClass.UpRate)
            yield hold, self, UpTime
            
            MachineClass.TotalUpTime += UpTime
            
            MachineClass.NRep += 1
            
            if G.RepairPerson.n == 1:
                MachineClass.NImmedRep += 1
            
            print "Machine %d down after %f" % (self.ID, UpTime)
            #We request a repairPerson
            
            PreRepair = now()
            yield request, self, G.RepairPerson
            
            print "Machine %d being repaired after waiting %f" % (self.ID, now()-PreRepair)
            
            #wait long enough to repair
            RepairTime = G.Rnd.expovariate(MachineClass.RepairRate)
            yield hold, self, RepairTime
            
            print "Machine %d repaired after %f" % (self.ID, RepairTime)
            #Repair done, release repairperson
            yield release, self, G.RepairPerson

class BreakDown(Process):
    def __init__(self, machine):
        self.machine = machine
        
    def breakMachine(self, BDRate = 0.5):
        while True:
            yield hold, self, G.Rnd.expovariate(BDRate)
       

def main():
    initialize()
    
    machines = 5
    
    for i in range(machines):
        M = MachineClass()
        activate(M, M.Run())
        
    MaxSimtime = 10000.0
    simulate(until=MaxSimtime)
    print "the percentage of up time was", MachineClass.TotalUpTime/(machines*MaxSimtime)
    
if __name__ == '__main__':
    main()
# Ishag Alexanian
# CS496 Implementing a Bank Agent and a Citizen Agent

from SimPy.Simulation import *
from random import Random
#from  SimPy.SimulationTrace import *
 

class Citizen ( Process ):
    NextID = 1
    
    def __init__(self):
        Process.__init__(self)
        self.ID = Citizen.NextID # ID or name is a number for a citizen agent to be identified    
        Citizen.NextID += 1
        self.Energy = random.randint(0, 10)    # Energy level is number between 0 and 10 for the level of energy that an agent has
        self.Credit = random.randint(0, 10)    # Credit it the credit score of the agent
        self.Money = 0     # Is the amount of money that an agent has
        self.Innovate = random.randint(1, 10) # Is the innovation level of an agent
        
    def Run(self,BankAgent):
        while True:
            # This is Loaning based on wanting energy and Innovation  
            
            
            if self.NeedEnergyLoan():    
                yield request, self, Bank.bankerperson
                print "T= %f   Agent %d wants a loan because his Energy: %d is less than 5." % (now(),self.ID,self.Energy)
                LoanAmount = random.randint(1, 10)
                BankAgent.AddLoan(self,LoanAmount) # Here you have to pass certain amount of money to add the loan and also be consistent with 
                self.Money += LoanAmount   # the amount added to self 
                self.Energy += 1
                print "T= %f   Agent %d has now money:%d and an Energy Level of %d.\n" % (now(),self.ID,self.Money,self.Energy) 
                yield hold, self, 2
                yield release, self, Bank.bankerperson  
            else:
                print "T= %f   Agent %d has an Energy of: %d, it will be decremented by one. \n" % (now(),self.ID,self.Energy)
                yield hold, self, 2
                self.Energy -= 1  
                
            self.CheckLoanPayback(BankAgent)
            
           
    def NeedEnergyLoan(self):
        if self.Energy < 5:
            return True
        else:
            return False
        
    def InnovateLoan(self):
        if self.Innovate > 8:
            return True
        else:
            return False
        
    def CheckLoanPayback(self,BankAgent):
        self.paymoney = [] # paymoney[0] is the loan ID    [1] loan amount    [2] y or n    y for yea its due or n for no its not due yet
        self.paymoney = BankAgent.CheckDues(self)
        
        if self.paymoney != []:
            if self.paymoney[2]=="y": 
                if (self.Money - self.paymoney[1])<0:
                    print "Kill Agent"
                else:
                    self.Money -= self.paymoney[1]
                    BankAgent.Remit(self,self.paymoney[0]) 
                    print 'T= %f   Agent %d has paidoff Loan number: %d \n' % (now(),self.ID,self.paymoney[0])
        
        
    def printCitizen(self):
        print 'Agent %d has money: %f and Energy of: %d' %(self.ID, self.Money,self.Energy)
     
    def __str__(self):
        return 'Agent %d' %(self.ID)
             
            

class Loan():
    NextLoanID = 1
    
    def __init__(self,Customer,LoanAmount):
        self.ID = Loan.NextLoanID     # is the loan ID 
        Loan.NextLoanID += 1
        self.Customer = Customer  
        self.LoanAmount = LoanAmount  # how much proposed
        self.TimeofBorrowed = now() 
        self.TimeIntervalRate = 0.25   # What are the time intervals that the agent has to pay back
        self.LoanAge = 8             #random.randrange(4, 14, 2)
        self.interest = 0.3  # This interest will be the percentage of the money that goes back to the bank agent
        self.Status = "NonPaid"
        
    def GetID(self):
        return self.ID 
    
    def SetStatus(self,stats):
        self.Status = stats
        
    def GetStatus(self):
        return self.Status 
        
    def GetCustomer(self):
        return self.Customer
    
    def GetLoanAge(self):
        return self.LoanAge
    
    def GetLoanAmount(self):
        return self.LoanAmount
    
    def GetTimeofBorrowed(self):
        return self.TimeofBorrowed
    
    
    def __str__(self):
        return ('Loan number:' + str(self.ID) + ', for '+ str(self.Customer)+', Loan Amount=' + str(self.LoanAmount)  
        + ', Time Interval Rate=' + str(self.TimeIntervalRate) +',  Time when Borrowed=' + str(self.TimeofBorrowed) 
        + ', Loan Age=' + str(self.LoanAge) + ',  with an interest=' + str(self.interest)) + ", with a Status: " + self.Status
        
        



class Bank():
# For now we have one bank present only
    bankerperson = Resource()  
       
    def __init__(self):
        self.ID = Citizen()
        self.LoanList = []
                
    def AddLoan(self,Customer,LoanAmount):
        print "\nThe Bank gave "+ str(Customer)+ " the Loan in the amount of " + str(LoanAmount) +"." 
        self.LoanList.append(Loan(Customer,LoanAmount))
        
    def LoanListPrint(self):
        print "\nThe Loan List:"
        for item in self.LoanList:    
            print item 
            
    def CheckDues(self,Customer):
        self.l = []
        for item in self.LoanList:
            if (Customer==item.GetCustomer()):
                if (item.GetStatus() == "NonPaid"):
                    if ((item.GetLoanAge() + item.GetTimeofBorrowed())== now()):
                        self.l.insert(0,item.GetID())
                        self.l.insert(1,item.GetLoanAmount())
                        self.l.insert(2,"y")
        
        return self.l
              
        
    def Remit(self,Customer,LoanID):
        for item in self.LoanList:
            if (Customer==item.Customer and LoanID==item.ID):
                item.SetStatus("Paid")
                
            
        
        
            
    def __str__(self):
        return 'The Bank is ' + str(self.ID)
    


            
def main():
# Beginning of main simulation program
    initialize()
    
    population = 3 # including the bank agent
    C = []  # List of all Citizens   
 
    C.append(Bank())   # add the bank agent to Citizen lists
    print C[0] # C[0] is the bank agent
    
    
    # Populating Agents in Citizen List
    for count in range(1,population):
        C.append(Citizen())     
    
    # Adding Loans based on energy    
    for count in range(1,population):
        activate(C[count], C[count].Run(C[0])) 
                       
    # start taking the credit score down if they don't pay their loans back at the Time Interval by the interval rate
    # start taking the credit score up if they pay their loans back at the Time Interval by the interval rate    

    # Adding Loans based on Innovation and Look at their credit score    
    #   for count in range(1,population):
    #       if C[count].Innovate >= 8:  # Also look at the credit score 
    #           C[0].AddLoan(C[count])
           

    simulate( until=20 )
    
    print "\n"
    for count in range(1,population):   
        C[count].printCitizen()
    

    #Printing The List of Loans
    C[0].LoanListPrint() 


if __name__ == '__main__':
    main()
    
# Also look at the credit score   
#Go Through the Yield Statement in the documentaion 
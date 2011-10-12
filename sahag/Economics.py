# Ishag Alexanian
# CS496 Implementing a Bank Agent and a Citizen Agent

from SimPy.Simulation import *
from random import Random, expovariate, uniform

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
            # This is Loaning based on wanting energy only  
            # Implementing another based out of need for innovation
            # Also look at the credit score  
            if self.Energy < 5:    
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
            
            
            

           
    def Buy(self):
        print "The agents energy level is down less than 5 so go out Buy"
        print "But if money is zero then get a loan"
        print "Buy something"
         
    def Sell(self):       
        print "Sell"
         
    def Produce(self):
        print "Produce"
        
    def printCitizen(self):
        return 'Agent %d has money: %f and Energy of: %d' %(self.ID, self.Money,self.Energy)
     
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
        self.LoanAge = random.randrange(1, 10, 2)# 3 minutes, For how long is the 
        self.interest = 0.3  # This interest will be the percentage of the money that goes back to the bank agent
    
    def __str__(self):
        return ('Loan number:' + str(self.ID) + ', for '+ str(self.Customer)+', Loan Amount=' + str(self.LoanAmount)  
        + ', Time Interval Rate=' + str(self.TimeIntervalRate) +',  Time when Borrowed=' + str(self.TimeofBorrowed) 
        + ', Loan Age=' + str(self.LoanAge) + ',  with an interest=' + str(self.interest))



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
            
    def __str__(self):
        return 'The Bank is ' + str(self.ID)
    


            
def main():
# Beginning of main simulation program
    initialize()
    
    population = 5 # including the bank agent
    C = []  # List of all Citizens   
 
    C.append(Bank())   # add the bank agent to Citizen lists
    print C[0] # C[0] is the bank agent
    
    
    # Populating Agents in Citizen List
    for count in range(1,population):
        C.append(Citizen())     
    
    # Adding Loans based on energy    
    for count in range(1,population):
        activate(C[count], C[count].Run(C[0])) 
             
             
    # For now don't give a second loan
    # Put the overall timer and simulations 
    # start taking the credit score down if they don't pay their loans back at the Time Interval by the interval rate
    # start taking the credit score up if they pay their loans back at the Time Interval by the interval rate    


    # Adding Loans based on Innovation and Look at their credit score    
 #   for count in range(1,population):
 #       if C[count].Innovate >= 8:  # Also look at the credit score 
 #           C[0].AddLoan(C[count])
           

    simulate( until=20 )
    
    print "\n"
    for count in range(1,population):   
        print str(C[count].printCitizen())
    

    #Printing The List of Loans
    C[0].LoanListPrint() 


if __name__ == '__main__':
    main()
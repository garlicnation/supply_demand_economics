from SimPy.Simulation import *
from SimPy.SimGUI import *
from random import randrange,random, seed, choice
from functools import partial
from Tkinter import *

class G:
    person_id = 0
    item_id = 0

class Gaia(Process):
    def __init__(self, name="Earth", population=50):
        Process.__init__(self, name=name)
        
        self.people = []
        self.population = population
        
    def creation(self):
        self.people = [Person(id=i, world=self) for i in xrange(self.population)]
        
        for person in self.people:
            person.start(person.run())
            
        yield passivate, self
        
        

class Person(Process):
    
    def __init__(self, id, world, name="Person"):
        Process.__init__(self, name=name+" "+str(id))
        
        
        self.actions = {'shop': self.shop, 'sleep':self.sleep, 
                        'entertain':self.entertain, 'socialize':self.socialize}
        
        self.world = world
        self.wallet = Level(name=self.name+"'s wallet", unitName='Dollars', initialBuffered=1000)
        self.energy = Level(name=self.name+"'s energy",  initialBuffered=100)
        self.storage = Store(name=self.name+"'s storage space", unitName='units')
        
        
        
        self.friends = []
        
    def run(self):
        some_stuff = []
        for i in range(10):
            some_stuff.append("Item "+str(G.item_id))
            G.item_id += 1
        yield put, self, self.storage, some_stuff
        while True:
            #Let's pick something to do
            current_action = self.action()
            #Now let's do it
            #I'm doing my best to keep the main run function simple. By putting the logic into sub-functions,
            # and having those subfunctions follow simpy's yielding converions, I can just cycle through the iterators I generate each turn
            # and let my current action do most of the work.
            # We'll use run() to handle interruptions
            for step in current_action():
                yield step
        
    
    #Each person has a different view of the world.
    #The value function is used by a person to dynamically determine what he consdiers something worth.
    def value(self, artifact):
        return randrange(100)
    
    #Here is the price we tell others something is worth
    def quote(self, artifact):
        return randrange(100)
    
    def purchase(self, contact, items):
        result = []
        current_money = self.wallet.amount
        for item in items:
            other_quote = contact.quote(item)
            my_value = self.value(item)
 #           print "%s thinks this thing is worth %f while %s is trying to sell it for %f"% (self.name, my_value, contact.name, other_quote)
            if my_value > other_quote and current_money >= other_quote:
                current_money -= other_quote
                result.append(item)
        return result
    
    #This function is how we're going to decide what to do next.
    def action(self):
        if self.energy.amount < 10:
            return self.sleep
        return choice(list(self.actions.values()))
    
    def shop(self):
        for friend in self.friends:
            purchase_decision = partial(self.purchase, friend)
            #Let's get some things that we think are a good deal.
            #If we don't find anything, we just move on
            yield (get,self, friend.storage, purchase_decision), (hold, self, 4)
            if self.acquired(friend.storage):
                purchased = self.got
                for item in purchased:
                    price = friend.quote(item)
                    my_price = self.value(item)
#                    print "I thought %s was worth %f so I bought it for %f" % (str(item), my_price, price)
                    yield get, self, self.wallet, price
                    yield put, friend, friend.wallet, price
                #It took some time to make our purchases
                yield hold, self, len(purchased)
                
                #Make sure to put what we got in our store
                yield put, self, self.storage, purchased
            else:
                continue
                
            
            
    def sleep(self):
        yield hold, self, 10
        yield put, self, self.energy, 30
        
    def entertain(self):
        yield hold, self, 5
         
    def socialize(self):    
        #Getting a new friend is inversely proportional to how many friends you currently have
        chances =10.0/(len(self.friends)+1)
        
        #If we get a friend, it takes us a little time to get to know them
        if chances > random():
            yield hold, self, 5
            new_friend = choice(self.world.people)
            if not new_friend in self.friends:
                self.friends.append(choice(self.world.people))
        else:
            #It takes less time to not find a friend. We give up pretty quickly
            yield hold, self, 2
            
    
    
def main():
    #We seed the RNG with a constant to make debugging simpler
    seed(12345)
    initialize()
    
    our_world = Gaia(population=100)
    
    activate(our_world, our_world.creation())
    
#   stepping(Globals)
    simulate(until=20)
    root=Tk()
    gu=SimGUI(root,consoleHeight=20)
    gu.mainloop()
    
if __name__ == "__main__":
    main()
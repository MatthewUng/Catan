from Resources import *
from fractions import *
import random 

yn = ['Y', 'N', 'y', 'n']

def prompt(p, error, allowed):
    """prompts the user until user returns valid input"""
    choice = raw_input(p)
    while choice not in allowed:
        print error
        #print choice
        #print allowed
        choice = raw_input(p)
    return choice

class Catan:

    def __init__(self):
        self.robbercount = Fraction(0)
        self.robberrate = Fraction(1, 7)
        self.robbed = list()

        self.resources = Resources("start")
        self.turn = 0
        self.players = self.resources.getplayers()
        self.curplayer = self.players[0]
        
        self.robbercount += Fraction(random.randint(0,3), 7)
        
    def next_turn(self):
        """undergo a turn"""
        print "*********************************************"
        print "\n{} to move".format(self.players[self.turn%len(self.players)])

        # check if robber activates
        self.robbercount += self.robberrate
        if self.robbercount >=1:
            self.robbercount -= 1
            print "Robber activates!!!!"
            self.moveRobber()

        # receiving resources
        print ""
        playerResources = self.resources.resource_turn()
        for pair in playerResources:
            print "{0} receives a {1}".format(pair[0], pair[1])

    def choosePlayer(self):
        """pick a player"""

        q = "pick a player:\n"
        error = "bad input.  Try again"
        return prompt(q, error, self.players)

    def chooseResource(self):
        """pick a resource and corresponding rate"""

        resource_prompt = "pick a resource:\n"
        error = "bad input. Try again"
        resource = prompt(resource_prompt, error, RESOURCES)

        rate_prompt = "What is the number?[2-12]\n"
        rate = prompt(rate_prompt, error, map(str, range(2, 13)))
        parse = toFraction(rate)

        return [resource, parse]

    def choosePlayerResource(self):
        """chooses both player and resource/rate"""
        player = self.choosePlayer()
        resource, rate = self.chooseResource()
        return [player, resource, rate]

    def moveRobber(self):
        """moves the robber and adjusts according"""

        def reset():
            """helper to reset past robbed resources"""
            for choice in self.robbed:
                player, resource, rate = choice
                self.resources.incRate(player, resource, rate)
                #self.rate[player][resource] += rate
            
            del self.robbed[:]

        if self.robbed:
            reset()

        while True:
            choice = prompt("Rob someone? \n", "try again!", yn)

            if choice.lower() == 'n':
                return 

            once = self.choosePlayerResource()
            self.robbed.append(once)
            player, resource, rate = once
            self.resources.decRate(player, resource, rate)

            decision = prompt("Continue? Y/N\n", "bad input. Try again.", yn)
            if decision.lower() == "n":
                return

    def build(self):
        """build more"""
        while True:
            player, resource, rate = self.choosePlayerResource()
            self.resources.incRate(player, resource, rate)

            #self.rate[player][resource] += Fraction(rate)
            
            more_prompt = "build more? Y/N"
            error = "bad input"
            more = prompt(more_prompt, error, yn)
            if more.lower() == 'n':
                return
        
    def getCommand(self):
        """gets a command"""
        possible = ["next", "knight", "build", "add", "remove", "debug"]
        command_prompt = "\nPossible commands: (next), (knight), (build)\n"
        error = "bad input. Try again"

        return prompt(command_prompt, error, possible)
    
    def run(self):
        """runs indefinitely"""
        while True:
            self.turn += 1
            print "\n\nCurrent turn {}".format(self.turn)
            self.next_turn()

            while True:
                next_turn = self.getCommand()
                if next_turn == "knight":
                    print "Moving robber with the knight"
                    self.moveRobber()
                
                elif next_turn == "build":
                    print "building..."
                    self.build()
                
                elif next_turn == "add":
                    print "adding..."
                    player, resource, rate = self.choosePlayerResource()
                    self.resources.incRate(player, resource, rate)

                elif next_turn == "remove":
                    print "removing..."
                    player, resource, rate = self.choosePlayerResource()
                    self.resources.decRate(player, resource, rate)

                elif next_turn == "debug":
                    self.debug()

                elif next_turn == "next":
                    break

                else:
                    print "error in run()"

    
    def debug(self):
        """debugging purposes"""
        self.resources.debug()

        print "robber stats"
        print "count: {}".format(self.robbercount)

if __name__ == "__main__":
    game = Catan()
    game.run()


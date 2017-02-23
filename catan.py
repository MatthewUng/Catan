from fractions import *
import random 

def toFraction(num):
    """converts an int/str [2-12] to corresponding fraction"""
    p = {2:1,
         3:2,
         4:3,
         5:4,
         6:5,
         7:6,
         8:5,
         9:4,
         10:3,
         11:2,
         12:1}
    if isinstance(num, str):
        if num.isdigit():
            num = int(num)
        else:
            print "error in toFraction"
    return Fraction(p[num], 36)

def dots(num):
    """returns the number of dots that correspond with the number"""
    d = {2:1,
         3:2,
         4:3,
         5:4,
         6:5,
         7:6,
         8:5,
         9:4,
         10:3,
         11:2,
         12:1}
    if isinstance(num, int):
        return d[num]

    elif isinstance(num, Fraction):
        for i in range(0, 50):
            if Fraction(i, 36) == num:
                return i

        print "error in dots(Fraction)"
        return

    else:
        print "problem in dots()"
        return

def prompt(p, error, allowed):
    """prompts the user until user returns valid input"""
    choice = raw_input(p)
    while choice not in allowed:
        print error
        choice = raw_input(p)
    return choice

class Catan:
    resources = ["wood", "brick", "wheat", "sheep", "rock"]

    def __init__(self):
        self.players = list()
        self.count = dict()
        self.rate = dict()

        self.robbercount = Fraction(0)
        self.robberrate = Fraction(1, 7)
        self.robbed = list()

        self.turn = 0
        self.curplayer = None
        
    def initGame(self):
        """initializes robber count and reads input file"""
        self.robbercount += Fraction(random.randint(0,3), 7)

        with open("start", "r") as f:
            f.readline()
            player = None
            for line in f:
                temp = line.split()
                if not temp:
                    continue

                elif len(temp) == 1:
                    player = temp[0]
                    if not self.curplayer:
                        self.curplayer = player

                    self.players.append(player)
                    self.rate[player] = dict()
                    self.count[player] = dict()

                    for resource in Catan.resources:
                        self.count[player][resource] = 0
                        self.rate[player][resource] = Fraction(0)

                elif temp[0] in Catan.resources and temp[1].isdigit():
                    self.startRate(player, temp[0], int(temp[1]))
                    

    def startRate(self, player, resource, rate):
        """returns start rate"""
        #rate is number [2-12]
        #0,0,2,6,1
        offset = {5:0,
                  4:0,
                  3:2,
                  2:6,
                  1:1}

        frac = toFraction(rate)
        self.rate[player][resource] += frac

        if rate > 6:
            self.count[player][resource] += Fraction(frac.denominator, 
                                    frac.numerator) * Fraction(1,2)* frac
        
        self.count[player][resource] += offset[dots(rate)] * frac

    def incRate(self, player, resource, rate):
        """increment the rate of a resource for a player"""
        if isinstance(rate, int):
            rate = toFraction(rate)

        self.rate[player][resource] += rate

    def decRate(self, player, resource, rate):
        """decrement the rate of a resource for a player"""
        if isinstance(rate, int):
            rate = toFraction(rate)

        self.rate[player][resource] -= rate

    def nextturn(self):
        """undergo a turn"""
        print "*********************************************"
        print "\n{} to move".format(self.players[self.turn%len(self.players)])
        self.robbercount += self.robberrate
        if self.robbercount >=1:
            self.robbercount -= 1
            print "Robber activates!"
            self.moveRobber()

        for player, value in self.rate.items():
            for resource, rate in value.items():
                self.count[player][resource] += rate
        
        print ""
        for player, d in self.count.items():
            for resource, count in d.items():
                while d[resource] > 1:
                    print "{0} receives a {1}".format(player, resource)
                    self.count[player][resource] -= 1
                    #print self.count[player][resource]

    def choosePlayer(self):
        """pick a player"""
        player = raw_input("pick a player:\n")
        while player not in self.players:
            print "bad input"
            player = raw_input("pick a player:\n")
        return player
        
    def chooseResource(self):
        """pick a resource and corresponding rate"""
        resource = raw_input("pick a resource:\n")
        while resource not in Catan.resources:
            print "bad input"
            resource = raw_input("pick a resource:\n")

        rate = raw_input("What is the number?[2-12]\n")
        while not rate.isdigit() or int(rate)<2 or int(rate)>12:
            print "bad input"
            rate = raw_input("What is the number?\n")

        parse = Fraction(rate)
        return [resource,rate]

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
                self.rate[player][resource] += rate
            
            del self.robbed[:]

        if self.robbed:
            reset()

        while True:
            choice = prompt("Rob someone? \n", "try again!", ['Y', 'y', 'N', 'n'])

            if choice.lower() == 'n':
                return 

            once = self.choosePlayerResource()
            self.robbed.append(once)
            player, resource, rate = once
            self.rate[player][resource] -= Fraction(rate)

            decision = raw_input("Continue? Y/N\n")
            while decision != "Y" and decision != "N":
                print "bad input"
                decision = raw_input("Continue? Y/N\n")
            if decision == "N":
                return

    def build(self):
        """build more"""
        player, resource, rate = self.choosePlayerResource()
        self.rate[player][resource] += Fraction(rate)

    def getCommand(self):
        """gets a command"""
        possible = ["next", "knight", "build", "add", "remove", "debug"]
        print "\nPossible commands: (next), (knight), (build)"
        command = raw_input()
        while command not in possible:
            print "bad input"
            print "\nPossible commands: (next), (knight), (build)"
            command = raw_input()

        return command
    
    def run(self):
        """runs indefinitely"""
        while True:
            self.turn += 1
            print "\n\nCurrent turn {}".format(self.turn)
            self.nextturn()

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
                    self.incRate(player, resource, rate)

                elif next_turn == "remove":
                    print "removing..."
                    player, resource, rate = self.choosePlayerResource()
                    self.decRate(player, resource, rate)

                elif next_turn == "debug":
                    self.debug()

                elif next_turn == "next":
                    break

                else:
                    print "error in run()"

    
    def debug(self):
        """debugging purposes"""
        print self.players
        print "rates:(dots)\n"
        for player, rate_dic in self.rate.items():
            print player
            for resource, rate in rate_dic.items():
                print resource, dots(rate)
            print ""

        print "counts(fraction):\n"
        for player, count_dic in self.count.items():
            print player
            for resource, count in count_dic.items():
                print resource, count
            print ""

        print "robber stats"
        print "count: {}".format(self.robbercount)

if __name__ == "__main__":
    game = Catan()
    game.initGame()
    game.run()


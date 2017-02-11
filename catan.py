from fractions import *
import random 

def toFraction(num):
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
    return Fraction(p[num], 36)

def dots(num):
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
        for i in range(1, 7):
            if Fraction(i, 36) == num:
                return i

        print "error in dots(Fraction)"
        return

    else:
        print "problem in dots()"
        return

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
        #0,0,2,6,1
        offset = {5:0,
                  4:0,
                  3:2,
                  2:6,
                  1:1}

        rate = toFraction(rate)
        self.rate[player][resource] += rate

        if rate > 6:
            out += Fraction(temp.denominator,temp.numerator) * Fraction(1,2)* temp
        
        self.count[player][resource] += offset[dots(rate)] * rate

    def incRate(self, player, resource, rate):
        if isinstance(rate, int):
            rate = toFraction(rate)

        self.rate[player][resource] += rate

    def decRate(self, player, resource, rate):
        if isinstance(rate, int):
            rate = toFraction(rate)

        self.rate[player][resource] -= rate

    def turn(self):
        print "{} to move".format(self.players[self.turn])
        self.robbercount += self.robberrate
        if self.robbercount >=1:
            self.robbercount -= 1
            print "Robber activates!"
            self.moveRobber()

        for player, value in self.rate.items():
            for resource, rate in value.items():
                self.count[player][resource] += rate
        
        for player, d in self.count.items():
            for resource, count in d.items():
                while count > 1:
                    print "{0} receives a {1}".format(player, resource)
                    count -= 1

    def choosePlayer(self):
        player = raw_input("pick a player:\n")
        while player not in self.players:
            print "bad input"
            player = raw_input("pick a player:\n")
        return player
        
    def chooseResource(self):
        resource = raw_input("pick a resource:\n")
        while resource not in Catan.resources:
            print "bad input"
            resource = raw_input("pick a resource:\n")

        rate = raw_input("What is the number?\n")
        while not rate.isdigit() or int(rate)<2 or int(rate)>12:
            print "bad input"
            rate = raw_input("What is the number?\n")

        parse = Fraction(rate)
        return [resource,rate]

    def choosePlayerResource(self):
        player = self.chooseplayer()
        resource, rate = self.chooseResource()
        return [player, resource, rate]

    def moveRobber(self):
        def reset():
            for choice in self.robbed:
                player, resource, rate = choice
                self.rate[player][resource] += rate
            
            del self.robbed[:]

        if self.robbed:
            reset()

        while True:
            once = self.choosePlayerResource()
            self.robbed.append(once)
            player, resource, rate = once
            self.rate[player][resource] -= rate

            decision = raw_input("Continue? Y/N\n")
            while decision != "Y" and decision != "N":
                print "bad input"
                decision = raw_input("Continue? Y/N\n")
            if decision == "N":
                break

    def build(self):
        player, resource, rate = self.choosePlayerResource()
        self.rate[player][resource] += rate   

    def getCommand(self):
        possible = ["next", "knight", "build", "add", "remove", "debug"]
        print "Possible commands: (next), (knight), (build)"
        command = raw_input()
        while command not in possible:
            print "bad input"
            print "Possible commands: (next), (knight), (build)"
            command = raw_input()

        return command
    
    def run(self):

        while True:
            self.turn += 1
            print "Current turn {}".format(self.turn)
            self.turn()

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
                    self.debug

                elif next_turn == "next":
                    break

                else:
                    print "error in run()"

    

    def debug(self):
        print self.players
        print "rates:\n"
        for player, rate_dic in self.rate.items():
            print player
            for resource, rate in rate_dic.items():
                print resource, rate
            print ""

        print "counts:\n"
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
    game.debug()


from fractions import *

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

class Catan:
    resources = ["wood", "brick", "wheat", "sheep", "rock"]

    def __init__(self):
        self.players = list()
        self.count = dict()
        self.rate = dict()

        self.initPlayers()
        self.turn = 0
        
    def initGame(self):
        for player in self.players:
            print "\n{} to choose".format(player)
            num = raw_input("how many adjacent resources?\n")

            while not num.isdigit() or int(num) <0 or int(num) > 3 or int(num) == 7:
                print "incorrect input.  Try again"
                num = raw_input("how many adjacent resources?\n")

            for _ in range(int(num)):
                resource = raw_input("pick a resource:\n").lower().strip()

                while resource not in Catan.resources:
                    print "Not a valid resource.  Try again"
                    resource = raw_input("pick a resource:\n").lower().strip()
                
                rate = raw_input("resource rate:\n").lower().strip()

                while not rate.isdigit() or int(rate)<2 or int(rate) >12:
                    rate = raw_input("resource rate:\n").lower().strip()

                self.count[player][resource] += toFraction(int(rate))

        for player in self.players[::-1]:
            print "\n{} to choose".format(player)
            num = raw_input("\nhow many adjacent resources?\n")

            while not num.isdigit() or int(num) <0 or int(num) > 3 or int(num)==7:
                print "incorrect input.  Try again"
                num = raw_input("how many adjacent resources?\n")

            for _ in range(int(num)):
                resource = raw_input("pick a resource:\n").lower().strip()

                while resource not in Catan.resources:
                    print "Not a valid resource.  Try again"
                    resource = raw_input("pick a resource:\n").lower().strip()
                
                rate = raw_input("resource rate:\n").lower().strip()

                while not rate.isdigit() or int(rate)<2 or int(rate) >12:
                    rate = raw_input("resource rate:\n").lower().strip()

                self.count[player][resource] += toFraction(int(rate))

    def initPlayers(self):
        with open("players", 'r') as f:
            f.readline()
            for line in f:
                self.players.append(line.strip())

        if len(self.players) <3 or len(self.players) > 4:
            print "not enough players"
            exit()

        for player in self.players:
            self.count[player] = dict()
            self.rate[player] = dict()

            for resource in Catan.resources:
                self.count[player][resource] = Fraction(0)
                self.rate[player][resource] = Fraction(0)
    
    def next(self):
        print "{} to move".format(self.players[self.turn])

        for player, value in self.rate.items():
            for resource, rate in value.items():
                self.count[player][resource] += rate
        
        for player, d in self.count.items():
            for resource, count in d.items():
                while count > 1:
                    print "{0} receives a {1}".format(player, resource)
                    count -= 1

        
    def debug(self):
        print self.players
        print "rates:"
        for key, value in self.rate:
            print key
            print value
        for key, value in self.count:
            print key
            print value


if __name__ == "__main__":
    game = Catan()
    game.initGame()
    game.debug()


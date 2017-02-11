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

        self.turn = 0
        
    def initGame(self):
        with open("start", "r") as f:
            f.readline()
            player = None
            for line in f:
                temp = line.split()
                if not temp:
                    continue

                elif len(temp) == 1:
                    player = temp[0]
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

        out = 0
        rate = toFraction(rate)
        try:
            self.rate[player][resource] += rate

        except:
            print self.rate[player]

        if rate > 6:
            out += Fraction(temp.denominator,temp.numerator) * Fraction(1,2)* temp
        
        self.count[player][resource] += offset[dots(rate)] * rate

    def incRate(self, player, resource, rate):
        pass
    
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

        
    def test(self):
        self.players = ["matt", "jp", "ansel"]


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

if __name__ == "__main__":
    game = Catan()
    game.initGame()
    game.debug()


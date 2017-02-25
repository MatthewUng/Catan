from fractions import *

RESOURCES = ['wood', 'wheat', 'rock', 'sheep', 'brick']

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

    if isinstance(num, Fraction):
        return num

    elif isinstance(num, str):
        if num.isdigit():
            num = int(num)
        else:
            print "error in toFraction\n input string in not number"
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
        for i in range(0, 99):
            if Fraction(i, 36) == num:
                return i

        print "error in dots(Fraction)"
        return

    else:
        print "problem in dots()"
        return

class Resources:
    def __init__(self, filename):
        self._players = list()
        self._count = dict()
        self._rates = dict()
        self.start(filename)
        
    def start(self,fname):
        with open(fname, "r") as f:
            f.readline()
            for line in f:
                temp = line.split()
                if not temp:
                    continue

                #line is a player
                elif len(temp) == 1:
                    player = temp[0]

                    self._players.append(player)
                    self._rates[player] = dict()
                    self._count[player] = dict()

                    for resource in RESOURCES:
                        self._count[player][resource] = 0
                        self._rates[player][resource] = Fraction(0)

                #input is resource/rate
                elif temp[0] in RESOURCES and temp[1].isdigit():
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
        self._rates[player][resource] += frac

        if rate > 6:
            self._count[player][resource] += Fraction(frac.denominator, 
                                    frac.numerator) * Fraction(1,2)* frac
        
        self._count[player][resource] += offset[dots(rate)] * frac
        if self._count[player][resource] >= 1:
            self._count[player][resource] -= 1

    def resource_turn(self):
        """returns list of resources that users obtain"""
        out = list()

        # increment counts
        for player, value in self._rates.items():
            for resource, rate in value.items():
                self._count[player][resource] += rate
        
        # returning resources
        for player, value in self._count.items():
            for resource, rate in value.items():
                while value[resource] >=1:
                    out.append([player, resource])
                    self._count[player][resource] -= 1
        return out

    def incRate(self, player, resource, rate):
        """increment the rate of a resource for a player"""
        if isinstance(rate, int):
            rate = toFraction(rate)

        self._rates[player][resource] += rate
    
    def incRateDot(self, player, resource, dot):
        """increment the rate based on dots"""
        self._rates[player][resource] += Fraction(dot, 36)

    def decRateDot(self, player, resource, dot):
        """increment the rate based on dots"""
        self._rates[player][resource] -= Fraction(dot, 36)

    def decRate(self, player, resource, rate):
        """decrement the rate of a resource for a player"""

        if isinstance(rate, int):
            rate = toFraction(rate)

        self._rates[player][resource] -= rate

    def getplayers(self):
        return self._players

    def debug(self):
        "debugging purposes"

        print "{} players in game:".format(len(self._players))
        for player in self._players:
            print player

        print "\nrates(dots):\n"
        for player, d in self._rates.items():
            print player
            for resource, rate in d.items():
                print resource, dots(rate)
            print ""

        print "counts(fraction):\n"
        for player, d in self._count.items():
            print player
            for resource, count in d.items():
                print resource, count
            print ""



if __name__ == "__main__":
    test = Resources("start")
    test.debug()

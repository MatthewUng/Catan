import math

def fill(n1,n2,n3,n4,n5):
    out = [0 for _ in range(36)]

    h1 = 3
    h2 = 4
    h3 = 6
    h4 = 9
    h5 = 18

    # first half
    for i in range(5):
        out[(int(n1+math.floor(7.2*i)))%36] += 1
    for i in range(4):
        out[(n2+9*i) % 36] += 1
    for i in range(3):
        out[(n3+12*i)%36] += 1
    for i in range(2):
        out[(n4+18*i)%36] += 1
    out[n5%36] += 1


    # second half
    for i in range(5):
        out[(int(n1+h1+math.floor(7.2*i)))%36] += 1
    for i in range(4):
        out[(n2+h2+9*i) % 36] += 1
    for i in range(3):
        out[(n3+h3+12*i)%36] += 1
    for i in range(2):
        out[(n4+h4+18*i)%36] += 1
    out[(n5+h5)%36] += 1

    return out

def fill2(n1,n2,n3,n4,n5,n6,n7,n8,n9,n10):
    out = [0 for _ in range(36)]

    # first half
    for i in range(5):
        out[(int(n1+math.floor(7.2*i)))%36] += 1
    for i in range(4):
        out[(n2+9*i) % 36] += 1
    for i in range(3):
        out[(n3+12*i)%36] += 1
    for i in range(2):
        out[(n4+18*i)%36] += 1
    out[n5] += 1


    # second half
    for i in range(5):
        out[(int(n6+math.floor(7.2*i)))%36] += 1
    for i in range(4):
        out[(n7+9*i) % 36] += 1
    for i in range(3):
        out[(n8+12*i)%36] += 1
    for i in range(2):
        out[(n9+18*i)%36] += 1
    out[n10] += 1

    return out
   
def test1():
    indices = [0,0,0,0,0]
    range_list = range(20)
    m = 9999999999999999999

    for n1 in range_list:
        for n2 in range_list:
            for n3 in range_list:
                for n4 in range_list:
                    for n5 in range_list:
                        l = fill(n1,n2,n3,n4,n5)
                        if minimize(l)<m:
                            indices = [n1,n2,n3,n4,n5]
                            m = minimize(l)
        print 'n1:', n1
    print "minimal indices: ", indices
    print "m: ", m
    return [indices, m]

def test2():
    indices = [0,0,0,0,0,0,0,0,0,0]
    m = 999999999999999
    range_list = range(5)
    for n1 in range_list:
        for n2 in range_list:
            for n3 in range_list:
                for n4 in range_list:
                    for n5 in range_list:
                        for n6 in range_list:
                            for n7 in range_list:
                                for n8 in range_list:
                                    for n9 in range_list:
                                        for n10 in range_list:
                                            l = fill2(n1,n2,n3,n4,n5,n6,n7,n8,n9,n10)
                                            if minimize(l) < m:
                                                indices = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10]
                                                m = minimize(l)
        print 'n1:', n1
    print "minimal indices: ", indices
    print "m: ", m
    return [indices, m]


def minimize(l):
    out = 0
    for value in l:
        out += value**value
    return out

if __name__ == "__main__":
    out = test1()
    l = fill(*out[0])
    print l[0:12]
    print l[12:24]
    print l[24:36]


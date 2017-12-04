import math

def entropy(l):
    if l:
        c_high = len(l[0]) - 1
        print c_high, "c_high"
        sum1 = len(l)
        s1 = 0
        attrlist1 = [0] * c_high
        for i in l:
            attrlist1[i[-1]] += 1
        for i in range(0,c_high):
            # print attrlist1[i]/sum1
            if attrlist1[i]:
                s1 += -((float(attrlist1[i])/sum1) * math.log(float(attrlist1[i])/sum1,2))
        return (s1, sum1)
    else:
        return (0,0)

def info_gain_list(l,r):
    s = len(l) + len(r)
    # print r
    # print l
    # print attrlist2

    s1 = 0
    s2 = 0
    s1, sum1 = entropy(l)
    s2, sum2 = entropy(r)
    P, sum0 = entropy(l+r)
    # print P, sum0, "Parent"
    gain = P - (s1*(sum1/float(s))) - (s2*(sum2/float(s)))
    # print gain, (s1*(sum1/float(s))), (s2*(sum2/float(s))), "="
    return gain

def separate(examples, a, thresh):
    left = []
    right = []

    for i in range(len(examples)):
        if examples[i][a] < thresh:
            left.append(examples[i])
        else:
            right.append(examples[i])
    return (left,right)

def info_gain(examples, a, thresh):
    gain = 0
    left, right = separate(examples, a, thresh)
    # print left
    # print right
    return info_gain_list(left,right)

def sameclass(examples):
    c = examples[0][-1]
    for i in range(1, len(examples)):
        if c != examples[i][-1]:
            return False
        else:
            c = examples[i][-1]
    return True

def DISTRIBUTION(examples,classnuml,classnum):
    a = 0
    if classnuml == 1:
        a = 1
    # print classnuml, classnum, c_high
    distlist = [0] * (classnum + a + 1)
    # print distlist
    s = len(examples)
    res = []
    for i in examples:
        # print i[-1]
        distlist[i[-1]] += 1
    for i in distlist:
        res.append(i/float(s))
    # print distlist
    # print res
    return res

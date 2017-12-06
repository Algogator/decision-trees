    # data is dist of classes not attributes!!!!!!!!!!
    # print len(tree)
def avg_dist(data):

    fin = []
    for y in range(len(data[0])):
        sum = 0
        for x in data:
            sum += x[y]
        # print sum, len(data)
        fin.append(sum/len(data))
    return fin

def pickmax(dist):
    m = max(dist)
    res = []
    for i in range(len(dist)):
        if dist[i] == m:
            res.append(i)
    return res

# avg_dist([[1,2],[1,2],[1,2]])

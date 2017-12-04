from sys import argv,setrecursionlimit
import math
import tree as t
import pdb
import random

# 20 points: Correct processing of the optimized option. Identifying and choosing, for each node, the (feature, threshold) pair with the highest information gain for that node, and correctly computing that information gain.
# 10 points: Correct processing of the randomized option. In other words, identifying and choosing, for each node, an appropriate (feature, threshold) pair, where the feature is chosen randomly, and the threshold maximizes the information gain for that feature,
# 10 points: Correctly directing training objects to the left or right child of each node, depending on the (threshold, value) pair used at that node.
# 10 points: Correct application of pruning, as specified in the slides (if any .
# 15 points: Correctly applying decision trees to classify test objects.
# 15 points: Correctly applying decision forests to classify test objects.
# 20 points: Following the specifications in producing the required output.

training_file = argv[1]
test_file = argv[2]
option = argv[3]

f = open(training_file,'r')
message = f.read()
f.close()
m = message.split('\n')
res = []
classnum = 0
classnuml = 1
for i in m:
    y = i.split()
    if y:
        res.append([])
        for x in y:
            res[-1].append(int(x))
        if res[-1][-1] > classnum:
            classnum = res[-1][-1]
        if res[-1][-1] < classnuml:
            classnuml = res[-1][-1]


#find classes
c_high = len(res[0]) - 1
# print(res)

# with open('training_data.txt') as f:
#     content = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# content = [x.lstrip().strip('\n').split("     ") for x in content]
# results = []
# for r in content:
#     results.append(list(map(int, r)))


# print training_file, test_file, option

def select_col(examples, a):
    res = []
    # print examples[-1]
    for i in examples:
        # print i,i[a]
        res.append(i[a])
    # print res
    return res

def entropy(l):
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



def choose_attribute(examples, attr):
    max_gain = -1
    best_attr = -1
    best_thresh = -1
    # print attr, examples
    if option == "optimized":
        for a in attr:
            #attribute _values is the array containing the values of all examples for attribute A
            # print a
            attr_val = select_col(examples, a)
            l  = min(attr_val)
            m = max(attr_val)
            for k in range(1,51):
                # print k
                thresh = l + ((k*(m-l))/51)
    #           For each threshold, measure the information gain attained on these
    #           examples using that combination of attribute A and threshold.
                gain = info_gain(examples, a, thresh)
                # print gain
                if gain > max_gain:
                    max_gain = gain
                    best_attr = a
                    best_thresh = thresh
    elif option == "randomized":
        a = random.choice(attr)
        attr_val = select_col(examples, a)
        l  = min(attr_val)
        m = max(attr_val)
        for k in range(1,51):
            # print k
            thresh = l + ((k*(m-l))/51)
    #           For each threshold, measure the information gain attained on these
    #           examples using that combination of attribute A and threshold.
            gain = info_gain(examples, a, thresh)
            # print gain
            if gain > max_gain:
                max_gain = gain
                best_attr = a
                best_thresh = thresh

        # print best_attr, best_thresh, "@@@@"
    return(best_attr,best_thresh,max_gain)



def sameclass(examples):
    c = examples[0][-1]
    for i in range(1, len(examples)):
        if c != examples[i][-1]:
            return False
        else:
            c = examples[i][-1]
    return True

def DISTRIBUTION(examples):
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

def DTL(examples, attributes, default):
    # print examples
    # print 1
    # print "===="
    if not examples:
    # However, notice the highlighted line, that says that if there are no examples, we should return default. What does that mean?
    # It means we should return a leaf node, that outputs class default.
    # If there are no examples, obviously we need to create a leaf node.
    # The default argument tells us what class to store at the leaf node.

        m = max(default)
        ind = [i for i, j in enumerate(default) if j == m]
        # print ind
        return t.Node(classtype=random.choice(ind),gain = 0)

    # if len(examples) < 2:
    #     return None

    elif sameclass(examples):
        # if len(examples) > 2:
        return t.Node(classtype=examples[0][-1],gain = 0)
        # else:
        #     return None

    else:
        best_attribute, best_threshold, max_gain = choose_attribute(examples, attributes)
        # print best_attribute, best_threshold
        # tree = a new decision tree with root test (best_attribute, best_threshold)
        tree = t.Node(best_attribute=best_attribute, best_threshold=best_threshold, gain = max_gain)
        # examples_left = {elements of examples with best_attribute < threshold}
        # examples_right = {elements of examples with best_attribute < threshold}
        # print best_attribute, best_threshold
        examples_left, examples_right = separate(examples, best_attribute, best_threshold)
        # print examples_left
        # print examples_right
        tree.left_child = DTL(examples_left, attributes, DISTRIBUTION(examples))
        # if not tree.left_child:
        #     tree.left_child = t.Node(classtype=examples[0][-1],gain = 0)
        tree.right_child = DTL(examples_right, attributes, DISTRIBUTION(examples))
        # if not tree.right_child:
        #     tree.right_child = t.Node(classtype=examples[0][-1],gain = 0)
        return tree

def classify(example,node):
    if node:
        if example[node.best_attribute] < node.best_threshold:
            if node.left_child:
                return classify(example, node.left_child)
            else:
                # print node.classtype, "left"
                return node.classtype
        else:
            if node.right_child:
                return classify(example, node.right_child)
            else:
                # print node.classtype, "right"
                return node.classtype

attr = []
for i in range(c_high):
    attr.append(i)
tree = DTL(res,attr,[])
Mtree = t.BinaryTree(tree)
Mtree.preorder_print(1,start = tree)

f = open(test_file,'r')
message = f.read()
f.close()
m = message.split('\n')
res = []
for i in m:
    res.append([])
    y = i.split()
    for x in y:
        res[-1].append(int(x))
del res[-1]

# print classify(res[3],tree)
overall_accuracy = 0
for i in range(len(res)):
    predicted_class = classify(res[i],tree)
    accuracy = 0
    if predicted_class == res[i][-1]:
        accuracy = 1
    overall_accuracy += accuracy
#If there were ties in your classification result, and the correct class was one of the classes that tied for best, the accuracy is 1 divided by the number of classes that tied for best.
# If there were ties in your classification result, and the correct class was NOT one of the classes that tied for best, the accuracy is 0.
    # print "ID="+str(i)+", predicted="+str(predicted_class)+", true="+str(res[i][-1])+", accuracy="+str(accuracy)

# overall classification accuracy, which is defined as the average of the classification accuracies you printed out for each test object
print 100 * (overall_accuracy/float(len(res)))

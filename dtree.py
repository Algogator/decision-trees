from sys import argv
import tree as t
import pdb
import random
from file_ops import preprocess
from info import separate, DISTRIBUTION, sameclass,  info_gain

# 20 points: Correct processing of the optimized option. Identifying and choosing, for each node, the (feature, threshold) pair with the highest information gain for that node, and correctly computing that information gain.
# 10 points: Correct processing of the randomized option. In other words, identifying and choosing, for each node, an appropriate (feature, threshold) pair, where the feature is chosen randomly, and the threshold maximizes the information gain for that feature,
# 10 points: Correctly directing training objects to the left or right child of each node, depending on the (threshold, value) pair used at that node.
# 10 points: Correct application of pruning, as specified in the slides (if any .
# 15 points: Correctly applying decision trees to classify test objects.
# 15 points: Correctly applying decision forests to classify test objects.

def select_col(examples, a):
    res = []
    # print examples[-1]
    for i in examples:
        # print i,i[a]
        res.append(i[a])
    # print res
    return res

def choose_attribute(examples, attr):
    global max_gain
    global best_attr
    global best_thresh
    max_gain = -1
    best_attr = -1
    best_thresh = -1
    # print attr, examples
    def thresh_optimize(a):
        global max_gain
        global best_attr
        global best_thresh
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
    if option == "optimized":
        for a in attr:
            thresh_optimize(a)
            #attribute _values is the array containing the values of all examples for attribute A
            # print a
    elif option == "randomized":
        a = random.choice(attr)
        thresh_optimize(a)

    elif option == "forest3":
        a = random.choice(attr)
        thresh_optimize(a)

    elif option == "forest15":
        a = random.choice(attr)
        thresh_optimize(a)

        # print best_attr, best_thresh, "@@@@"
    return(best_attr,best_thresh,max_gain)

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
        tree.left_child = DTL(examples_left, attributes, DISTRIBUTION(examples,classnuml,classnum))
        # if not tree.left_child:
        #     tree.left_child = t.Node(classtype=examples[0][-1],gain = 0)
        tree.right_child = DTL(examples_right, attributes, DISTRIBUTION(examples,classnuml,classnum))
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

training_file = argv[1]
test_file = argv[2]
option = argv[3]



res, classnum, classnuml = preprocess(training_file)

#find classes
c_high = len(res[0]) - 1
# print(res)

attr = []
for i in range(c_high):
    attr.append(i)
if option == "forest3":
    trees = []
    Btrees = []
    for i in range(1,4):
        trees.append(DTL(res,attr,[]))
    for i in trees:
        Btrees.append(t.BinaryTree(i))
    for i in range(1, len(Btrees) + 1):
        Btrees[i-1].preorder_print(i, start=trees[i-1])
elif option == "forest15":
    pass
else:
    tree = DTL(res,attr,[])
    Mtree = t.BinaryTree(tree)
    Mtree.preorder_print(1,start = tree)
    res, classnum, classnuml = preprocess(test_file)

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
print "classification accuracy=",100 * (overall_accuracy/float(len(res)))

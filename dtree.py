from sys import argv
import tree as t
import pdb
from helpers import avg_dist, pickmax
from classify import classify
import random
from file_ops import preprocess
from info import separate, DISTRIBUTION, sameclass,  info_gain
from choose_attrib import choose_attribute

def DTL(examples, attributes, default):
    if not examples:
        return t.Node(dist=default,gain = 0)

    # if len(examples) < 2:
    #     return None

    elif sameclass(examples):
        # if len(examples) > 2:
        # print examples,"=", default, classnuml, classnum
        # return t.Node(dist=examples[0][-1],gain = 0)
        return t.Node(dist=DISTRIBUTION(examples,classnuml,classnum),gain = 0)
        # else:
        #     return None

    else:
        best_attribute, best_threshold, max_gain = choose_attribute(examples, attributes,option)
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



training_file = argv[1]
test_file = argv[2]
option = argv[3]

res, classnum, classnuml = preprocess(training_file)
# print classnuml, classnum, res
#find classes
c_high = len(res[0]) - 1
# print(res)

attr = []
for i in range(c_high):
    attr.append(i)
if option == "forest3":
    trees = []
    Btrees = []
    for i in range(3):
        trees.append(DTL(res,attr,DISTRIBUTION(res,classnuml, classnum)))
    for i in trees:
        Btrees.append(t.BinaryTree(i))
    for i in range(len(Btrees)):
        Btrees[i].preorder_print(i+1, start=trees[i])
    tree = trees
elif option == "forest15":
    trees = []
    Btrees = []
    for i in range(1,16):
        trees.append(DTL(res,attr,DISTRIBUTION(res,classnuml, classnum)))
    for i in trees:
        Btrees.append(t.BinaryTree(i))
    # for i in range(1, len(Btrees) + 1):
    #     Btrees[i-1].preorder_print(i, start=trees[i-1])
    tree = trees
else:
    tree = []
    tree.append(DTL(res,attr,DISTRIBUTION(res,classnuml, classnum)))
    Mtree = t.BinaryTree(tree[0])
    # Mtree.preorder_print(1,start = tree[0])

res, classnum, classnuml = preprocess(test_file)
# print classify(res[3],tree)

overall_accuracy = 0
# print res[0]
# pdb.set_trace()
for i in range(len(res)):
    data = []
    for t in tree:
        # print res[i]
        data.append(classify(res[i],t))
    accuracy = 0
    fin = avg_dist(data)
    pred_classes = pickmax(fin)

    if res[i][-1] in pred_classes :
        accuracy = 1/len(pred_classes)
    # else:
    #     print fin, pred_classes, res[i][-1]
    overall_accuracy += accuracy
#If there were ties in your classificatiplainon result, and the correct class was one of the classes that tied for best, the accuracy is 1 divided by the number of classes that tied for best.

    # print "ID="+str(i)+", predicted="+str(predicted_class)+", true="+str(res[i][-1])+", accuracy="+str(accuracy)

# overall classification accuracy, which is defined as the average of the classification accuracies you printed out for each test object
print "classification accuracy=",100 * (overall_accuracy/float(len(res)))

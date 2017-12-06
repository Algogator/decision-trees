from sys import argv
import tree as t
import pdb
from helpers import avg_dist, pickmax
from classify import classify
import random
from file_ops import preprocess
from info import separate, DISTRIBUTION, sameclass,  info_gain
from choose_attrib import choose_attribute
import g_vars


def DTL(examples, attributes, default):
    if not examples:
        return t.Node(dist=default, gain=0)

    elif sameclass(examples):
        return t.Node(dist=DISTRIBUTION(examples), gain=0)

    else:
        best_attribute, best_threshold, max_gain = choose_attribute(
            examples, attributes)
        tree = t.Node(best_attribute=best_attribute,
                      best_threshold=best_threshold, gain=max_gain)
        examples_left, examples_right = separate(
            examples, best_attribute, best_threshold)
        # Pruning
        if len(examples_left) < 50 or len(examples_right) < 50:
            tree.dist = DISTRIBUTION(examples)
            tree.best_threshold = -1
            tree.best_attribute = -1
            tree.gain = 0

        else:
            tree.left_child = DTL(examples_left, attributes,
                                  DISTRIBUTION(examples))
            tree.right_child = DTL(examples_right, attributes,
                                   DISTRIBUTION(examples))

        return tree


training_file = argv[1]
test_file = argv[2]
option = argv[3]

res, classnum, classnuml = preprocess(training_file)
# No of attributes
c_high = len(res[0]) - 1
g_vars.init(classnum + 1, classnuml, c_high, option)
attr = []
for i in range(c_high):
    attr.append(i)
# print attr
if option == "forest3":
    trees = []
    Btrees = []
    for i in range(3):
        trees.append(DTL(res, attr, DISTRIBUTION(res)))
    for i in trees:
        Btrees.append(t.BinaryTree(i))
    for i in range(len(Btrees)):
        Btrees[i].preorder_print(i + 1, start=trees[i])
    tree = trees
elif option == "forest15":
    trees = []
    Btrees = []
    for i in range(15):
        trees.append(DTL(res, attr, DISTRIBUTION(res)))
    for i in trees:
        Btrees.append(t.BinaryTree(i))
    tree = trees
else:
    tree = []
    tree.append(DTL(res, attr, DISTRIBUTION(res)))
    Mtree = t.BinaryTree(tree[0])
    Mtree.preorder_print(1, start=tree[0])

res_test, _, _ = preprocess(test_file)

overall_accuracy = 0
for i in range(len(res_test)):
    data = []
    for t in tree:
        data.append(classify(res_test[i], t))
    accuracy = 0
    fin = avg_dist(data)
    pred_classes = pickmax(fin)
    # pdb.set_trace()
    if res_test[i][-1] in pred_classes:
        accuracy = 1 / len(pred_classes)
    overall_accuracy += accuracy
# If there were ties in your classificatiplainon result, and the correct
# class was one of the classes that tied for best, the accuracy is 1
# divided by the number of classes that tied for best.

    print "ID="+str(i)+", predicted="+str(pred_classes)+", true="+str(res[i][-1])+", accuracy="+str(accuracy)

# overall classification accuracy, which is defined as the average of the
# classification accuracies you printed out for each test object
print "classification accuracy=", 100 * (overall_accuracy / float(len(res_test)))

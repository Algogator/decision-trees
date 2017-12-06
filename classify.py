def classify(example,node):
    # print example, node
    if node:
        if example[node.best_attribute] < node.best_threshold:
            if node.left_child:
                return classify(example, node.left_child)
            else:
                # print node.classtype, "left"
                # return node.classtype
                return node.dist
        else:
            if node.right_child:
                return classify(example, node.right_child)
            else:
                # res = pickmax()
                # print res, node.dist
                # print node.classtype, "right"
                # return node.classtype
                return node.dist

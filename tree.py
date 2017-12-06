class Node(object):
    def __init__(self, gain, best_attribute=-1, best_threshold=-1, dist=None):
        self.best_attribute = best_attribute
        self.best_threshold = best_threshold
        self.dist = dist
        self.gain = gain
        self.left_child = None
        self.right_child = None

class BinaryTree(object):
    def __init__(self, root):
        self.root = root
        # print root

    def search(self, find_val):
        return self.preorder_search(self.root, find_val)

    def print_tree(self):
        return self.preorder_print(self.root, "")[:-1]

    def preorder_search(self, start, find_val):
        if start:
            if(start.value == find_val):
                return True
            else:
                return self.preorder_search(start.left,find_val) or self.preorder_search(start.right,find_val)
        else:
            return False

    def preorder_print(self,tree,start,node_id=1):
        if start:
            q = []
            q.append(start)
            node_id = 0
            while q:
                elem = q.pop(0)
                node_id += 1
                print "tree="+str(tree)+", node="+str(node_id)+", feature="+str(elem.best_attribute)+", thr="+str(elem.best_threshold)+", gain="+str(elem.gain)
                # (str(start.value) + "-")
                if elem.left_child:
                    q.append(elem.left_child)
                if elem.right_child:
                    q.append(elem.right_child)



# # Set up tree
# tree = BinaryTree(1)
# tree.root.left = Node(2)
# tree.root.right = Node(3)
# tree.root.left.left = Node(4)
# tree.root.left.right = Node(5)
#
# # Test search
# # Should be True
# print tree.search(4)
# # Should be False
# print tree.search(6)
#
# # Test print_tree
# # Should be 1-2-4-5-3
# print tree.print_tree()

def b():
    # global max_gain
    # global best_attr
    # global best_thresh
    max_gain = -1
    best_attr = -1
    best_thresh = -1
    # print attr, examples
    def thresh_optimize():
        global max_gain
        global best_attr
        global best_thresh
        max_gain = -2
        best_attr = -2
        best_thresh = -2
    thresh_optimize()
    print max_gain

b()

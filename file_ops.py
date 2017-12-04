def preprocess(training_file):
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
    return(res, classnum, classnuml)

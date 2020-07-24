import Searcher
import os
from multiprocessing import Pool

# slicing rule structure
#{
#    rule: as per searcher,
#    key: key split on if search match,
#    specific: whether to run general match or specific match
#}


def slicing(file, rule):
    flag = False
    searchpattern = Searcher.searcher(rule['rule'])
    with open(file,"r") as f:
        data =f.read()
        if rule['specific']:
            if searchpattern.SpecificMatch(data):
                flag=True
        else:
            if searchpattern.IsMatch(data):
                flag=True
        if flag== True:            
             for x in slicebykeys(rule['key'],data):
                yield x

def slicebykeys(key, data):
    for datakey in data.keys():
        if datakey==key:
            if isinstance(data[datakey],list) or isinstance(data[datakey],tuple):
                for item in data[datakey]:
                    yield item
            elif isinstance(data[datakey],dict):
                for itemkey in data[datakey].keys():
                    yield data[datakey][itemkey]
            else:
                yield data[datakey]
        else:
            if isinstance(data[datakey],list) or isinstance(data[datakey],tuple):
                for item in data[datakey]:
                    for result in slicebykeys(key,item):
                        yield result
            elif isinstance(data[datakey],dict):
                for itemkey in data[datakey].keys():
                    for result in slicebykeys(key, data[datakey][itemkey]):
                        yield result

def slicewriter(file, rule,intermediatepath):
    count = 0
    for result in slicing(file, rule):
        with open(os.path.join(intermediatepath, str(count)+file),'w') as writer:
            writer.write(result)
        count= count+1

def Slicer(rules=[],poolsize=8):
    inputpath = os.path.abspath("../Input")
    intermediatepath = os.path.abspath("../Intermediate")
    with Pool(poolsize) as pool:
        for file in os.listdir(inputpath):
            if file.endswith('.json'):
                for rule in rules:
                    pool.apply_async(slicewriter, args=(file, rule, intermediatepath))
        
import unittest
import Slicer
import json
import os
import functools


def testdatawrapper (func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        #sample json chunk for testing purposes
        examplejson= """{"menu": {
      "id": "file",
      "value": "File",
      "popup": {
        "menuitem": [
          {"value": "New", "onclick": "CreateNewDoc()"},
          {"value": "Open", "onclick": "OpenDoc()"},
          {"value": "Close", "onclick": "CloseDoc()"}
        ]
      }
    }}"""
    
        examplejsondes=json.loads(examplejson)
            
        with open("Input/Test.json",'w') as testfile:
            json.dump(examplejsondes,testfile)
        results = func(*args, **kwargs)
        os.remove("Input/Test.json")
        return results
    return wrapper


class Test_SlicerTest(unittest.TestCase):
    
    @testdatawrapper
    def TestforExplicitErrors(self):
        Slicer.Slicer(rules=[{rule:"menuitem",key:"menuitem",specific:False}], poolsize=6, debug=True)
    

if __name__ == '__main__':
    unittest.main()

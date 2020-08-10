import unittest
import Slicer
import json
import os
import functools


def testdatawrapper (debug):
    if debug:
        print('debug enabled')
        print(os.getcwd())
    def funclayer(func):
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
            if debug==True:
                print(examplejsondes)
            with open("../Input/Test.json",'w') as testfile:
                json.dump(examplejsondes,testfile)
            if debug:
                print(os.listdir('../Input'))
            results = func( debug=debug, *args, **kwargs)
            if debug==True:
                print(results)
            return results
        return wrapper
    try:
        return funclayer
    except Exception as e:
        throw(e)
        if debug:
            print(e)
    finally:
        os.remove("../Input/Test.json")


class Test_SlicerTest(unittest.TestCase):
    
    @testdatawrapper(debug=True)
    def TestforExplicitErrors(self):
        Slicer.Slicer(rules=[{rule:"menuitem",key:"menuitem",specific:False}], poolsize=6)
        self.assertEqual(len([name for name in os.listdir('../Intermediate') if os.path.isfile(name)]),3)

if __name__ == '__main__':
    unittest.main()

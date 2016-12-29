#!/usr/bin/python3

import sys
import argparse
import importlib
from subprocess import call
from pyspark import SparkConf, SparkContext

def main():


    
    # Sources
    parser = argparse.ArgumentParser(description='Spark Command Line Tool allows one to have set up a Spark job using a command line.\
                                                  All functions must be Python expressions.')
    parser.add_argument('--import', action=SparkAction, metavar="MODULE",
                                    help='Import an external library or a local module file.')                                                       
    parser.add_argument('--textFile',  action=SparkAction, metavar="FILE", 
                                       help='Create and RDD from a text file, local or on HDFS.') 
                                      
    # Transformations                                                      
    parser.add_argument('--filter',  action=SparkAction, metavar="FUNC", help='Func(e) => bool')  
    parser.add_argument('--map',  action=SparkAction, metavar="FUNC", help='Func(e) => object')  
    parser.add_argument('--flatMap',  action=SparkAction, metavar="FUNC", help='Func(e) => iterable ')  
    parser.add_argument('--distinct',  action=SparkAction, nargs=0) 
    parser.add_argument('--sortBy',  action=SparkAction, metavar="FUNC", help='Func(e) => object') 
    parser.add_argument('--sortByKey',  action=SparkAction,  metavar="FUNC", help='Func(e) => object') 
    parser.add_argument('--reduceByKey',  action=SparkAction, metavar="FUNC", help='Func(v1,v2) => object')  
    parser.add_argument('--mapPartitions',  action=SparkAction, metavar="FUNC", help='Func(e) => iterable')      
    
    parser.add_argument('--groupByKey',  action=SparkAction, nargs=0)  

    # Actions                    
    parser.add_argument('--reduce',  action=SparkAction, metavar="FUNC", help='Func(v1,v2) => object' )   
    parser.add_argument('--count',  action=SparkAction, nargs=0)  
    parser.add_argument('--countByKey',  action=SparkAction, nargs=0)      
    parser.add_argument('--take',  action=SparkAction, metavar="N" )       
    parser.add_argument('--saveHDFS',  action=SparkAction, metavar="FILE",
                                       help='Save the output on the HDFS file system.')      
    parser.add_argument('--saveLocal',  action=SparkAction, metavar="FILE",
                                       help='Save the output on the local file system.')      
    
    args = vars(parser.parse_args())
    print ("Job Workflow")
    for i,(action, function) in  enumerate (args["actions"]):
        print str(i+1) + ".", action, "-"*(14-len(action))  , function if function != [] else ""

    # Spark Context
    conf = (SparkConf()
             .setAppName("Spark Command Line Tool")
    )
    sc = SparkContext(conf = conf)

    this_RDD = None
    import_list=[]
    for action, arg in args["actions"]:

        if action == "import":
            if arg[-3:] == ".py":            
                sc.addPyFile(arg)
            module_name=arg.split("/")[-1].split(".")[0]
            import_list.append(module_name)

        if action == "textFile":
            this_RDD=sc.textFile(arg)    

        elif action == "filter":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.filter(func)
            
        elif action == "map":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.map(func)

        elif action == "mapPartitions":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.mapPartitions(func)

        elif action == "flatMap":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.flatMap(func)
            
        elif action == "distinct":
            this_RDD=this_RDD.distinct()   

        elif action == "groupByKey":
            this_RDD=this_RDD.groupByKey() 

        elif action == "reduceByKey":
            func = getDoubleArgFunction (eval('lambda v1,v2: ' + arg), import_list)
            this_RDD=this_RDD.reduceByKey(func)  
            
        elif action == "sortBy":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.sortBy(func)
            
        elif action == "sortByKey":
            func = getSingleArgFunction (eval('lambda e: ' + arg), import_list)
            this_RDD=this_RDD.sortByKey(func)
            
        elif action == "reduce":
            func = getDoubleArgFunction (eval('lambda v1,v2: ' + arg), import_list)
            this_RDD=sc.parallelize([this_RDD.reduce(func)])

        elif action == "count":
            this_RDD=sc.parallelize([this_RDD.count()])

        elif action == "countByKey":
            this_RDD=sc.parallelize(this_RDD.countByKey().items())

        elif action == "take":
            this_RDD=sc.parallelize(this_RDD.take(int(arg)))
                        
        elif action == "saveLocal":
            call ("/usr/local/hadoop/bin/hdfs dfs -rm -r " + arg, shell=True)
            this_RDD.saveAsTextFile(arg)
            call ("/usr/local/hadoop/bin/hdfs dfs -getmerge " + arg + " " + arg , shell=True)  
            call ("/usr/local/hadoop/bin/hdfs dfs -rm -r " + arg, shell=True)

        elif action == "saveHDFS":
            call ("/usr/local/hadoop/bin/hdfs dfs -rm -r " + arg, shell=True)
            this_RDD.saveAsTextFile(arg)          
                        
                        
class SparkAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'actions' in namespace:
            setattr(namespace, 'actions', [])
        previous = namespace.actions
        previous.append((self.dest, values))
        setattr(namespace, 'actions', previous)

def getSingleArgFunction(func, import_list):
    def myFunc (e):
        for module in import_list:
            globals()[module]=importlib.import_module(module)
        return func(e)
    return myFunc

def getDoubleArgFunction(func, import_list):
    def myFunc (v1,v2):
        for module in import_list:
            globals()[module]=importlib.import_module(module)
        return func(v1,v2)
    return myFunc

        
main()





    
    

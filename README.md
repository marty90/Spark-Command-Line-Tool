# Spark Command Line Tool
=========================
Spark Command Line Tool allows one to have set up a Spark job using a command line. All functions must be Python expressions.

# Table of Content
<!---
Done with https://github.com/ekalinin/github-markdown-toc )
-->
   * [1. Description](#1-description)
   * [2. Prerequisites](#2-prerequisites)
      * [2.1 Getting Started](#21-getting-started)
      * [2.2 Driver allocation](#22-driver-allocation)
      * [2.3 Input path specification](#23-input-path-specification)
      * [2.4 Expression syntax](#24-expression-syntax)
   * [3. Running a Job](#3-running-a-job)
   * [4 Examples](#4-examples)
      * [4.1 Word Count](#41-word-count)
      * [4.2 Word Count with sorted output](#42-word-count-with-sorted-output)
      * [4.3 Overall Word Count](#43-overall-word-count)
      * [4.4 Distinct Word Count](#44-distinct-word-count)
      * [4.4 Initial Letter Count](#44-initial-letter-count)

         
# 1. Description
This tool allows to run simple *Spark* jobs using a simple command line syntax.
You can create a simple RDDs from text files;
Then, it is possible to instrument tasks coming from a predefined set of possible transformations.
Finally you can perform actions on the RDDs and save them on disk(s).
Please read something about [Spark](http://spark.apache.org/) if you are not familiar with it.

For information about this Readme file and this tool please write to
[martino.trevisan@polito.it](mailto:martino.trevisan@polito.it)

# 2. Prerequisites
## 2.1 Getting Started
To use this tool you need a *Spark* cluster already configured and the `spark-submit` utility.
Please download locally this tool with this command line:
```
git clone https://github.com/marty90/Spark-Command-Line-Tool
```
## 2.2 Driver allocation

You must run this *Spark* application with the `spark-submit` tool.
Please rember to set the `--master` option in the correct way;
it can be `yarn-client` (driver process is executed on the local machine)
or `yarn-cluster` (driver process is executed on a cluster node).

With the `--saveLocal` option, the result is saved on the local file system too;
for obvious reasons, this is allowed only in `yarn-client` mode.

## 2.3 Input path specification
The input path for the text files will be given as input to the Spark environment;
therefore it can contain wildcards (\*) and expansions (in *bash-like* syntax, e.g., `log_\{1,2\}` will be expanded in `log_1` and `log_2` ).
The path can refer to *HDFS* files and in this case it will be something like the following :
```
hdfs://BigDataHA/data/2016_*/mylog.gz
```
It can refer to the local file system as well (when running the driver locally), using this syntax:
```
file:///<absolute_path_to_files>
```

## 2.4 Expression syntax
This tool heavily uses `eval` and `exec` *python builtins*; so, be careful when writing your command line.
All arguments must be python expressions; if you are not familiar with *python* (2.7), please read [something](https://docs.python.org/2/).

# 3. Running a Job
The tool has the followind syntax:
```
spark-submit Spark-Command-Line-Tool.py [-h] [--import MODULE] [--textFile FILE]
                                  [--filter FUNC] [--map FUNC]
                                  [--flatMap FUNC] [--distinct]
                                  [--sortBy FUNC] [--sortByKey FUNC]
                                  [--reduceByKey FUNC] [--mapPartitions FUNC]
                                  [--groupByKey] [--reduce FUNC] [--count]
                                  [--countByKey] [--take N] [--saveHDFS FILE]
                                  [--saveLocal FILE]

Spark Command Line Tool allows one to have set up a Spark job using a command
line. All functions must be Python expressions.

optional arguments:
  -h, --help            show this help message and exit
  --import MODULE       Import an external library or a local module file.
  --textFile FILE       Create and RDD from a text file, local or on HDFS.
  --filter FUNC         Func(e) => bool
  --map FUNC            Func(e) => object
  --flatMap FUNC        Func(e) => iterable
  --distinct
  --sortBy FUNC         Func(e) => object
  --sortByKey FUNC      Func(e) => object
  --reduceByKey FUNC    Func(v1,v2) => object
  --mapPartitions FUNC  Func(e) => iterable
  --groupByKey
  --reduce FUNC         Func(v1,v2) => object
  --count
  --countByKey
  --take N
  --saveHDFS FILE       Save the output on the HDFS file system.
  --saveLocal FILE      Save the output on the local file system.
 ```
 
# 4 Examples
In this section we use as input file the sample dataset provided in this repository with the name `lorem-ipsum.txt`.
## 4.1 Word Count
Count the occurrency number of each word:
```
spark-submit --master local[*] Spark-Command-Line-Tool.py \
         --textFile file:///$(pwd)/lore-ispum.txt \
         --flatMap "e.split()" \
         --map "(e,1)" \
         --countByKey \
         --map "e[0] + ' ' + str(e[1])" \
         --saveLocal WordCount.txt
```
## 4.2 Word Count with sorted output
Count the occurrency number of each word and sort the output by occurency number (high to low):
```
spark-submit --master local[*] Spark-Command-Line-Tool.py \
         --textFile file:///$(pwd)/lore-ispum.txt \
         --flatMap "e.split()" \
         --map "(e,1)" \
         --countByKey \
         --sortBy "0-e[1]" \
         --map "e[0] + ' ' + str(e[1])" \
         --saveLocal SortedWordCount.txt
```
## 4.3 Overall Word Count
Count how many words (sapce separated) are present in the document:
```
spark-submit --master local[*] Spark-Command-Line-Tool.py \
         --textFile file:///$(pwd)/lore-ispum.txt \
         --flatMap "e.split()" \
         --count \
         --saveLocal WordNumber.txt
```
## 4.4 Distinct Word Count
Count how many words (sapce separated) are present in the document:
```
spark-submit --master local[*] Spark-Command-Line-Tool.py \
         --textFile file:///$(pwd)/lore-ispum.txt \
         --flatMap "e.split()" \
         --distinct \
         --count \
         --saveLocal DistinctWordNumber.txt
```
## 4.4 Initial Letter Count
Count how many words (sapce separated) are present in the document:
```
spark-submit --master local[*] Spark-Command-Line-Tool.py \
         --textFile file:///$(pwd)/lore-ispum.txt \
         --flatMap "e.split()" \
         --map "(e[0].lower(),1)" \
         --countByKey \
         --map "e[0] + ' ' + str(e[1])" \
         --saveLocal InitialLetter.txt
```

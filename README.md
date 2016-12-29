# Spark Command Line Tool
=========================
Spark Command Line Tool allows one to have set up a Spark job using a command line. All functions must be Python expressions.

# Table of Content
<!---
Done with https://github.com/ekalinin/github-markdown-toc )
-->

         
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
bla bla

## 4 Examples
In this section we use as input file the sample dataset provided [here](http://spark.apache.org/...).
## 4.1 Count
To select all the lines in the tcp_complete log where the *FQDN* is `www.facebook.com`, you can type:
```
path='hdfs://.../2016_11_27_*/log_tcp_complete.gz'
spark-submit  simple_query.py -i $path -o "facebook_flows" \
              --query "fqdn=='www.facebook.com'"
```
### 3.1.2 HTTP requests to port 7547
To select all the urls on server port 7547, you can use:
```
path='hdfs://.../2016_11_27_*/log_http_complete.gz'
spark-submit  simple_query.py -i $path -o "port_7547" -s tab \
              --query "s_port=='7547'"
```
Please note that all fields are strings. If you want to evaluate them as integer or float, you must explicitely convert them.

# 4. Running an advanced query (map + reduce)
This kind of query is more complex than the previous one since it **includes a *filter*, a *map* and a *reduce* transformation.**
Optionally, you can specify a second map transformation if you use *ReduceByKey* that will be executed after the latter.
Three kinds of workflows are allowed.
* *Filter* -> *Map* -> *Distinct*
* *Filter* -> *Map* -> *Reduce*
* *Filter* -> *Map* -> *ReduceByKey* ( -> *Map*)

The command line syntax is:
```
spark-submit advanced_query.py [-h] [-i input] [-o output] [--filter filter]
                         [--map map] [--distinct] [--reduce reduce]
                         [--reduceByKey reduceByKey] [--finalMap finalMap]
                         [--separator separator] [-l]
optional arguments:
  -h, --help            show this help message and exit
  -i input, --input input
                        Input log files path.
  -o output, --output output
                        Output file where the result of the query is written.


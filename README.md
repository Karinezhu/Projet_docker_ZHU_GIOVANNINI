# Apache spark cluster + Mongodb on Docker: 

In this project, we are going to build an standalone Apache Spark cluster with Mongodb.

## Cluster overview

The cluster is composed of four main components: Mongodb, the Spark master node and two Spark workers nodes.

![image](https://user-images.githubusercontent.com/77232278/166847257-9d7ce5c8-780f-43ed-8c56-cf2ce817ab03.png)


## Installation

### Prerequisites
  - Install Docker and Docker compose

### Containers content

#### Cluster base image

The cluster is created with one unique image that can be launched as any workload we want.

##### Dockerfile
```
# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.0.2 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
```

##### Start-spark file

```
#!/bin/bash

. "/opt/spark/bin/load-spark-env.sh"

if [ "$SPARK_WORKLOAD" == "master" ];
then

export SPARK_MASTER_HOST=`hostname`

cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_MASTER_LOG

elif [ "$SPARK_WORKLOAD" == "worker" ];
then

cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER >> $SPARK_WORKER_LOG

elif [ "$SPARK_WORKLOAD" == "submit" ];
then
    echo "SPARK SUBMIT"
else
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker, submit"
fi
```

#### Mongo db

Fot this container, we used the official image from mongo.

***N.B. For the data importation, we tried to use another container (mongo-seed) to seed the data automatically, but despite multiples attempts it wasn't working***

#### Mongo seed

##### Dockerfile
```
FROM mongo

COPY Dry_Bean_Dataset.csv /Dry_Bean_Dataset.csv


ADD import.sh /import.sh
RUN chmod +x /import.sh

CMD mongoimport --database Bdt --collection grain --file /Dry_Bean_Dataset.csv --headerline --type csv
```

##### Import file
```
#! /bin/bash

mongoimport --database Bdt --collection grain --file /tmp/Dry_Bean_Dataset.csv --headerline --type csv
```

#### Docker compose file
```
version: "2.2.3"
services:
  mongodb:
    hostname: mongodb1 
    image: mongo
    container_name: mongodb  
    ports: 
      - 27017
  mongo_seed:
    container_name: mongo_seed
    build: ./mongo-seed
    links:
      - mongodb
  spark-master:
    image: cluster_image:1.0.0
    container_name: spark-master1
    ports:
      - "9090:8080"
      - "7077:7077"
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data
    environment:
      - SPARK_LOCAL_IP=spark-master
      - SPARK_WORKLOAD=master
  spark-worker-a:
    image: cluster_image:1.0.0
    container_name: spark-worker-a
    ports:
      - "9091:8080"
      - "7000:7000"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-a
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data
  spark-worker-b:
    image: cluster_image:1.0.0
    container_name: spark-worker-b
    ports:
      - "9092:8080"
      - "7001:7000"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-b
    volumes:
        - ./apps:/opt/spark-apps
        - ./data:/opt/spark-data
```


### Build the image 


Go on the image directory 
```
cd cluster_image/
```

Then build the cluster image
```
docker build . -t cluster_image:1.0.0
```

### Start the cluster

Return to the root first.

```
cd ..
```

```
docker-compose up -d
```

### Create the mongo database

Now we are going to create the database to test with pyspark.

1.Retrieve the dataset
```
wget https://raw.githubusercontent.com/Karinezhu/Projet_docker_ZHU_GIOVANNINI/master/Dry_Bean_Dataset.csv
```

2.Copy the dataset on the mongo container

```
docker cp Dry_Bean_Dataset.csv mongodb:/tmp/Dry_Bean_Dataset.csv
```

3.Run the mongo container

```
docker exec -it mongodb bash
```

4.Import the dataset in the mongo database

```
mongoimport -d Bdtest -c grain --file /tmp/Dry_Bean_Dataset.csv --headerline --type csv
```

5.Run mongosh 

```
mongosh 27017
```

Now we can use the below commands to use the database and retrieve some data.

```
show bds
use Bdtest
db.grain.findOne()
```

![image](https://user-images.githubusercontent.com/77232278/166684085-6f67ac45-863a-498f-90bb-47e4a698cc72.png)

### Connect to the spark shell

1.Run spark-master
```
docker exec -it spark-master1 bash
```

2.Install the packages for pypspark 
```
apt update
apt install python3-pip
pip3 install pyspark
```

1.Run pyspark
```
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:2.4.2
```

#### Connection to Mongo db

1. Import the packages 
```
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
```

Since we got some issues with the session, we stop the session first, then we create another one
```
sc.stop()
```

2.Configure spark
```
sparkConf = SparkConf().setAppName("Mongo_spark")
sparkConf.set("spark.mongodb.input.uri", "mongodb://mongodb1:27017/Bdtest.grain")
sparkConf.setMaster("spark://spark-master1:7077")
sparkConf.set("spark.submit.deployMode", "cluster")
sc = SparkContext(conf = sparkConf)
sqlContext =SQLContext(sc)
```

3.Now retrieve the data 
```
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").load()
df.printSchema()
```

![image](https://user-images.githubusercontent.com/77232278/166683483-2dcd732a-87f1-4399-b303-56a1f66f350b.png)

## Links for Docker hub repertories

  - [Cluster image](https://hub.docker.com/repository/docker/karinezhu/cluster_image)

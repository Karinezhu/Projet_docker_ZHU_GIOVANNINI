# Apache spark cluster + Mongodb on Docker: 

## Installation

### Retrieve the dataset
```
wget https://raw.githubusercontent.com/Karinezhu/Projet_docker_ZHU_GIOVANNINI/master/Dry_Bean_Dataset.csv
```

### Prerequisites
  - Install Docker and Docker compose


### Build the image 

```
docker build -t cluster-apache-spark:3.0.2 .
```

### Start the cluster
```
docker-compose up -d
```

### Connect to the spark shell

#### Run spark-master
```
docker exec -it spark-master1 bash
```
#### Install the packages for pypspark 

```
apt update
apt install python3-pip
pip3 install pyspark
```

#### Run pyspark
```
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:2.4.2 --master spark://spark-master1:7077
```

## Connection to Mongo db

```
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
```

```
sc.stop()
```

```
sparkConf = SparkConf().setAppName("App")
sparkConf.set("spark.mongodb.input.uri", "mongodb://mongodb1:27017/Bdtest.grain")
sparkConf.setMaster("spark://spark-master1:7077")
sparkConf.set("spark.submit.deployMode", "cluster")
sc = SparkContext(conf = sparkConf)
sqlContext =SQLContext(sc)
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").load()
df.printSchema()
```

![image](https://user-images.githubusercontent.com/77232278/166683483-2dcd732a-87f1-4399-b303-56a1f66f350b.png)

## Create the mongo database

1.Copy the dataset on the mongo container.

```
docker cp Dry_Bean_Dataset.csv mongodb:/tmp/Dry_Bean_Dataset.csv
```

2.Run the mongo container.

```
docker exec -it mongodb bash
```

3.Import the dataset in the mongo database.

```
mongoimport -d Bdtest -c grain --file /tmp/Dry_Bean_Dataset.csv --headerline --type csv
```

4.Run mongosh 

```
mongosh 27017
```

Now we can use the below commands to use the database and retrieve some data.

```
show bds
use Bdtest
db.grain.find().pretty()
```

![image](https://user-images.githubusercontent.com/77232278/166684085-6f67ac45-863a-498f-90bb-47e4a698cc72.png)

## Links for Docker hub repertories

  - [Cluster image](https://hub.docker.com/repository/docker/karinezhu/cluster_image)

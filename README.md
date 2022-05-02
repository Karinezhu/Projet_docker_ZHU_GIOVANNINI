# Apache spark cluster + Mongodb on Docker: 

## Installation

### Retrieve the datasets
```
https://raw.githubusercontent.com/Karinezhu/Projet_docker_ZHU_GIOVANNINI/master/Dry_Bean_Dataset.csv
https://raw.githubusercontent.com/Karinezhu/Projet_docker_ZHU_GIOVANNINI/master/opendata.json
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
pyspark
```

## Run Mongo alone 

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
mongosh
```

Now we can use the below commands to use the database and retrieve some data.

```
show bds
use Bdtest
db.grain.find().pretty()
```

# Apache spark cluster + Mongodb on Docker: 

## This project 

```
Docker-compose up -d
```

```
docker cp Dry_Bean_Dataset.csv mongodb:/tmp/Dry_Bean_Dataset.csv
docker exec mongodb mongoimport -d Bdtest -c grain --file /tmp/Dry_Bean_Dataset.csv
```
```
docker exec -it mongodb
```

```
mongosh 27017
```
```
show bds
```
```
use Bdtest
```
```
db.grain.find().pretty()
```

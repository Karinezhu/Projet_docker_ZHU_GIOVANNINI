# Spark cluster + Mongodb : 

```
Docker-compose up -d

```

```
docker cp Dry_Bean_Dataset.csv <container-name-or-id>:/tmp/Dry_Bean_Dataset.csv
docker exec <container-name-or-id> mongoimport -d Bdtest -c grain --file /tmp/Dry_Bean_Dataset.csv
```
```
docker exec -it <container-name> 
```

```
mongosh 27017
```

show bds

use Bdtest

db.grain.find().pretty()

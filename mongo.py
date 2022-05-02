import pymongo
import pymongo_spark

mongo_url = 'mongodb://mongo:27017/'

client = pymongo.MongoClient(mongo_url)
client.foo.bar.insert_many([
    {"x": 1.0, "y": -1.0}, {"x": 0.0, "y": 4.0}])
client.close()

pymongo_spark.activate()
rdd = (sc.mongoRDD('{0}foo.bar'.format(mongo_url))
    .map(lambda doc: (doc.get('x'), doc.get('y'))))
rdd.collect()
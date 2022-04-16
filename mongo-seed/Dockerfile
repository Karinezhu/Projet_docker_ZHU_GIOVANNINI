FROM mongo

COPY primer-dataset.json /primer-dataset.json
CMD mongoimport --host mongodb --db Bdres --collection restaurants --type json --file /primer-dataset.json --jsonArray

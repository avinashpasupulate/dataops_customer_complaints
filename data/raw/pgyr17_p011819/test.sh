
cd /Users/avinashpasupulate/Documents/datascience/dataops/data/raw/pgyr17_p011819
echo "loading to ownership table . . . "
split -a 6 -b 15m ownership.csv ownership.part_
ls
pwd
for f in ownership.part_*; do echo "loading $f"; mysql --port=3306 -h terraform-20190601084659482700000001.csclevrtct8b.us-east-1.rds.amazonaws.com -u uywfwmartm -p7qADBvQFgv --local-infile=1 --verbose --show-warnings --execute="LOAD DATA LOCAL INFILE '$f' INTO TABLE opencmsdb.ownership FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n'"; done
#mysqlimport --local --use-threads 4 --compress --port=3306 -h terraform-20190601084659482700000001.csclevrtct8b.us-east-1.rds.amazonaws.com -u uywfwmartm -p7qADBvQFgv --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\n' opencmsdb ownership.part_*
rm -r ownership.part_*

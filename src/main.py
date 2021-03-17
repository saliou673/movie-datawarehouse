import os
from core.database import Database
from core.logger import log

db = Database()

sqlDir = os.getcwd() + "/src/migrations/";

log.info("Database creation ...")
db.executeScriptFile(sqlDir + "create-database.sql");
log.info("Database created !")

# select the created database
db.selectDB('movie_warehouse')

log.info("Tables creation ...")
db.executeScriptFile(sqlDir + "create-tables.sql");
log.info("Tables created !")
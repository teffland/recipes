from cooking import db_helper

print "INITIALIZING DB SCHEMA"
db_helper.db_init()
print "LOADING INITIAL DATA"
db_helper.db_seed3()

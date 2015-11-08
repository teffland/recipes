from cooking import app
from cooking.config import DevelopmentConfig as cf
app.run(host=cf.HOST, port=cf.PORT, debug=cf.DEBUG)

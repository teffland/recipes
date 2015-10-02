# DEPRECATED

class BaseModel(object):

    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def timestamp_to_db(cls, date_time):
        if date_time:
            return "'" + date_time.strftime(BaseModel.TIMESTAMP_FORMAT) + "'"
        else:
            return 'NULL'

    @classmethod
    def db_to_timestamp(cls, date_time_string):
        if date_time_string.lower() != 'null':
            return datetime.datetime.strptime(date_time_string, BaseModel.TIMESTAMP_FORMAT)
        else:
            return None

    @classmethod
    def string_to_db(cls, str):
        if str:
            return "'" + str + "'"
        else:
            return "NULL"

    @classmethod
    def number_to_db(cls, number):
        if number != None:
            return str(number)
        else:
            return "NULL"

from hashlib import sha384
import urllib
from cooking.config import Config
from werkzeug import secure_filename
import os


class Photo(object):

    DEFAULT_IMAGE = "no_image.png"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    @classmethod
    def hash_name(cls, name):
        return sha384(name).digest().encode('base64')[0:-1].replace('/', '-')

    @classmethod
    def download_photo(cls, url):
        try:
            photo_hash = cls.hash_name(url)
            localname = photo_hash + ".jpg"
            urllib.urlretrieve(url, Config.PHOTO_DIR + localname)
            return localname
        except:
            return cls.DEFAULT_IMAGE

    @classmethod
    def allowed_file(cls, file):
        return '.' in file.filename and file.filename.rsplit('.', 1)[1] in cls.ALLOWED_EXTENSIONS

    @classmethod
    def make_server_filename(cls, file):
        aux = secure_filename(file.filename.split('/')[-1].split('\\')[-1])
        name, extension = aux.split('.', 1)
        return cls.hash_name(name) + '.' + extension 

    @classmethod
    def upload_photo(cls, file):
        server_filename = cls.make_server_filename(file)
        file.save(os.path.join(Config.PHOTO_DIR, server_filename))
        return server_filename
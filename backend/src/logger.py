import logging
import logging.handlers

def init(logfile='./mididec.log', weblogfile='./webapi.log', maxBytes=1024*100, backupCount=2):
    init_default(logfile, maxBytes, backupCount)
    init_events(logfile, maxBytes, backupCount)
    init_users(logfile, maxBytes, backupCount)
    init_webapi(weblogfile, maxBytes, backupCount)

def init_default(logfile, maxBytes, backupCount):
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile, "a", encoding=None, delay="true", maxBytes=maxBytes, backupCount=backupCount)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)

def init_events(logfile, maxBytes, backupCount):
    logger = logging.getLogger("events")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile, "a", encoding=None, delay="true", maxBytes=maxBytes, backupCount=backupCount)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)

def init_users(logfile, maxBytes, backupCount):
    logger = logging.getLogger("users")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile, "a", encoding=None, delay="true", maxBytes=maxBytes, backupCount=backupCount)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)

def init_webapi(logfile, maxBytes, backupCount):
    logger = logging.getLogger("webapi")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile, "a", encoding=None, delay="true", maxBytes=maxBytes, backupCount=backupCount)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)

def get(name='default'):
    return logging.getLogger(name)

def users():
    return get('users')

def events():
    return get('events')

def webapi():
    return get('webapi')

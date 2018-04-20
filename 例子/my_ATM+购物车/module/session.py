import hashlib,time


class Session:
    def __init__(self):
        pass

    '''制作session的ID'''
    def __createSession(self):
        create_session_id = "%s" % (time.time())
        hash = hashlib.sha1()
        hash.update(bytes(create_session_id, encoding="utf-8"))
        return hash.hexdigest()

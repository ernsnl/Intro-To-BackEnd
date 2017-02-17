class Error(object):

    def __init__(self, id, error_msg):
        self.id = id
        self.error_msg = error_msg

    def __str__(self):
        return self.id + ': ' + self.error_msg

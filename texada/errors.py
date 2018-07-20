class ClientError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message or "You've sent a bad request"
        self.status_code = status_code or ClientError.status_code
        self.payload = payload or {}

    def to_dict(self):
        error = dict(self.payload or ())
        error["message"] = self.message
        return error

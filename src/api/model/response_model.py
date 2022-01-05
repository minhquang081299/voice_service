class DataModel(object):
    def __init__(self, result, message, item):
        self.result = result
        self.message = message
        self.item = item

class ErrorModel(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class ResponseModel(object):
    def __init__(self, data, error):
        self.data = data
        self.error = error



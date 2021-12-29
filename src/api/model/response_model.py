class DataModel:
    def __init__(self, result, message, item):
        self.result = result
        self.message = message
        self.item = item

class ErrorModel:
    def __init__(self, code, message):
        self.code = code
        self.message = message

class ResponseModel:
    def __init__(self, data, error):
        self.data = data
        self.error = error

error = None
data = None


item = {"sess_id" : sess_id , "url": output_file[sess_id]}
data = DataModel(True, "File thay đổi thành công ", item)
if error is not None:
    error = vars(error)
if data is not None:
    data = vars(data)
response = ResponseModel(data, error)
return json.dumps(vars(response))
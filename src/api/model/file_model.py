
class FileModel():
    def __init__(self, file, rs):
        self.file=file
        
    def _check_type(self):
        if '.wav' not in self.file:
            return False
        return True
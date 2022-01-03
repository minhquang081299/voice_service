import pydub
import os
import librosa
from src.api.config.config import AudioConfig as af

class FileService:
    def __init__(self, prefix, fn):
        self._prefix = prefix
        self._fn = fn
        self._fp = prefix+'/'+fn
        self._output =None
    
    def check_length(self) -> bool:
        """
            before normalize
            if file's too large, return False
            else return True
        """
        infor = self._read_info()
        sr = infor['sample_rate']
        duration = infor['duration']
        max_lenght = af.MAX_DURATION*af.SR
        if sr*duration>max_lenght:
            return False
        return True
        
    
    def _read_info(self) -> dict:
       
        print(self._fp)
        sr = librosa.get_samplerate(self._fp)
        print(sr)
        duration = librosa.get_duration(filename = self._fp)
        return {"filename": self._fn,
                "normed_filename": self._output,
                "prefix": self._prefix,
                "duration": duration,
                "sample_rate": sr}
    
    def check_type(self):
        return '.wav' in self._fn
    
    def convert_audio(self) -> str:
        """
        return new name of converted file
        if the file's not meet the conditions, return "" (empty string)
        """
        
        filename = self._fn.split(".")[0]
        filename = filename+'_norm.wav'
        self._output = self._prefix+'/'+filename
        if not self.check_type():
            if self.check_length():
                try:
                    os.system(f'ffmpeg -i {self._fp} -ar 16000 -ac 1 -sample_fmt s16 {self._output}')
                    os.system(f'rm {self._fp}')
                    return filename
                except FileNotFoundError as e:
                    print(e)
                    print(f"File {self._fp} does not exist") 
            else:
                print("File's too large, please resize your audio file")
              
        else:
            sr = self._read_info()
            
            if sr['sample_rate'] != 16000:
                try:
                    os.system(f'ffmpeg -i {self._fp} -ar 16000 -ac 1 -sample_fmt s16 {self._output}') 
                    os.system(f'rm {self._fp}')
                    return filename
                except FileNotFoundError as e:
                    print(e)
                    print(f"File {self._fp} does not exist") 
        return ""
                
            
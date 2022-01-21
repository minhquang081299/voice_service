from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
from datasets import load_dataset
import soundfile as sf
import kenlm
from transformers.file_utils import cached_path, hf_bucket_url
from pyctcdecode import Alphabet, BeamSearchDecoderCTC, LanguageModel
import os, zipfile
from src.api.config.config import ModelConfig
import librosa
from src.api.config.config import ModelConfig as mc

class VoiceService():
    def __init__(self, 
                 lm_model_path:str,
                 w2v2_processor:str,
                 w2v2_for_ctc:str):
        
        self._ngram_lm_model_path = lm_model_path
        self._w2v2_processor = Wav2Vec2Processor.from_pretrained(w2v2_processor)
        self._w2v2_for_ctc = Wav2Vec2ForCTC.from_pretrained(w2v2_for_ctc)
        self._ngram_lm_model = self._get_decoder_ngram_model(self._w2v2_processor.tokenizer)
        
    def _get_decoder_ngram_model(self, tokenizer):
        vocab_dict = tokenizer.get_vocab()
        sort_vocab = sorted((value, key) for (key, value) in vocab_dict.items())
        vocab = [x[1] for x in sort_vocab][:-2]
        vocab_list = vocab
        # convert ctc blank character representation
        vocab_list[tokenizer.pad_token_id] = ""
        # replace special characters
        vocab_list[tokenizer.unk_token_id] = ""
        # vocab_list[tokenizer.bos_token_id] = ""
        # vocab_list[tokenizer.eos_token_id] = ""
        # convert space character representation
        vocab_list[tokenizer.word_delimiter_token_id] = " "
        # specify ctc blank char index, since conventially it is the last entry of the logit matrix
        alphabet = Alphabet.build_alphabet(vocab_list, ctc_token_idx=tokenizer.pad_token_id)
        lm_model = kenlm.Model(self._ngram_lm_model_path)
        decoder = BeamSearchDecoderCTC(alphabet,
                                    language_model=LanguageModel(lm_model))
        return decoder
    
    def _map_to_array(self, batch):
        speech, sampling_rate = sf.read(batch["file"], dtype='float32')
        batch["speech"] = speech
        batch["sampling_rate"] = sampling_rate
        return batch
    
    def voice_service(self, audio_path):
        ds=self._map_to_array({"file": audio_path})
        input_values = self._w2v2_processor(
                  ds["speech"], 
                  sampling_rate=ds["sampling_rate"], 
                  return_tensors="pt"
            ).input_values
        
        logits = self._w2v2_for_ctc(input_values).logits[0]
        beam_search_output = self._ngram_lm_model.decode(logits.cpu().detach().numpy(), beam_width=500)
        return beam_search_output
    
    def long_voice_service(self, audio_path):
        rs = []
        sr = librosa.get_samplerate(audio_path)
        stream = librosa.stream(audio_path,
                            block_length=256,
                            frame_length=4096,
                            hop_length=1024)
        
        for y in stream:
            ds={'speech': y,'sampling_rate':sr}
            input_values = self._w2v2_processor(
                    ds["speech"], 
                    sampling_rate=ds["sampling_rate"], 
                    return_tensors="pt"
                ).input_values
            
            logits = self._w2v2_for_ctc(input_values).logits[0]
            beam_search_output = self._ngram_lm_model.decode(logits.cpu().detach().numpy(), beam_width=500)
            rs.append(beam_search_output)
            
        return rs
        
        
        
        
# def download_pretrain_model(lm_path, w2v2_processor_path, w2v2_ctc_path, cache_dir='./cache/')->None:
#     processor = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h", cache_dir = cache_dir)
#     model = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h",cache_dir=cache_dir)
#     processor.save_pretrained(w2v2_processor_path)
#     model.save_pretrained(w2v2_ctc_path)
#     lm_file = hf_bucket_url("nguyenvulebinh/wav2vec2-base-vietnamese-250h", filename='vi_lm_4grams.bin.zip')
#     lm_file = cached_path(lm_file,cache_dir=cache_dir)
#     with zipfile.ZipFile(lm_file, 'r') as zip_ref:
#         zip_ref.extractall(cache_dir)
#     lm_file = cache_dir + 'vi_lm_4grams.bin'

# if __name__ == "__main__":
#     processor_path = ModelConfig.W2V2_PROCESSOR_PREFIX
#     ctc_path = ModelConfig.W2V2_FOR_CTC_PREFIX
#     download_pretrain_model('', processor_path, ctc_path)


    
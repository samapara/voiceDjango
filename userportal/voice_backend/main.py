import os
import sys
from pathlib import Path

import librosa
import numpy as np
import torch

from userportal.voice_backend.encoder import inference as encoder
from userportal.voice_backend.encoder.params_model import model_embedding_size as speaker_embedding_size
from userportal.voice_backend.synthesizer.inference import Synthesizer
from userportal.voice_backend.vocoder import inference as vocoder

base_path = os.path.join(os.getcwd(), "userportal/voice_backend")

enc_model_path = os.path.join(base_path, "encoder/saved_models/pretrained.pt")
syn_model_dir = os.path.join(base_path, "synthesizer/saved_models/logs-pretrained/")
voc_model_fpath = os.path.join(base_path, "vocoder/saved_models/pretrained/pretrained.pt")
low_mem = False
# print(Path(os.path.join(os.getcwd(), syn_model_dir ,"taco_pretrained")))
print(enc_model_path, syn_model_dir, voc_model_fpath)


class BackendHandler:

    def __init__(self):
        self.synthesizer = Synthesizer(Path(syn_model_dir + "taco_pretrained"), low_mem=low_mem)
        encoder.load_model(Path(enc_model_path))
        vocoder.load_model(voc_model_fpath)

    def test_models(self):
        print("Running a test of your configuration...\n")
        if not torch.cuda.is_available():
            print("Your PyTorch installation is not configured to use CUDA. If you have a GPU ready "
                  "for deep learning, ensure that the drivers are properly installed, and that your "
                  "CUDA version matches your PyTorch installation. CPU-only inference is currently "
                  "not supported.", file=sys.stderr)

        print("Preparing the encoder, the synthesizer and the vocoder...")
        # encoder.load_model(Path(enc_model_path))
        # synthesizer = Synthesizer(Path(syn_model_dir + "taco_pretrained"), low_mem=low_mem)

        print("\tTesting the encoder...")
        encoder.embed_utterance(np.zeros(encoder.sampling_rate))

        # Create a dummy embedding. You would normally use the embedding that encoder.embed_utterance
        # returns, but here we're going to make one ourselves just for the sake of showing that it's
        # possible.
        embed = np.random.rand(speaker_embedding_size)
        # Embeddings are L2-normalized (this isn't important here, but if you want to make your own
        # embeddings it will be).
        embed /= np.linalg.norm(embed)
        # The synthesizer can handle multiple inputs with batching. Let's create another embedding to
        # illustrate that
        embeds = [embed, np.zeros(speaker_embedding_size)]
        texts = ["test 1", "test 2"]
        print("\tTesting the synthesizer... (loading the model will output a lot of text)")
        mels = self.synthesizer.synthesize_spectrograms(texts, embeds)

        # The vocoder synthesizes one waveform at a time, but it's more efficient for long ones. We
        # can concatenate the mel spectrograms to a single one.
        mel = np.concatenate(mels, axis=1)
        # The vocoder can take a callback function to display the generation. More on that later. For
        # now we'll simply hide it like this:
        no_action = lambda *args: None
        print("\tTesting the vocoder...")
        # For the sake of making this test short, we'll pass a short target length. The target length
        # is the length of the wav segments that are processed in parallel. E.g. for audio sampled
        # at 16000 Hertz, a target length of 8000 means that the target audio will be cut in chunks of
        # 0.5 seconds which will all be generated together. The parameters here are absurdly short, and
        # that has a detrimental effect on the quality of the audio. The default parameters are
        # recommended in general.
        vocoder.infer_waveform(mel, target=200, overlap=50, progress_callback=no_action)

        print("All test passed! You can now synthesize speech.\n\n")

    def process_audio_file(self, path):
        in_fpath = Path(path)

        preprocessed_wav = encoder.preprocess_wav(in_fpath)

        original_wav, sampling_rate = librosa.load(in_fpath)

        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)

        return preprocessed_wav

    def get_embedding(self, wav):
        return encoder.embed_utterance(wav)

    def synthesize(self, text, embedding):
        texts = [text]
        embeds = [embedding]
        specs = self.synthesizer.synthesize_spectrograms(texts, embeds)

        return specs[0]

    def generate_wav(self, spec):
        generated_wav = vocoder.infer_waveform(spec)
        generated_wav = np.pad(generated_wav, (0, self.synthesizer.sample_rate), mode="constant")
        return generated_wav

    def save_to_disk(self, generated_wav, file_name):
        librosa.output.write_wav(file_name, generated_wav.astype(np.float32),
                                 self.synthesizer.sample_rate)
        print("Saved Output: %s" % file_name)

import librosa
import numpy as np

def extract_mfcc(file_path, sr=16000, n_mfcc=13):
    signal, sr = librosa.load(file_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc, axis=1)

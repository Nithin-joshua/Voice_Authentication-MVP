import librosa
import numpy as np

MIN_DURATION = 2.0        # seconds
MAX_SILENCE_RATIO = 0.4  # 40%

def validate_audio(audio_path: str):
    """
    Validates audio quality before feature extraction.
    Rejects short, silent, or low-energy recordings.
    """
    y, sr = librosa.load(audio_path, sr=None)

    duration = librosa.get_duration(y=y, sr=sr)
    if duration < MIN_DURATION:
        return False, "Audio too short"

    rms = librosa.feature.rms(y=y)[0]
    silence_ratio = np.mean(rms < 0.01)

    if silence_ratio > MAX_SILENCE_RATIO:
        return False, "Audio contains too much silence"

    return True, "Audio valid"

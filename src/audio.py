import numpy as np
import soundcard as sc
import soundfile as sf
from loguru import logger
from src.constants import OUTPUT_FILE_NAME, SAMPLE_RATE

MICROPHONE_ID = str(sc.default_microphone().name)

def record_until_keypress() -> np.ndarray:
    logger.debug("Recording... Press Enter to stop.")
    audio_chunks = []
    with sc.get_microphone(
        id=MICROPHONE_ID,
        include_loopback=True,
    ).recorder(samplerate=SAMPLE_RATE) as mic:
        while True:
            audio_chunk = mic.record(numframes=int(SAMPLE_RATE * 0.5))
            audio_chunks.append(audio_chunk)
            if input("Press Enter to stop recording or just wait to continue...") == "":
                break
    audio_data = np.concatenate(audio_chunks, axis=0)
    return audio_data

def save_audio_file(audio_data: np.ndarray, output_file_name: str = OUTPUT_FILE_NAME) -> None:
    logger.debug(f"Saving audio file to {output_file_name}...")
    sf.write(file=output_file_name, data=audio_data, samplerate=SAMPLE_RATE)
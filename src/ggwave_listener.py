import ggwave
import sounddevice as sd
import numpy as np
from typing import Optional, Callable
import threading
import queue
import time

class GGwaveListener:
    def __init__(self, callback: Callable[[str], None], sample_rate: int = 48000):
        """
        Initialize the GGwave listener.
        
        Args:
            callback: Function to call when text is decoded
            sample_rate: Audio sample rate (default: 48000)
        """
        self.callback = callback
        self.sample_rate = sample_rate
        self.instance = ggwave.init()
        self.stream = None
        self.is_running = False
        self.audio_queue = queue.Queue()
        self.processing_thread = None

    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream processing."""
        if status:
            print(f"Audio callback status: {status}")
        if self.is_running:
            # Convert to float32 and scale to [-1, 1]
            audio_data = indata[:, 0].astype(np.float32)
            self.audio_queue.put(audio_data)

    def process_audio(self):
        """Process audio data from the queue."""
        while self.is_running:
            try:
                audio_data = self.audio_queue.get(timeout=1.0)
                # Decode the GGwave signal
                decoded = ggwave.decode(self.instance, audio_data)
                if decoded:
                    try:
                        text = decoded.decode('utf-8')
                        self.callback(text)
                    except UnicodeDecodeError:
                        print("Failed to decode message as UTF-8")
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing audio: {e}")

    def start(self):
        """Start listening for GGwave signals."""
        if self.is_running:
            return

        self.is_running = True
        
        # Start audio stream
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            callback=self.audio_callback
        )
        self.stream.start()

        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_audio)
        self.processing_thread.start()

    def stop(self):
        """Stop listening for GGwave signals."""
        self.is_running = False
        
        if self.processing_thread:
            self.processing_thread.join()
            
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop()
        if hasattr(self, 'instance'):
            ggwave.free(self.instance) 
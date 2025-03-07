import os
import requests
from typing import Optional
from transformers import MarianMTModel, MarianTokenizer
import torch
from dotenv import load_dotenv

load_dotenv()

class Translator:
    def __init__(self, use_local: bool = True):
        """
        Initialize the translator.
        
        Args:
            use_local: Whether to use local model instead of Google Translate API (default: True)
        """
        self.use_local = use_local
        self.model = None
        self.tokenizer = None
        self.api_key = None
        
        if use_local:
            print("Initializing local translation model...")
            # Load the MarianMT model for English to Arabic translation
            model_name = "Helsinki-NLP/opus-mt-en-ar"
            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)
            
            # Use GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Using device: {self.device}")
            self.model.to(self.device)
        else:
            # Try to get Google Translate API key from environment
            self.api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
            if not self.api_key:
                print("Warning: Google Translate API key not found. Falling back to local model.")
                self.__init__(use_local=True)  # Recursively initialize with local model

    def translate(self, text: str) -> Optional[str]:
        """
        Translate text to Arabic.
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or None if translation fails
        """
        if not text:
            return None
            
        try:
            if self.use_local or not self.api_key:
                return self._translate_local(text)
            else:
                try:
                    return self._translate_google(text)
                except Exception as e:
                    print(f"Google Translate API error: {e}. Falling back to local model.")
                    # Fallback to local model if Google Translate fails
                    if not self.model:
                        self.__init__(use_local=True)
                    return self._translate_local(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def _translate_local(self, text: str) -> str:
        """Translate using local MarianMT model."""
        # Tokenize and translate
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        translated = self.model.generate(**inputs)
        
        # Decode the translation
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def _translate_google(self, text: str) -> str:
        """Translate using Google Translate API."""
        if not self.api_key:
            raise ValueError("Google Translate API key not available")
            
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            "q": text,
            "target": "ar",
            "source": "en",
            "key": self.api_key
        }
        
        response = requests.post(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        return result["data"]["translations"][0]["translatedText"] 
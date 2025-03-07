# GGwave to Arabic Transcription System

A real-time system that captures GGwave acoustic signals, decodes them, and translates the content into Arabic with live display.

## Features

- Real-time GGwave signal capture and decoding
- Instant translation to Arabic using local AI model (MarianMT)
- Optional Google Translate API integration
- Live transcript display through web interface
- Support for both audible and ultrasonic GGwave signals
- Noise filtering and robust error handling
- Offline translation support by default

## Prerequisites

- Python 3.8+
- PortAudio (for PyAudio)
- Internet connection (only for initial model download or Google Translate API if enabled)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GGwave-to-Arabic-Transcription-System.git
cd GGwave-to-Arabic-Transcription-System
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up environment variables:
If you want to use Google Translate API instead of the local model, create a `.env` file and add:
```
USE_GOOGLE_TRANSLATE=true
GOOGLE_TRANSLATE_API_KEY=your_api_key_here
```

## Usage

1. Start the web interface:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. The system will automatically start listening for GGwave signals and display translated Arabic text in real-time.

## Translation Options

The system supports two translation methods:

1. Local Translation (Default):
   - Uses the MarianMT model (Helsinki-NLP/opus-mt-en-ar)
   - Works offline after initial model download
   - No API key required
   - Suitable for privacy-sensitive applications

2. Google Translate API (Optional):
   - Requires internet connection
   - Requires API key
   - May provide more accurate translations for some cases
   - Enable by setting environment variables (see Installation step 4)

## Project Structure

```
.
├── app.py                  # Main Flask application
├── src/
│   ├── ggwave_listener.py # GGwave signal processing
│   ├── translator.py      # Translation service
│   └── utils.py          # Utility functions
├── static/               # Static web files
├── templates/           # HTML templates
└── requirements.txt    # Project dependencies
```

## Configuration

You can adjust various parameters in `config.py`:
- Signal processing parameters
- Translation model selection
- UI refresh rate
- Audio device settings

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GGwave SDK developers
- Hugging Face team for translation models
- Flask framework contributors 
from flask import Flask, render_template, jsonify
from src.ggwave_listener import GGwaveListener
from src.translator import Translator
import queue
import threading
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Global message queue for storing translations
message_queue = queue.Queue()

# Initialize components with local translation by default
# Only use Google Translate if explicitly configured
use_google_translate = os.getenv("USE_GOOGLE_TRANSLATE", "").lower() == "true"
translator = Translator(use_local=not use_google_translate)

def translation_callback(text):
    """Callback function for handling decoded GGwave messages."""
    if text:
        # Translate the text to Arabic
        translated = translator.translate(text)
        if translated:
            # Add both original and translated text to the queue
            message_queue.put({
                "original": text,
                "translated": translated,
                "timestamp": ""  # You could add a timestamp here if needed
            })

# Initialize GGwave listener with our callback
listener = GGwaveListener(callback=translation_callback)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/messages')
def get_messages():
    """API endpoint to get new messages."""
    messages = []
    while not message_queue.empty():
        try:
            messages.append(message_queue.get_nowait())
        except queue.Empty:
            break
    return jsonify(messages)

@app.route('/start')
def start_listening():
    """Start the GGwave listener."""
    try:
        listener.start()
        return jsonify({"status": "success", "message": "Listening started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop')
def stop_listening():
    """Stop the GGwave listener."""
    try:
        listener.stop()
        return jsonify({"status": "success", "message": "Listening stopped"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def cleanup():
    """Cleanup function to be called when the application exits."""
    listener.stop()

if __name__ == '__main__':
    try:
        # Start the Flask app
        app.run(debug=True, use_reloader=False)
    finally:
        cleanup() 
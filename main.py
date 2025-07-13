from flask import Flask, request, send_file
from flask_cors import CORS
import os
import tempfile
from pydub import AudioSegment
from pydub.effects import speedup

app = Flask(__name__)
CORS(app)

@app.route("/clone", methods=["POST"])
def clone():
    voice_file = request.files['voice']
    style = request.form.get('style', 'robot')

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, "input.wav")
    output_path = os.path.join(temp_dir, "output.wav")

    voice_file.save(input_path)
    sound = AudioSegment.from_file(input_path)

    if style == "child":
        sound = speedup(sound, 1.5)
    elif style == "robot":
        sound = sound.low_pass_filter(400).high_pass_filter(1000)
    elif style == "old":
        sound = sound.low_pass_filter(1000)
    elif style == "cinematic":
        sound = sound + 6
    elif style == "sad":
        sound = speedup(sound, 0.8)

    sound.export(output_path, format="wav")
    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
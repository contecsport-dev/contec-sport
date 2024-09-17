import os
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
import logging
import imghdr

load_dotenv()  # This loads the variables from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Verify that the file is actually an image
        if imghdr.what(filepath) not in ALLOWED_EXTENSIONS:
            os.remove(filepath)
            return jsonify({'error': 'Invalid image file'}), 400
        
        description = request.form.get('description', '')
        try:
            analysis = analyze_image(filepath, description)
            return jsonify({'analysis': analysis})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file type'}), 400

def analyze_image(filepath, description):
    try:
        with open(filepath, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        logging.info(f"Analyzing image: {filepath}")
        logging.info(f"Description: {description}")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a VFX expert assistant. Analyze the provided image and give a detailed breakdown of the VFX techniques used, designed to assist video editors in understanding and replicating visual effects seen in screenshots or frames from videos. It will analyze uploaded images, identify the visual effects present, and provide detailed, step-by-step guidance on how to recreate these effects using Adobe Premiere or Adobe After Effects. The GPT will focus on breaking down complex visual effects into manageable steps, offering tips and techniques specific to these software platforms. It will cater to both novice and experienced editors, ensuring clarity and comprehensiveness in its explanations.."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze this image for VFX techniques. User description: {description}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        analysis = response.choices[0].message.content
        logging.info(f"Analysis result: {analysis}")
        return analysis
    except Exception as e:
        logging.error(f"Error in analyze_image: {str(e)}")
        return f"An error occurred during image analysis: {str(e)}"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)


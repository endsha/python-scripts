from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import base64
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app


@app.route('/convert', methods=['POST'])
def convert_image_to_base64():
    try:
        data = request.json
        image_url = data.get('image_url')
        if not image_url:
            return jsonify({'error': 'Image URL is required'}), 400

        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch the image from the URL'}), 400

        # Convert the image content to Base64
        base64_encoded = base64.b64encode(response.content).decode('utf-8')

        # Create a data URI for rendering in an HTML img tag
        # Get the MIME type of the image
        mime_type = response.headers['Content-Type']
        data_uri = f"data:{mime_type};base64,{base64_encoded}"

        return jsonify({'base64': data_uri}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

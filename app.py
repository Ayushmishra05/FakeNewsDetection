from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fake News detection function (replace with your actual model logic)
def check_fake_news(text):
    predict = PredictionPipeline()
    predicted = predict.predict(text)
    if predicted[0] == 0 :
        return True
    return False

@app.route('/detect_fake_news', methods=['POST'])
def detect_fake_news():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Perform Fake News detection
    is_fake = check_fake_news(text)

    return jsonify({"isFake": is_fake, "text": text})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

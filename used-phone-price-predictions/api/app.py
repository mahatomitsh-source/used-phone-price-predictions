from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = pickle.load(open("models/used_phone.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

@app.route("/")
def home():
    return {
        "message": "Used Phone Price Prediction API Running"
    }

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["features"]

        # Convert to numpy array
        data = np.array(data).reshape(1, -1)

        # Check feature length
        if data.shape[1] != 8:
            return jsonify({
                "error": f"Expected 8 features, got {data.shape[1]}"
            })

        # Scale data
        data = scaler.transform(data)

        # Predict
        prediction = model.predict(data)

        return jsonify({
            "predicted_price": float(prediction[0])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
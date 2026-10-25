
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "model_bundle.joblib"

bundle = joblib.load(MODEL_PATH)
model = bundle["pipeline"]
features = bundle["features"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "model": "XGBoost",
        "model_version": bundle.get("model_version", "1.0"),
        "features_required": len(features)
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object containing features."}), 400

    missing = [feature for feature in features if feature not in data]

    if missing:
        return jsonify({
            "error": "Some required features are missing.",
            "missing_features": missing
        }), 400

    try:
        input_data = pd.DataFrame(
            [[float(data[feature]) for feature in features]],
            columns=features
        )

        prediction = int(model.predict(input_data)[0])

        return jsonify({
            "prediction": prediction,
            "result": "Correct movement" if prediction == 1 else "Incorrect movement"
        })

    except (TypeError, ValueError) as error:
        return jsonify({"error": f"Invalid feature values: {error}"}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# List of valid crops
VALID_CROPS = {
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans',
    'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 'grapes',
    'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton',
    'jute', 'coffee'
}

# Load fertilizer data
fertilizer_df = pd.read_csv("fertilizer.csv").set_index("Crop")

# Core logic
def check_soil_moisture(crop, moisture):
    crop = crop.lower()

    if crop not in VALID_CROPS:
        return f"❌ Unsupported crop '{crop}'. Please choose from: {', '.join(sorted(VALID_CROPS))}"

    if crop not in fertilizer_df.index:
        return f"❌ Crop '{crop}' not found in the fertilizer database."

    ideal_moisture = fertilizer_df.loc[crop, "soil_moisture"]

    if moisture < ideal_moisture:
        return f"🌱 Soil moisture is low. Ideal for {crop} is {ideal_moisture}%. Please irrigate."
    elif moisture == ideal_moisture:
        return f"✅ Soil moisture is perfect for {crop} ({ideal_moisture}%)."
    elif moisture > ideal_moisture + 10:
        return f"⚠️ Soil moisture is too high! Ideal: {ideal_moisture}%. ⚠️ Recommendation: Harvest the crop, it's at a risk of getting damage."
    else:
        return f"💧 Soil moisture is a bit high (Ideal: {ideal_moisture}%). Avoid overwatering."

# API route
@app.route('/check_moisture', methods=['POST'])
def check_moisture():
    data = request.get_json()

    crop = data.get("crop")
    moisture = data.get("moisture")

    if not crop or moisture is None:
        return jsonify({"error": "Both 'crop' and 'moisture' are required."}), 400

    try:
        moisture = float(moisture)
    except ValueError:
        return jsonify({"error": "'moisture' should be a number."}), 400

    result = check_soil_moisture(crop, moisture)
    return jsonify({"recommendation": result})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

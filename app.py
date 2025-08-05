from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# ✅ Load the retrained model and scaler
model = joblib.load('xgboost_attrition_model_7features.joblib')
scaler = joblib.load('scaler_7features.joblib')

# ✅ Homepage
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Prediction route
@app.route('/predict', methods=['POST'])
def predict():
      



    

          

    try:
        # 🎯 Get form data
        age = int(request.form['Age'])
        distance = float(request.form['DistanceFromHome'])
        education = int(request.form['Education'])
        joblevel = int(request.form['JobLevel'])
        gender = request.form['Gender']  # Male / Female
        monthly_income = float(request.form['MonthlyIncome'])
        overtime = request.form['OverTime']  # Yes / No

        # 🔁 Encode gender and overtime
        gender_encoded = 1 if gender == 'Male' else 0
        overtime_encoded = 1 if overtime == 'Yes' else 0

        # 🔢 Combine inputs
        input_data = np.array([[age, distance, education, joblevel, gender_encoded, monthly_income, overtime_encoded]])

        # 🔍 Scale input
        input_scaled = scaler.transform(input_data)

        # 🤖 Make prediction
        prediction = model.predict(input_scaled)[0]

        # 🟢 Prepare output
        if prediction == 1:
            result = "✅ Yes, this employee is likely to leave."
        else:
            result = "No, this employee is likely to stay."

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



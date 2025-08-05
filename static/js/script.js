document.getElementById('attritionForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  
  // Convert form data to JSON object
  const data = {};
  formData.forEach((value, key) => {
    // Convert categorical to numeric
    if (key === 'Gender') {
      data[key] = value === 'Male' ? 1 : 0;
    } else if (key === 'OverTime') {
      data[key] = value === 'Yes' ? 1 : 0;
    } else {
      data[key] = Number(value);
    }
  });

  // Show loading text
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = "🔄 Predicting...";
  resultDiv.style.color = 'black';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const result = await response.json();

    // Show prediction result
    if (result.prediction === 1) {
      resultDiv.textContent = "⚠️ Employee is likely to leave.";
      resultDiv.style.color = 'red';
    } else {
      resultDiv.textContent = "✅ Employee is likely to stay.";
      resultDiv.style.color = 'green';
    }
  } catch (error) {
    resultDiv.textContent = `❌ Error: ${error.message}`;
    resultDiv.style.color = 'red';
  }
});

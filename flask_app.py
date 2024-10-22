# flask_app.py

from flask import Flask, request, jsonify
from model import InvestmentCalculator

app = Flask(__name__)

# Define the API endpoint
@app.route("/calculate", methods=["POST"])
def calculate_investment():
    # Get data from POST request
    data = request.json
    monthly_saving = data.get("monthly_saving")
    number_of_period = data.get("number_of_period")
    interest_rate = data.get("interest_rate")
    starting_amount = data.get("starting_amount")
    expected_total_return = data.get("expected_total_return")
    scheme = data.get("scheme")

    # Create an instance of InvestmentCalculator
    calculator = InvestmentCalculator(monthly_saving, interest_rate, starting_amount, number_of_period, expected_total_return)
    
    if scheme == "By Expected Return":
        number_of_period = calculator.calculate_period()
        
    else:
        calculator.calculate_apy_return()

    # Prepare the response data
    summary = calculator.get_summary()
    savings_breakdown = calculator.get_savings_breakdown().to_dict(orient="records")

    # Return the results as JSON
    return jsonify({
        "summary": summary,
        "savings_breakdown": savings_breakdown
    })

if __name__ == "__main__":
    app.run(debug=True)

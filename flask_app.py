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

    # Create an instance of InvestmentCalculator
    calculator = InvestmentCalculator(monthly_saving, number_of_period, interest_rate, starting_amount)
    
    # Perform the calculation
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

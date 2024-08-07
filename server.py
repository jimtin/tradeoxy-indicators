from sanic import Sanic
from sanic.response import text
import sanic
import helper_functions as helpers
import json as json

app = Sanic("IndicatorsApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, World!")


# Function to receive an indicator specification and calculate it
@app.post("/calc-indicator")
async def calc_indicator(request):
    # Get the request json
    data = request.json
    # Check that the indicator_name is in the request
    if "indicator_name" not in data or data["indicator_name"] == "" or data["indicator_name"] is None:
        return sanic.json({"error": "Indicator name not found in request"})
    # Check that the parameters are in the request
    if "parameters" not in data or data["parameters"] == "" or data["parameters"] is None:
        return sanic.json({"error": "Parameters not found in request"})
    # Make sure that the parameters a list of dictionaries
    if not isinstance(data["parameters"], list):
        return sanic.json({"error": "Parameters must be a list of dictionaries"})
    # Make sure that the parameters are not empty
    if len(data["parameters"]) == 0:
        return sanic.json({"error": "Parameters cannot be empty"})
    # Make sure that all the parameters are dictionaries
    for param in data["parameters"]:
        if not isinstance(param, dict):
            return sanic.json({"error": "Parameters must be a list of dictionaries"})
    # Make sure that all the keys are lowercase
    for param in data["parameters"]:
        param = {k.lower(): v for k, v in param.items()}
    # Check that the indicator has a value_column parameter
    value_column_found = False
    for param in data["parameters"]:
        if "value_column" in param:
            value_column_found = True
    if not value_column_found:
        return sanic.json({"error": "Value column parameter not found in parameters"})
    # Check that the data is in the request
    if "data" not in data or data["data"] == "" or data["data"] is None:
        return sanic.json({"error": "Data not found in request"})
    # Check that the parameters are valid for the indicator
    check_result = helpers.check_parameters(
        indicator_name=data["indicator_name"], 
        parameters=data["parameters"]
    )
    # If the check returns an error, return the error
    if check_result["outcome"] == "error":
        return sanic.json(check_result)
    # If the check returns success, calculate the indicator
    if check_result["outcome"] == "success":
        # Calculate the indicator
        result = helpers.calculate_indicator(
            indicator_name=data["indicator_name"], 
            parameters=data["parameters"],
            data=data["data"]
        )
        return sanic.json(result)
    else:
        return sanic.json({"error": "Unknown error"})
    
    
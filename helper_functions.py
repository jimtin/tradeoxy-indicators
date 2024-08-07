import json
import indicators


# Function to check the parameters for an indicator type
def check_parameters(indicator_name: str, parameters: json) -> json:
    """
    Check that the parameters for an indicator are valid
    :param indicator_name: The name of the indicator to check
    :param parameters: The parameters for the indicator
    :return: A dictionary with the result of the check
    """
    # Retrieve the indicator parameters from the indicator_params.json file
    with open("indicator_params.json") as f:
        indicator_params = json.load(f)
    # Extract the indicators
    indicators = indicator_params["indicators"]
    # Iterate through the indicators to find the required parameters
    for indicator in indicators:
        if indicator["indicator_name"] == indicator_name:
            required_params = indicator["params"]
            # Iterate through the required parameters
            for param in required_params:
                # Check that the value of the 'name' key is a key in the parameters
                param_name = param["name"]
                param_type = param["value_type"]
                for param in parameters:
                    if param_name in param:
                        # Check the value of the parameter matches the required type
                        if param_type == "int":
                            if not isinstance(param[param_name], int):
                                return {
                                    "outcome": "error",
                                    "error": f"Parameter {param_name} must be an integer"
                                }
                        else:
                            return {
                                "outcome": "error",
                                "error": f"Parameter type {param_type} not recognized"
                            }
                        # Return success if all the parameters are valid
                        return {
                            "outcome": "success"
                        }
                    else:
                        return {
                            "outcome": "error",
                            "error": f"Parameter {param_name} not found"
                        }
                    
    # If the indicator is not found, return an error
    return {
        "outcome": "error",
        "error": "Indicator not found"
    }


# Function to calculate the indicator
def calculate_indicator(indicator_name: str, parameters: json, data: json) -> json:
    """
    Calculate the indicator for the given parameters
    :param indicator_name: The name of the indicator to calculate
    :param parameters: The parameters for the indicator
    :return: The result of the indicator calculation
    """
    # If the indicator is RSI, calculate the RSI
    if indicator_name == "rsi":
        period = 14
        value_column = "close"
        # Iterate through the parameters list to find the period column and value column
        for param in parameters:
            if "period" in param:
                period = param["period"]
            if "value_column" in param:
                value_column = param["value_column"]
        try:
            indicator = indicators.rsi(
                value_column=value_column,
                period=period,
                data=data
            )
            return indicator
        except Exception as exception:
            return {"error": f"Error calculating the RSI value in the helper_functions file. Exception: {str(exception)}"}
    else:
        return {"error": "Indicator not found"}
            
    

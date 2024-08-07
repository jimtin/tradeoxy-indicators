import pandas_ta
import json
import pandas



# Function to calculate the RSI
def rsi(value_column: str, period: int, data: json) -> json:
    """
    Calculate the RSI for a given dataset
    :param value_column: The column name of the value to calculate the RSI for
    :param period: The period to calculate the RSI over
    :param data: The data to calculate the RSI for
    :return: The RSI for the given data
    """
    # Attempt to convert the data to a pandas DataFrame
    try:
        data = pandas.DataFrame(data)
    except Exception as e:
        return {
            "outcome": "error",
            "error": "Data could not be converted to a DataFrame"
        }
    # Check that the value column exists in the data
    if value_column not in data.columns:
        return {
            "outcome": "error",
            "error": "Value column not found in data"
        }
    # Check that the length of the data is greater than the period
    if len(data) < period:
        return {
            "outcome": "error",
            "error": "Data length is less than the period"
        }
    # Calculate the RSI using the TA-Lib library
    rsi_values = pandas_ta.rsi(
        close=data[value_column],
        length=period
    )
    # Append the RSI values to the data
    data["rsi"] = rsi_values
    # Return the data with the RSI values
    return data.to_dict(orient="records")


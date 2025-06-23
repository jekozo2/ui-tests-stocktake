from typing import Union


def format_to_two_decimal_string(value: Union[str, float]) -> str:
    """
    Converts a float or numeric string to a string with exactly two decimal places,
    preserving trailing zeroes (e.g., '9.9' -> '9.90', 12 -> '12.00').

    Args:
        value (Union[str, float]): The input number as a float or string.

    Returns:
        str: The formatted string with two decimal places.

    Raises:
        ValueError: If the input cannot be converted to a float.
    """
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid input for formatting: {value!r}")

    return f"{numeric_value:.2f}"

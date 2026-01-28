def calculator_tool(expression: str) -> str:
    """
    Simple calculator tool for mathematical expressions
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        str: Result of the calculation or error message
    """
    try:
        # Basic safety check - only allow mathematical operations
        allowed_chars = set('0123456789+-*/(). ')
        if not set(expression).issubset(allowed_chars):
            return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed."
        
        # Evaluate the expression
        result = eval(expression)
        return f"{result}"
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error: {str(e)}"


def text_length_tool(text: str) -> str:
    """
    Tool to count characters in text
    
    Args:
        text (str): Text to count characters for
        
    Returns:
        str: Number of characters in the text
    """
    try:
        char_count = len(text)
        return f"{char_count}"
    except Exception as e:
        return f"Error: {str(e)}"


def uppercase_tool(text: str) -> str:
    """
    Tool to convert text to uppercase
    
    Args:
        text (str): Text to convert to uppercase
        
    Returns:
        str: Text converted to uppercase
    """
    try:
        return text.upper()
    except Exception as e:
        return f"Error: {str(e)}"

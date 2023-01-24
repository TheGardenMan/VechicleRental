"""
Custom error classes
"""


class APIError(Exception):
    def __init__(self, message: str = "Error", status: int = 400) -> None:
        # Custom Exception class.
        # Caught by vechiclerental\api\middleware.py
        self.message = message
        self.status = status

class UserWithNoInfosException(Exception):
    """Exception raised when data is not found in the database."""

    def __init__(self, message="O usuario foi cadastrado com as informacoes necessarias incompletas."):
        self.message = message
        super().__init__(self.message)

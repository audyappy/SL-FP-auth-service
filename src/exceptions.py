class ServiceException(Exception):
    """Base class for all service exceptions."""
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}

class NotFoundException(ServiceException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)
        
class ForeignConstraintException(ServiceException):
    def __init__(self, message="Foreign constraint violation"):
        # super().__init__(message, status_code=409)  # 409 Conflict
        super().__init__(message, status_code=400)

class CreationFailedException(ServiceException):
    def __init__(self, message="Failed to create resource"):
        # super().__init__(message, status_code=422)  # 422 Unprocessable Entity
        super().__init__(message, status_code=400)

class ValidationFailedException(ServiceException):
    def __init__(self, message="Validation failed"):
        super().__init__(message, status_code=400)
        
class UnauthorizedException(ServiceException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)
    
class UserNotFound(ServiceException):
    def __init__(self, message="User not found"):
        super().__init__(message, status_code=404)
        
class InvalidPassword(ServiceException):
    def __init__(self, message="Invalid password"):
        super().__init__(message, status_code=401)
        
class BadRequestToExternalService(ServiceException):
    def __init__(self, message="Bad request to external service"):
        super().__init__(message, status_code=400)
        
        
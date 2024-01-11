class Unauthorized(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)
        
class NotFound(Exception):
    def __init__(self, message="NotFound"):
        self.message = message
        super().__init__(self.message)
def log_info(msg:str, data: dict[str, any]):
    print(msg,data)
    
def log_error(error: Exception, msg:str, data: dict[str, any]):
    print(error, msg, data)
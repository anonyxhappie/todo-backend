class Constants:

    """
    Constant is class used to store all string literals
    """
    
    EXCEPTION_CODES = {
        'DEFAULT': [10000, 'There is some error in service, please try again'],
        'INVALID_REQUEST': [10001, 'Request data is invalid'],
        'DATABASE_READ_ERROR': [10002, 'An error occured while reading database'],
        'DATABASE_WRITE_ERROR': [10003, 'An error occured while writing in database'],
        'BUCKET_NAME_EXIST': [10011, 'Bucket name already exist'],
        'INVALID_BUCKET_ID': [10012, 'Invalid Bucket ID'],
        'INVALID_TODO_ITEM_ID': [10013, 'Invalid Todo Item ID']
    }
    MESSAGE = 'message'
    RESULT = 'result'
    STATUS = 'status'
    ERROR = 'error'
    
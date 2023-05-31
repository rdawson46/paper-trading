import re
from datetime import datetime
from pytz import timezone

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def validPass(pwd:str)->bool:
    """
    validates that the password entered meets the security criteria 
    """
    return bool(pwd)

# made with regex, will need to replace
def validEmail(email:str)->bool:
    """
    uses regex to check if the email passed is a valid email

    method will be changed
    """
    if(re.fullmatch(regex, email)):
        return True
    return False


def isValidTime()->bool:
    """
    determines if it is during trading hours
    """
    time = datetime.now(timezone('US/Eastern')).hour
    return  time >= 9 and time < 17


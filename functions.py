import re

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
password_regex = r"\b \b"

def validPass(pwd:str)-> bool:
    """
    validates that the password entered meets the security criteria
    """
    # HACK: might work, might not
    if not re.search(r'[A-Z]', pwd):
        return False
    if not re.search(r'[0-9]', pwd):
        return False
    return bool(pwd)

# made with regex, will need to replace
def validEmail(email:str)->bool:
    """
    uses regex to check if the email passed is a valid email

    method will be changed
    """
    if(re.fullmatch(email_regex, email)):
        return True
    return False

import requests

# authenticate user function
def user_authenticator(email, password, required_scope = None, request = None):
    print(f"Authenticating user with email: {email} and password: {password}") # print log
    request = requests.post('https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users',json={'email': email, 'password': password}) # creating request

    if request.ok and request.text.find("True") != -1:
        return {"validated email": email, "validated password": password} # return validated email and password if ok
    return None

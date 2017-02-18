import re
from classes.error import Error


def validate_email_data(email, min=1, max=25):
    errors = []
    email = email.strip()
    if (len(email) < min):
        error = Error("Email", "Email cannot be empty")
        errors.append(error)
    if (len(email) > max):
        error = Error("Email", "Email cannot be longer than " +
                      str(max) + " characters.")
        errors.append(error)
    if (not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)):
        error = Error("Email", "Email" + " should follow the following format: example@example.com")
        errors.append(error)
    return errors

def validate_text_data(text, id, min=1, max=25):
    errors = []
    text = text.strip()
    if (len(text) < min):
        error = Error(id, id + " cannot be shorter than " +
                      str(min) + " characters.")
        errors.append(error)
    if (len(text) > max):
        error = Error(id, id + " cannot be longer than " +
                      str(max) + " characters.")
        errors.append(error)
    if (not re.match(r"^[a-zA-Z0-9]*$", text)):
        error = Error(id, id + " should include only alpha-numeric characters")
        errors.append(error)
    return errors


def validate_password_data(password, repeat_password,  min=6, max=32):
    errors = []
    password = password.strip()
    repeat_password = repeat_password.strip()
    if (len(password) < min):
        error = Error("Password", "Password" + " cannot be shorter than " +
                      str(min) + " characters.")
        errors.append(error)
    if (len(password) > max):
        error = Error("Password", "Password" + " cannot be longer than " +
                      str(max) + " characters.")
        errors.append(error)
    if (not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$", password)):
        error = Error("Password", "Password" + " should include at " +
                      "least one small case letter, at least one capital case letter, " +
                      "at least one number and at least one following special characters: " +
                      " -+_!@#$%^&*.,?")
        errors.append(error)
    if (len(repeat_password) > 0 and password != repeat_password):
        error = Error("Repeat Password", "Confirm password does not match.")
        errors.append(error)
    return errors

def validate_login_data(_user):
    errors = []
    errors.extend(validate_email_data(_user.email, 1, 250))
    errors.extend(validate_password_data(_user.password, ''))
    return errors

def validate_user_data(_user, repeat_password):
    errors = []
    errors.extend(validate_text_data(_user.first_name, "First Name"))
    errors.extend(validate_text_data(_user.last_name, "Last Name"))
    errors.extend(validate_text_data(_user.username, "Username", 6, 32))
    errors.extend(validate_email_data(_user.email, 1, 250))
    errors.extend(validate_password_data(_user.password, repeat_password))
    return errors

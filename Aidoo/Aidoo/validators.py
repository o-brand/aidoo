from profanity.validators import validate_is_profane


def validate_profanity(value):
    """The default profanity validator has an issue where it believes that
    strings ending with ' a' is profanity. This additional validator
    makes an exception for such strings before calling the validator"""

    if len(value) == 0:
        return
    elif len(value) == 1:
        return
    else:
        if value[-2] + value[-1] == " a":
            value = value[0 : len(value) - 1]
            validate_is_profane(value)
        else:
            validate_is_profane(value)

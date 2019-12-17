class LoginException(Exception):
    """Exception that is thrown when wrong credentials have been provided

    """
    pass


class UnknownStatusException(Exception):
    """Exception that is thrown when an unknown status has been return from a requests call

    """
    pass


class NotLoggedInException(Exception):
    """Exception that is thrown when a requests call has been made without being authenticated

    """

    pass


def encode(unencoded):
    """Encoding function for the username and password.

    This is an implementation of the Base64 encoding with some minor
    quirks, like input '' returns 'AA==' while Base64 returns '' in that case. It is a Python implementation for the
    encode function found in index.htm on the modem

    Args:
        unencoded (str): unencoded string value

    Returns:
        str: The 'Base64' encoded string value

    """
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    encoded = ""

    i = 0

    while True:
        chr0 = ord(unencoded[i]) if i < len(unencoded) else 0
        chr1 = ord(unencoded[i + 1]) if i < len(unencoded) - 1 else 0
        chr2 = ord(unencoded[i + 2]) if i < len(unencoded) - 2 else 0

        enc1 = lookup[chr0 >> 2]
        enc2 = lookup[((chr0 & 3) << 4) | (chr1 >> 4)]
        if chr1 == 0:
            enc3 = enc4 = lookup[64]
        elif chr2 == 0:
            enc3 = lookup[((chr1 & 15) << 2)]
            enc4 = lookup[64]
        else:
            enc3 = lookup[((chr1 & 15) << 2) | (chr2 >> 6)]
            enc4 = lookup[chr2 & 63]

        encoded = f'{encoded}{enc1}{enc2}{enc3}{enc4}'

        i = i + 3
        if i >= len(unencoded):
            break

    return encoded

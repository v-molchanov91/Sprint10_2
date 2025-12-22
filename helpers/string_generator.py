import random
import string


class StringGenerator:
    @staticmethod
    def alphanumeric(length=10):
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choices(chars, k=length))

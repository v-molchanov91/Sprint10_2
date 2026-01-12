from faker import Faker
import random
import string


fake = Faker("ru_RU")


class UserGenerator:
    @staticmethod
    def _generate_password(length=12):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def generate_user_data(email=None, password=None, name=None):
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        final_name = name or full_name

        if email is None:
            username = f"{first_name.lower()}.{last_name.lower()}"
            domain = random.choice(["yandex.ru", "mail.ru", "gmail.com", "bk.ru"])
            final_email = f"{username}@{domain}"
        else:
            final_email = email

        final_password = password or UserGenerator._generate_password()

        return {
            "name": final_name,
            "email": final_email,
            "password": final_password,
            "submitPassword": final_password,
        }

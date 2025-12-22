class Error:
    EMAIL_ALREADY_USED = "Почта уже используется"


class AssertMessages:
    STATUS_CODE_MISMATCH = "Ожидался статус код {expected}, получен {actual}"
    ERROR_MESSAGE_MISMATCH = "Ожидалось сообщение: '{expected}', получено: '{actual}'"
    FIELD_MISSING = "В ответе отсутствует поле {field_name}"
    FIELD_VALUE_MISMATCH = "Ожидалось {field_name}: '{expected}', получено: '{actual}'"

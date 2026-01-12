class URLs:
    BASE_URL = "https://qa-desk.stand.praktikum-services.ru/api"

    USER_CREATE_URL = f"{BASE_URL}/signup"
    USER_LOGIN_URL = f"{BASE_URL}/signin"

    LISTING_CREATE_URL = f"{BASE_URL}/create-listing"
    LISTING_UPDATE_URL = f"{BASE_URL}/update-offer/{{}}"
    LISTING_DELETE_URL = f"{BASE_URL}/listings/{{}}"

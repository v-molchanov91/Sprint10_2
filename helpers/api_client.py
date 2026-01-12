import requests
from data.config import URLs


class ApiClient:
    @staticmethod
    def post_request_create_user(payload):
        return requests.post(URLs.USER_CREATE_URL, json=payload)

    @staticmethod
    def post_request_login_user(payload):
        return requests.post(URLs.USER_LOGIN_URL, json=payload)

    @staticmethod
    def post_request_create_listing(headers, data, image_path=None):
        files = []

        for key, value in data.items():
            files.append((key, (None, str(value))))

        image_file = None
        if image_path:
            try:
                image_file = open(image_path, "rb")
                filename = image_file.name.split("/")[-1]
                files.append(("image", (filename, image_file, "image/jpeg")))
            except Exception as e:
                if image_file:
                    image_file.close()
                raise e
        try:
            return requests.post(URLs.LISTING_CREATE_URL, headers=headers, files=files)
        finally:
            if image_file and not image_file.closed:
                image_file.close()

    @staticmethod
    def patch_request_update_listing(headers, listing_id, data, image_path=None):
        files = {}

        for key, value in data.items():
            files[key] = (None, str(value))

        image_file = None
        if image_path:
            try:
                image_file = open(image_path, "rb")
                filename = image_file.split("/")[-1]
                files["image"] = (filename, image_file, "image/jpeg")
            except Exception as e:
                if image_file:
                    image_file.close()
                raise e

        url = URLs.LISTING_UPDATE_URL.format(listing_id)
        try:
            return requests.patch(url, headers=headers, files=files)
        finally:
            if image_file and not image_file.closed:
                image_file.close()

    @staticmethod
    def delete_request_delete_listing(headers, listing_id):
        url = URLs.LISTING_DELETE_URL.format(listing_id)
        return requests.delete(url, headers=headers)

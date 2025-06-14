import requests
from typing import Any
from os import path

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


class MyAutoDownloader:
    def __download_image(self, source: str, dest: str) -> None:
        response = requests.get(source, stream=True, headers=headers)
        response.raise_for_status()
        with open(dest, "wb") as dest_file:
            for chunk in response:
                dest_file.write(chunk)

    def __get_api_endpoint(self, page_number: int) -> str:
        return f"https://api2.myauto.ge/ka/products?TypeID=0&ForRent=&Mans=&CurrencyID=3&MileageType=1&Page={page_number}"

    # TODO: avoid Any
    def __make_api_request(self, url: str) -> dict[str, Any]:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def __get_image_urls_from_item(self, item: dict[str, Any]) -> list[str]:
        image_list: list[str] = []
        car_id = item["car_id"]
        photo = item["photo"]
        pic_number = item["pic_number"]
        for id in range(1, pic_number + 1):
            image_url = (
                f"https://static.my.ge/myauto/photos/{photo}/large/{car_id}_{id}.jpg"
            )
            image_list.append(image_url)
        return image_list

    def __get_image_list(self, page_number: int) -> list[str]:
        response = self.__make_api_request(self.__get_api_endpoint(page_number))

        image_list: list[str] = []
        for item in response["data"]["items"]:
            image_list += self.__get_image_urls_from_item(item)
        return image_list

    def download_images(self, page_number: int, output_folder: str) -> None:
        image_list = self.__get_image_list(page_number)
        for item in image_list:
            dest = path.join(output_folder, item.split("/")[-1:][0])
            self.__download_image(item, dest)

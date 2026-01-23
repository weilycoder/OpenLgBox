import json
import requests

from typing import Any, Optional

from bs4 import BeautifulSoup


class LuoguAPI(object):
    def __init__(
        self,
        *,
        proxy: Optional[str] = None,
        headers: Optional[dict[str, str | bytes | None]] = None,
        uid: Optional[int] = None,
        client_id: Optional[str] = None,
        timeout: int = 8,
    ) -> None:
        self.proxy = proxy
        self.headers = (
            headers
            if headers is not None
            else {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        self.uid = uid
        self.client_id = client_id

        self.timeout = timeout

    @property
    def cookies(self) -> dict[str, str]:
        cookies = {}
        if self.uid:
            cookies["_uid"] = str(self.uid)
        if self.client_id:
            cookies["__client_id"] = self.client_id
        return cookies

    def get_response(self, url: str) -> requests.Response:
        response = requests.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
            proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None,
        )
        response.raise_for_status()
        return response

    def fetch_user_data(self, target: int) -> dict[str, Any]:
        url = f"https://www.luogu.com.cn/user/{target}"
        response = self.get_response(url)

        soup = BeautifulSoup(response.text, "html.parser")

        script_tag = soup.find("script", id="lentille-context", type="application/json")

        if script_tag and script_tag.string:
            json_data = json.loads(script_tag.string.strip())
            return json_data["data"]
        else:
            raise ValueError("Could not find the required script tag in the HTML.")

    def get_user_achievements(self, target: int) -> dict[str, Any]:
        user_data = self.fetch_user_data(target)
        return {
            "ccfLevel": user_data["user"]["ccfLevel"],
            "xcpcLevel": user_data["user"]["xcpcLevel"],
            "prizes": user_data["prizes"],
        }

    def search_user(self, target: str) -> tuple[int, str]:
        url = f"https://www.luogu.com.cn/api/user/search?keyword={target}"
        response = self.get_response(url)
        json_data = response.json()
        return json_data["users"][0]["uid"], json_data["users"][0]["name"]


if __name__ == "__main__":
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    user = input("Enter user name: ")
    api = LuoguAPI(
        uid=config.get("uid"),
        client_id=config.get("client_id"),
    )
    user_id, user_name = api.search_user(user)
    data = api.get_user_achievements(user_id)

    print(f"User ID: {user_id}")
    print(f"User Name: {user_name}")
    print(f"ccfLevel: {data['ccfLevel']}")
    print(f"xcpcLevel: {data['xcpcLevel']}")
    print(json.dumps(data["prizes"], indent=4, ensure_ascii=False))

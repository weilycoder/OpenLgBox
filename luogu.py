import json
import requests

from typing import Any, Optional

from bs4 import BeautifulSoup

from util import alias_luogu_contests


def prizes_format(
    prizes: list[dict],
) -> list[tuple[Optional[str], Optional[int], Optional[str], Optional[float], Optional[int]]]:
    formatted_prizes: list[tuple[Optional[str], Optional[int], Optional[str], Optional[float], Optional[int]]] = []
    for prize in prizes:
        data = prize.get("prize", {})
        contest_name = data.get("contest", None)
        contest_year = data.get("year", None)
        if contest_name in alias_luogu_contests:
            contest_name = alias_luogu_contests[contest_name]
        formatted_prizes.append(
            (
                contest_name,
                contest_year,
                data.get("prize", None),
                data.get("score", None),
                data.get("rank", None),
            )
        )
    return formatted_prizes


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
            else {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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

    def get_user_achievements(
        self, target: int
    ) -> tuple[int, int, list[tuple[Optional[str], Optional[int], Optional[str], Optional[float], Optional[int]]]]:
        user_data = self.fetch_user_data(target)
        return (
            user_data["user"]["ccfLevel"],
            user_data["user"]["xcpcLevel"],
            prizes_format(user_data["prizes"]),
        )

    def search_user(self, target: str) -> tuple[int, str]:
        url = f"https://www.luogu.com.cn/api/user/search?keyword={target}"
        response = self.get_response(url)
        json_data = response.json()
        return json_data["users"][0]["uid"], json_data["users"][0]["name"]

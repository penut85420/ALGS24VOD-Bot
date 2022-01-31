import asyncio
import re
from urllib.parse import urlencode

import requests
from twitchio.ext import commands

from ALGS24VOD import CheckVOD, load_json, timestamp


class ALGS24VOD(commands.Bot):
    def __init__(self):
        self._title = None
        self.title = None
        self.channel = None
        self.config = load_json("Config.json")
        super().__init__(
            token=self.config["access_token"],
            prefix="__NoCommandPrefix__",
            initial_channels=[self.config["broadcaster_id"]],
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")

        tasks = [self.monitor_title, self.broadcast_title]
        tasks = [asyncio.create_task(t()) for t in tasks]
        for t in tasks:
            await t

    async def monitor_title(self):
        while True:
            await self.refresh_config()
            if self._title != self.title:
                self.title = self._title
                self.set_channel_title(self.config["title_fmt"] % self.title)
                await self.channel.send(self.config["message_fmt"] % self.title)
            await asyncio.sleep(self.config["timer"])

    async def broadcast_title(self):
        while True:
            await asyncio.sleep(self.config["message_timer"])
            await self.refresh_config()
            await self.channel.send(self.config["message_fmt"] % self._title)

    def set_channel_title(self, title):
        url = f"http://localhost:8080/title?title={title}"
        requests.get(url)

        data = {
            "client_id": self.config["client_id"],
            "redirect_uri": "http://localhost:8080/",
            "response_type": "code",
            "scope": "channel:manage:broadcast",
        }

        url = "https://id.twitch.tv/oauth2/authorize?" + urlencode(data, doseq=True)

        resp = requests.get(url, cookies=self.config["cookie"])
        content = resp.content.decode("UTF-8")
        url = re.search("URL='(http://.+)'", content).groups()[0]

        resp = requests.get(url, cookies=self.config["cookie"])
        print(f'{timestamp()} [{resp.status_code}] Set Title "{title}"')

    async def refresh_config(self):
        self.config = load_json("Config.json")
        while self.channel is None:
            await self.join_channels([self.config["broadcaster_id"]])
            self.channel = self.get_channel(self.config["broadcaster_id"])
        self._title = CheckVOD().check_dir(self.config["target_dir"])


def main():
    ALGS24VOD().run()


if __name__ == "__main__":
    main()

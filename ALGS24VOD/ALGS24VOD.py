import asyncio
import re
from urllib.parse import urlencode

import requests
from twitchio.ext import commands

from ALGS24VOD import CheckVOD, load_json, timestamp


class ALGS24VOD(commands.Bot):
    def __init__(self):
        self.title = None
        self.config = load_json("Config.json")
        super().__init__(
            token=self.config["access_token"],
            prefix="__NoCommandPrefix__",
            initial_channels=[self.config["broadcaster_id"]],
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")
        while len(self.connected_channels) < 1:
            await self.join_channels([self.config["broadcaster_id"]])
        self.channel = self.connected_channels[0]
        await asyncio.create_task(self.monitor_title())

    async def monitor_title(self):
        while True:
            self.config = load_json("Config.json")
            title = CheckVOD().check_dir(self.config["target_dir"])
            if title != self.title:
                self.title = title
                self.set_channel_title(self.config["title_fmt"] % title)
                await self.channel.send(f"現正播放「{title}」")
                await asyncio.sleep(self.config["timer"])

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


def main():
    ALGS24VOD().run()


if __name__ == "__main__":
    main()

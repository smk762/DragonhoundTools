#!/usr/bin/env python3
import discord
import asyncio
import requests
import json
import os
import sys
import time
import datetime
from dotenv import load_dotenv

load_dotenv()
NN_ANN_CHANNEL = int(os.getenv('NN_ANN_CHANNEL'))
TOKEN = os.getenv('TOKEN')

season = "Season_6"
notaries_data = requests.get(f"https://raw.githubusercontent.com/KomodoPlatform/NotaryNodes/master/{season.lower().replace('_', '')}/elected_nn_social.json").json()

nn_pings = {}
for nn in notaries_data:
    for region in notaries_data[nn]["regions"]:
        nn_pings.update({f"{nn}_{region}": f'<@{notaries_data[nn]["discord"]}>'})
unmined_nn_names = list(nn_pings.keys())

r = requests.get(f"http://stats.kmd.io/api/table/addresses/?season={season}&server=Main&coin=KMD")
KMD_addresses_data = r.json()["results"]
KMD_addresses = []
for i in KMD_addresses_data:
    KMD_addresses.append(i["address"])


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(NN_ANN_CHANNEL) # channel ID goes here
        while not self.is_closed():
            try:
                now = int(time.time())
                time_4hrs_ago = now - 60*60*4
                print(f"time_4hrs_ago: {time_4hrs_ago}")
                loop = 0
                while True:
                    r = requests.get(f'https://stats.kmd.io/api/mining/notary_last_mined_table/')
                    try:
                        resp = r.json()['results']
                        not_mined_recently = []
                        not_mined_recently_alert = []
                        msg = "**The following NN have not mined in the last 4 hours...**\n"
                        for item in resp:
                            nn = item["name"]
                            addr = item["address"]
                            print(f"{nn}: {addr} ({item['blocktime']})")
                            print(unmined_nn_names)
                            if nn in unmined_nn_names:
                                print("removing from unmined_nn_names")
                                unmined_nn_names.remove(nn)
                            if item["blocktime"] < time_4hrs_ago:

                                if nn in nn_pings and addr in KMD_addresses:
                                    not_mined_recently.append(nn)
                                    time_since_mined = now - item["blocktime"]
                                    time_since_mined_hms = datetime.timedelta(seconds=time_since_mined)
                                    print(item["blocktime"])
                                    print(now)
                                    print(time_since_mined)
                                    print(time_since_mined_hms)
                                    if nn_pings[nn] == "":
                                        msg += f"{nn} (last mined {time_since_mined_hms} ago)\n"
                                    else:
                                        msg += f"{nn_pings[nn]} ({nn} last mined {time_since_mined_hms} ago)\n"


                        if len(not_mined_recently_alert) > 10:
                          msg = f"<@448777271701143562> Check bot, something's up."

                        elif len(unmined_nn_names) > 0:
                            msg += "**The following NN have not mined yet this season...**\n"
                            for op in unmined_nn_names:
                                if nn_pings[op] == "":
                                    msg += f"{op} ({op} has not mined yet)\n"
                                else:
                                    msg += f"{nn_pings[op]} ({op} has not mined yet)\n"
                        print(not_mined_recently)
                        if len(not_mined_recently) > 0 and msg != "":
                            print("sending alert...")
                            await channel.send(msg)
                            print(msg)
                        break
                    except Exception as e:
                        print(f"{e}")
                        sys.exit()
                        time.sleep(10)
                        loop += 1

                    if loop > 12:
                        print("sending alert...")
                        await channel.send(f"<@448777271701143562> Mining endpoint not responding!\n")
                        break

            except Exception as e:
                print("sending alert...")
                await channel.send(f"<@448777271701143562> Mining endpoint not responding!\n{e}")
            await self.close()


client = MyClient()
client.run(TOKEN)

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

nn_pings = {
    "alien_AR": "<@412323938782150658>",
    "alien_EU": "<@412323938782150658>",
    "alien_NA": "<@412323938782150658>",
    "alienx_EU": "<@412323938782150658>",
    "alienx_NA": "<@412323938782150658>",
    "alrighttt_DEV": "<@405011811511828481>",
    "artem_DEV": "<@457121878465708043>",
    "artempikulin_AR": "<@457121878465708043>",
    "ca333_DEV": "<@375074477756645386>",
    "ca333_EU": "<@375074477756645386>",
    "chmex_AR": "<@420119978138664961>",
    "chmex_EU": "<@420119978138664961>",
    "chmex_SH": "<@420119978138664961>",
    "cipi2_EU": "<@419964976397156352>",
    "cipi_AR": "<@419964976397156352>",
    "cipi_EU": "<@419964976397156352>",
    "cipi_NA": "<@419964976397156352>",
    "collider_SH": "<@558329313490108416>",
    "computergenie_NA": "<@474206298427097099>",
    "dappvader_SH": "<@686210447266807838>",
    "dragonhound_DEV": "<@448777271701143562>",
    "dragonhound_NA": "<@448777271701143562>",
    "drkush_SH": "<@525478463981748239>",
    "gcharang_DEV": "<@423176312354635779>",
    "goldenman_AR": "<@412907089992613888>",
    "hyper_NA": "<@459844460625526824>",
    "karasugoi_NA": "<@426823107865608192>",
    "kolo_AR": "<@458262320775430155>",
    "komodopioneers_EU": "<@375949808772579339>",
    "madmax_AR": "<@380786853558747139>",
    "madmax_EU": "<@380786853558747139>",
    "madmax_NA": "<@380786853558747139>",
    "majora31_SH": "<@712206161356521563>",
    "marmarachain_EU": "<@409990217047474176>",
    "mcrypt_AR": "<@458507065178980353>",
    "mcrypt_SH": "<@458507065178980353>",
    "metaphilibert_SH": "<@368864295397752833>",
    "mrlynch_AR": "<@504735704543395853>",
    "mylo_SH": "<@371114647052615681>",
    "node-9_EU": "<@412482228359266328>",
    "node-9_NA": "<@412482228359266328>",
    "nodeone_NA": "<@>",
    "nutellaLicka_SH": "<@202999072519356416>",
    "ocean_AR": "<@461724153326600206>",
    "pbca26_NA": "<@403229823834521616>",
    "pbca26_SH": "<@403229823834521616>",
    "phit_SH": "<@352577127494713345>",
    "ptyx_NA": "<@303794669945618442>",
    "shadowbit_AR": "<@>",
    "shadowbit_DEV": "<@>",
    "shadowbit_EU": "<@>",
    "sheeba_SH": "<@288941564263268353>",
    "slyris_EU": "<@206445134122844170>",
    "smdmitry_AR": "<@486144655369437184>",
    "smdmitry_EU": "<@486144655369437184>",
    "strob_NA": "<@278565047113089025>",
    "strobnidan_SH": "<@278565047113089025>",
    "strob_SH": "<@278565047113089025>",
    "tokel_AR": "<@>",
    "tonyl_AR": "<@272003866906722306>",
    "tonyl_DEV": "<@272003866906722306>",
    "van_EU": "<@>",
    "webworker01_NA": "<@300741339279130624>",
    "yurii_DEV": "<@668742126992883714>"
 }


NN_ANN_CHANNEL = int(os.getenv('NN_ANN_CHANNEL'))
BTC_FEE_ALERT_PRICE = int(os.getenv('BTC_FEE_ALERT_PRICE'))
TOKEN = os.getenv('TOKEN')

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
                time_16hrs_ago = now - 60*60*16
                loop = 0
                while True:
                    r = requests.get("http://stats.kmd.io/api/table/last_notarised/?season=Season_5&chain=LTC")
                    try:
                        resp = r.json()['results']
                        no_ntx_list = []
                        no_ntx_alert = []
                        msg = "**The following NN have not notarised LTC in the last 16 hours...**\n"
                        for item in resp:
                            if item["block_time"] < time_16hrs_ago:
                                nn = item["notary"]
                                if nn in nn_pings:
                                    no_ntx_list.append(nn)
                                    time_since_ntx = now - item["block_time"]
                                    time_since_ntx_hms = datetime.timedelta(seconds=time_since_ntx)
                                    print(item["block_time"])
                                    print(now)
                                    print(time_since_ntx)
                                    print(time_since_ntx_hms)
                                    if nn_pings[nn] == "":
                                        msg += f"{nn} (last LTC NTX {time_since_ntx_hms} ago)\n"
                                    else:
                                        msg += f"{nn_pings[nn]} ({nn} last LTC NTX {time_since_ntx_hms} ago)\n"
                        if len(no_ntx_alert) > 0:
                          msg = f"<@448777271701143562> Check bot, something's up."

                        elif len(no_ntx_list) > 0 and msg != "":
                            await channel.send(msg)
                            print(msg)
                        break
                    except Exception as e:
                        print(f"{e}")
                        sys.exit()
                        time.sleep(10)
                        loop += 1

                    if loop > 12:
                        await channel.send(f"<@448777271701143562> Last notarised endpoint not responding!\n")
                        break

            except Exception as e:
                await channel.send(f"<@448777271701143562> Mining endpoint not responding!\n{e}")
            # await asyncio.sleep(60*60*4) # task runs every 4 hrs
            await self.close() # or run once and cron


client = MyClient()
client.run(TOKEN)

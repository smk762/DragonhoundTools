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
unmined_nn_names = list(nn_pings.keys())

S5_KMD_addresses = requests.get("http://stats.kmd.io/api/wallet/chain_addresses/?season=Season_5&chain=KMD")
S5_KMD_addresses = S5_KMD_addresses.json()["Season_5"]["Main"]["KMD"]
S5_KMD_addresses = list(S5_KMD_addresses.values())


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
                time_4hrs_ago = now - 60*60*4
                loop = 0
                while True:
                    r = requests.get('http://stats.kmd.io/api/table/last_mined/?season=Season_5')
                    try:
                        resp = r.json()['results']
                        not_mined_recently = []
                        not_mined_recently_alert = []
                        msg = "**The following NN have not mined in the last 4 hours...**\n"
                        for item in resp:
                            nn = item["name"]
                            addr = item["address"]
                            if nn in unmined_nn_names:
                                unmined_nn_names.remove(nn)
                            if item["last_mined_blocktime"] < time_4hrs_ago:
                                if nn in nn_pings and addr in S5_KMD_addresses:
                                    not_mined_recently.append(nn)
                                    time_since_mined = now - item["last_mined_blocktime"]
                                    time_since_mined_hms = datetime.timedelta(seconds=time_since_mined)
                                    print(item["last_mined_blocktime"])
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
            '''
            try:
                loop = 1
                while loop < 10:
                  time.sleep(5)
                  r = requests.get('https://api.blockchair.com/bitcoin/stats')
                  resp = r.json()
                  data = resp['data']
                  btc_suggested_fee = data['suggested_transaction_fee_per_byte_sat']
                  print(btc_suggested_fee > 1)
                  loop += 1
                  if btc_suggested_fee > 1:
                    break
                if btc_suggested_fee < BTC_FEE_ALERT_PRICE:
                    await channel.send(f"BTC Fee at {btc_suggested_fee} sat per byte")
                    pass
                else:
                    await channel.send(f"BTC Fee at {btc_suggested_fee} sat per byte")
            except Exception as e:
                await channel.send(f"<@448777271701143562> BTC Fee endpoint not responding!\n{e}")
            '''
            # await asyncio.sleep(60*60*4) # task runs every 4 hrs
            await self.close() # or run once and cron


client = MyClient()
client.run(TOKEN)

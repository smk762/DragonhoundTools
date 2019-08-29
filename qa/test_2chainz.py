#!/usr/bin/env python3
from qalib import *
paramlist = ["-ac_name=PEGTEST", "-ac_supply=5000", "-ac_reward=800000000",
			  			"-ac_sapling=1,", "-addnode=116.203.120.163", 
			  			"-addnode=116.203.120.91"
			  ]
komodod_path = home+"/Mixa84/komodo/src"
spawn_2chainz('PEGTEST', paramlist, komodod_path)
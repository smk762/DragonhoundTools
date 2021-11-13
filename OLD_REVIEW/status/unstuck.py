#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *
from statslib import *
from nnlib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cc'))
from oracleslib import *
now = time.time()
stats_data = []
forked_list = []
stuck_list = []
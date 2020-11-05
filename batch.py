# coding: utf-8

import discord
import random
import sys
import os
import json
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from lib import (
    config,
    shindan_client,
    log,
    markov
)


markov.raw_data_parse()

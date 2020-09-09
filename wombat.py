"""!wombat returns a random wombat image"""

import re
import requests
from random import randint
from google_images_search import GoogleImagesSearch

def wombat():
    gis = GoogleImagesSearch('AIzaSyACSrWsNWMtPpt9nl59_rAgPSTYU8YSL0Y', '013617714715596442592:tuzubzph_am')
    search_params = {
        'q': 'cute wombat',
        'num': 50,
        'imgType': 'photo',
        'imgSize': 'large',
        'searchType': 'image'
    }
    key = randint(1,50)
    gis.search(search_params=search_params)

    return gis.results[key] 

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!wombat", text)
    if not match:
        return

    return wombat()


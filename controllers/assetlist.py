'''
Created on Mar 28, 2014

@author: Bruno Santos (https://github.com/brunorene)
'''

import os, sys, logging, json
from models.assetlist import Assetlist
#from models.meolist import MeoList
from controllers.assets import AssetController

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

#from meokanal import MKClient
from utils.core import *

log = logging.getLogger()
astControl = AssetController()
#cl = MKClient()

from base import BaseController

class AssetlistController(BaseController):
    def __init__(self):
        super(AssetlistController, self).__init__()

    def get_all_assetlists(self):
        return self.kv.list_assetlists()

    def get_assetlist(self, mac_address):
        return self.kv.get_assetlist(mac_address)

    def set_assetlist(self, mac_address, assets):
        self.kv.set_assetlist(mac_address, Assetlist(mac_address, assets))

    def delete_assetlist(self, mac_address):
        self.kv.delete_assetlist(mac_address)

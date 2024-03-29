import unicodedata
import hashlib
import time
from source.cryptography import KeyGen as keygen
from Crypto.Cipher import AES
import os
import json
import binascii
import unicodedata
from base64 import b64encode, b64decode
import random
from source.graph import Graph, tx
from source.node import Node as node
from source.util import Util as util
from flask import jsonify

# Instantiate necessary objects
cryptography = keygen()
graph = Graph()
node = node()
util = util()

class Wallet:

    def access_wallet(self):
        self.wallet = cryptography.generate_and_verify_seedphrase(cryptography)
        if self.wallet == True: # If a new wallet is created
            self.alphanumeric_address = cryptography.get_address_pair(cryptography)[0]
            self.readable_address = cryptography.get_address_pair(cryptography)[1]
            self.addresses = self.alphanumeric_address, self.readable_address
            if graph.count_tx_number() == 0 or 1 or 2 or 3:
                return True
            else:
                return False
        elif self.wallet == False: # If a wallet exists already and is being loaded
            self.alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)
            self.readable_address = cryptography.get_ex_readable_address(cryptography)
            self.addresses = self.alphanumeric_address, self.readable_address

            if graph.count_tx_number() == 0 or 1 or 2 or 3:
                return True
            else:
                return False

    def retrieve_addresses(self):
        return self.addresses

    def get_balance(self, address):
        balance = 0
        graph_data = util.get_graph()
        for key in graph_data:
            if graph_data[key]['sender'] and graph_data[key]['recipient'] == address:
                genesis = False
            else:
                genesis = True

        if genesis == True:
            minted_tx = (graph_data[(list(graph_data.keys())[0])])
            balance = int(minted_tx["amount"])

        else:
            for tx in graph_data():
                if address in graph_data[tx]['sender']:
                    balance -= int(graph_data[tx]["amount"])
                if address in graph_data[tx]["recipient"]:
                    balance += int(graph_data[tx]["amount"])

        print(f'Balance of the following wallet address "{address}" is: {"{:,}".format(balance)} LXR')
        return balance




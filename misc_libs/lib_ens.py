#!/usr/bin/env python3
import time
from web3.auto.infura import w3
from ens import ENS
ns = ENS.fromWeb3(w3)

ABI = [{"inputs":[{"internalType":"contract ENS","name":"_ens","type":"address"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":True,"internalType":"uint256","name":"contentType","type":"uint256"}
  ],"name":"ABIChanged","type":"event"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":False,"internalType":"address","name":"a","type":"address"}
  ],"name":"AddrChanged","type":"event"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":False,"internalType":"uint256","name":"coinType","type":"uint256"},
    {"indexed":False,"internalType":"bytes","name":"newAddress","type":"bytes"}
  ],"name":"AddressChanged","type":"event"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":True,"internalType":"address","name":"owner","type":"address"},
    {"indexed":True,"internalType":"address","name":"target","type":"address"},
    {"indexed":False,"internalType":"bool","name":"isAuthorised","type":"bool"}
  ],"name":"AuthorisationChanged","type":"event"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":False,"internalType":"bytes","name":"hash","type":"bytes"}
  ],"name":"ContenthashChanged","type":"event"},
  {"anonymous":False,"inputs":[
    {"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},
    {"indexed":False,"internalType":"bytes","name":"name","type":"bytes"},
    {"indexed":False,"internalType":"uint16","name":"resource","type":"uint16"},
    {"indexed":False,"internalType":"bytes","name":"record","type":"bytes"}
  ],"name":"DNSRecordChanged","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},{"indexed":False,"internalType":"bytes","name":"name","type":"bytes"},{"indexed":False,"internalType":"uint16","name":"resource","type":"uint16"}],"name":"DNSRecordDeleted","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"}],"name":"DNSZoneCleared","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},{"indexed":True,"internalType":"bytes4","name":"interfaceID","type":"bytes4"},{"indexed":False,"internalType":"address","name":"implementer","type":"address"}],"name":"InterfaceChanged","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},{"indexed":False,"internalType":"string","name":"name","type":"string"}],"name":"NameChanged","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},{"indexed":False,"internalType":"bytes32","name":"x","type":"bytes32"},{"indexed":False,"internalType":"bytes32","name":"y","type":"bytes32"}],"name":"PubkeyChanged","type":"event"},
  {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"node","type":"bytes32"},{"indexed":True,"internalType":"string","name":"indexedKey","type":"string"},{"indexed":False,"internalType":"string","name":"key","type":"string"}],"name":"TextChanged","type":"event"},

  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"uint256","name":"contentTypes","type":"uint256"}],
  "name":"ABI","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"}],
  "name":"addr","outputs":[{"internalType":"address payable","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"uint256","name":"coinType","type":"uint256"}],
  "name":"addr","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],
  "name":"authorisations","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"}],
  "name":"clearDNSZone","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"}],
  "name":"contenthash","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes32","name":"name","type":"bytes32"},{"internalType":"uint16","name":"resource","type":"uint16"}],
  "name":"dnsRecord","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes32","name":"name","type":"bytes32"}],
  "name":"hasDNSRecords","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes4","name":"interfaceID","type":"bytes4"}],
  "name":"interfaceImplementer","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],
  "name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"}],
  "name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"}],
  "name":"pubkey","outputs":[{"internalType":"bytes32","name":"x","type":"bytes32"},{"internalType":"bytes32","name":"y","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"uint256","name":"contentType","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],
  "name":"setABI","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"uint256","name":"coinType","type":"uint256"},{"internalType":"bytes","name":"a","type":"bytes"}],
  "name":"setAddr","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"address","name":"a","type":"address"}],
  "name":"setAddr","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bool","name":"isAuthorised","type":"bool"}],
  "name":"setAuthorisation","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes","name":"hash","type":"bytes"}],
  "name":"setContenthash","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes","name":"data","type":"bytes"}],
  "name":"setDNSRecords","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes4","name":"interfaceID","type":"bytes4"},{"internalType":"address","name":"implementer","type":"address"}],
  "name":"setInterface","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"string","name":"name","type":"string"}],
  "name":"setName","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"bytes32","name":"x","type":"bytes32"},{"internalType":"bytes32","name":"y","type":"bytes32"}],
  "name":"setPubkey","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":False,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"string","name":"key","type":"string"},{"internalType":"string","name":"value","type":"string"}],
  "name":"setText","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
  {"constant":True,"inputs":[{"internalType":"bytes4","name":"interfaceID","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"pure","type":"function"},
  {
    "constant":True,
    "inputs":[
      {
        "internalType":"bytes32",
        "name":"node",
        "type":"bytes32"
      },
      {
        "internalType":"string",
        "name":"key",
        "type":"string"
      }
    ],
    "name":"text",
    "outputs":[
      {
        "internalType":"string",
        "name":"",
        "type":"string"
      }
    ],
    "payable":False,
    "stateMutability":"view",
    "type":"function"
  }
]


def get_ens_eth_address(name):
  return ns.address(name)


def get_ens_eth_owner(name):
  return ns.owner(name)


def get_ens_eth_owner(address):
  return ns.name(address)


def get_ens_eth_namehash(address):
  return ns.namehash(address)


def load_ens_contract():
    contract_address = w3.toChecksumAddress('0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41')
    return w3.eth.contract(address=contract_address, abi=ABI)


def get_ens_record(node, key):
    ens_contract = load_ens_contract()
    return ens_contract.caller.text(node=node, key=key)


if __name__ == '__main__':


    #ABI = {"constant":True,"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"string","name":"key","type":"string"}],"name":"text","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"}
    #print(ns.get_text('dragonhound.eth', 'avatar'))
    print(get_ens_record(ns.namehash('dragonhound.eth'), "com.github"))
    print(get_ens_record(ns.namehash('dragonhound.eth'), "avatar"))
    print(ns.owner('dragonhound.eth'))                # ENS Owner eth address
    #print(ns.address('dragonhound.eth'))              # ENS Owner eth address
    print(ns.resolver('dragonhound.eth').address)     # Address of contract for ENS 
    #print(dir(ns.resolver('dragonhound.eth')))
    print("****************************")
    #print(ns.reverser(ns.address('dragonhound.eth')))
    print(ns.reverser(ns.address('dragonhound.eth')).address) # DefaultReverseResolver address
    print("****************************")
    print(ns.get_text('dragonhound.eth', "com.github"))
    print(ns.get_text('dragonhound.eth', "avatar"))
    

    def get_text(self, name: str, key: str):
        """
        """
        print(name)
        node = normal_name_to_hash(name)
        print(node)
        print(dir(self.ens.functions))
        print(self.ens.caller().text(node, key))
        return self.ens.caller.text(node, key)


    def text(self, name: str, key: str):
        """
        """
        print("=-------------------------=")
        print(name)
        #self._ens = self.web3.eth.contract(abi=abis.ENS, address=self.web3.toChecksumAddress("0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41"))
        print("=-------------------------=")
        return self.resolve(name, get='text')

    def get_text(self, name: str, key: str):
        node = raw_name_to_hash(name)
        print(node)
        return self.text(node=node, key=key)
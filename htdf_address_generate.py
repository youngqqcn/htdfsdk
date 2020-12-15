#!coding:utf8
#author:yqq
#date:2019/5/5 0005 19:33
#date: 2020-09-27  refactored by yqq in python3
#description:  HTDF address generate demo
#
# run this demo:
#  step 1 :  pip3 install ecdsa  bech32
#  step 2 :  python3 htdf_address_generate.py
# 
# algorithm :
#  step 1 : generate random in range 1 and MAX_P , 
#  step 2 : use secp256k1 library generate keypair : private_key and public_key
#  step 3 : address = bech32(ripemd160( sha256( public_key ) ) )
#  step 4 : OK!

import hashlib
import ecdsa
import os
from bech32 import bech32_encode, convertbits
from binascii import hexlify, unhexlify

def privkey_to_compress_pubkey(privkey):
    sk = ecdsa.SigningKey.from_string( unhexlify( privkey), curve=ecdsa.SECP256k1)
    s = sk.get_verifying_key().to_string(encoding='compressed')
    return  hexlify(s).decode('latin1')

def generate_private_key():
    # reference : https://en.bitcoin.it/wiki/Private_key
    MAX_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140
    while True:
        privkey = hexlify(os.urandom(32))    
        if  (1<<32) < int(privkey, 16) <  MAX_P:
            return privkey.decode('latin1')

def pubkey_to_address( pubKey,  hrp='htdf'):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256( unhexlify(pubKey)).digest())
    r160data = ripemd160.digest()
    data = [ r160data[i]  for i in range(len(r160data)) ]
    address = bech32_encode(hrp, convertbits(data, 8, 5))   
    return address

def gen_addr_from_privkey(priv_key : str) -> str:
    pubKey = privkey_to_compress_pubkey(priv_key)
    address = pubkey_to_address(pubKey, hrp='htdf')
    return address

def generate_htdf_address(hrp = 'htdf'):
    privkey = generate_private_key()
    pubkey = privkey_to_compress_pubkey(privkey) 
    # print("private key: {}".format(privkey))
    # print("public key : {}".format(privkey_to_compress_pubkey(privkey) ))
    # print("address : {}".format( pubkey_to_address( pubkey, hrp) ) )
    # print("address : {}".format( gen_addr_from_privkey(privkey) ))
    print('"{}","{}"'.format( privkey, gen_addr_from_privkey(privkey) ))

def main():
    for i in range(10):
        generate_htdf_address(hrp='htdf')
    pass

if __name__ == '__main__':

    main()



#coding:utf8
#author: yqq
#date: 2020/12/15 下午7:16
#descriptions:

UNSIGNED_TX_TEMPLATE = """{\
           "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
           "memo": "%s",\
       	"msgs": [{\
       		"Amount": [{\
       			"amount": "%d",\
                   "denom": "satoshi"\
       		}],\
               "Data": "%s",\
               "From": "%s",\
               "GasPrice": %s,\
               "GasWanted": %s,\
       		"To": "%s"\
       	}],\
           "sequence": "%d"\
           }"""

BROADCAST_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdfservice/send",  
                   "value":{
                       "From": "%s",
                       "To": "%s",
                       "Amount": [{
                           "denom": "satoshi",
                           "amount": "%d"
                       }],
                       "Data": "%s",
                       "GasPrice": "%d",
                       "GasWanted": "%d"
                   }
               }],
               "fee": {
                   "gas_wanted": "%d",
                   "gas_price": "%d"
               },
               "signatures": [{
                   "pub_key": {
                       "type": "tendermint/PubKeySecp256k1",
                       "value": "%s"
                   },
                   "signature": "%s"
               }],
               "memo": "%s"
           }
       }"""
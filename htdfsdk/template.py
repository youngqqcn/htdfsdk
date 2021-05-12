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




UNSIGNED_DELEGATE_TX_TEMPLATE = """{\
        "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
        "memo": "%s",\
       	"msgs": [{\
       	    "type":"htdf/MsgDelegate",\
       	    "value":{\
       	        "amount": {\
       			    "amount": "%d",\
                    "denom": "satoshi"\
       		    },\
                "delegator_address": "%s",\
       		    "validator_address": "%s"\
       		}\
       	}],\
        "sequence": "%d"\
        }"""



BROADCAST_DELEGATE_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdf/MsgDelegate",  
                   "value":{
                       "delegator_address": "%s",
                       "validator_address": "%s",
                       "amount": {
                           "denom": "satoshi",
                           "amount": "%d"
                       }
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





UNSIGNED_WITHDRAW_DELEGATE_REWARDS_TX_TEMPLATE = """{\
        "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
        "memo": "%s",\
       	"msgs": [{\
       	    "type":"htdf/MsgWithdrawDelegationReward",\
       	    "value":{\
                "delegator_address": "%s",\
       		    "validator_address": "%s"\
       		}\
       	}],\
        "sequence": "%d"\
        }"""



BROADCAST_WITHDRAW_DELEGATE_REWARDS_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdf/MsgWithdrawDelegationReward",  
                   "value":{
                       "delegator_address": "%s",
                       "validator_address": "%s"
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



UNSIGNED_UNDELEGATE_TX_TEMPLATE = """{\
        "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
        "memo": "%s",\
       	"msgs": [{\
       	    "type":"htdf/MsgUndelegate",\
       	    "value":{\
       	        "amount": {\
       			    "amount": "%d",\
                    "denom": "satoshi"\
       		    },\
                "delegator_address": "%s",\
       		    "validator_address": "%s"\
       		}\
       	}],\
        "sequence": "%d"\
        }"""



BROADCAST_UNDELEGATE_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdf/MsgUndelegate",  
                   "value":{
                       "delegator_address": "%s",
                       "validator_address": "%s",
                       "amount": {
                           "denom": "satoshi",
                           "amount": "%d"
                       }
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





UNSIGNED_SET_UNDELEGATE_STATUS_TX_TEMPLATE = """{\
        "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
        "memo": "%s",\
       	"msgs": [{\
       	    "type":"htdf/MsgSetUndelegateStatus",\
       	    "value":{\
       	        "Status":%s,\
                "delegator_address": "%s",\
       		    "validator_address": "%s"\
       		}\
       	}],\
        "sequence": "%d"\
        }"""



BROADCAST_SET_UNDELEGATE_STATUS_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdf/MsgSetUndelegateStatus",  
                   "value":{
                        "Status":%s,
                       "delegator_address": "%s",
                       "validator_address": "%s"
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



UNSIGNED_EDIT_VALIDATOR_INFO_TX_TEMPLATE = """{\
        "account_number": "%d",\
       	"chain_id": "%s",\
       	"fee": {\
       			"gas_price": "%d",\
       			"gas_wanted": "%d"\
       	},\
        "memo": "%s",\
       	"msgs": [{\
       	    "type":"htdf/MsgEditValidator",\
       	    "value":{\
       	        "Description":{\
       	            "details":"%s",\
       	            "identity":"%s",\
       	            "moniker":"%s",\
       	            "website":"%s"\
       	        },\
       	        "address":"%s",\
       	        "commission_rate":"%s",\
       	        "min_self_delegation":"%s"\
       		}\
       	}],\
        "sequence": "%d"\
        }"""



BROADCAST_EDIT_VALIDATOR_INFO_TX_TEMPLATE  = """{
           "type": "auth/StdTx",
           "value":{
               "msg": [{
                   "type": "htdf/MsgEditValidator",  
                   "value":{
                        "Description":{
       	                    "details":"%s",
       	                    "identity":"%s",
       	                    "moniker":"%s",
       	                    "website":"%s"
       	                },
       	                "address":"%s",
       	                "commission_rate":"%s",
       	                "min_self_delegation":"%s"
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
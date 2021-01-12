#coding:utf8
#author: yqq
#date: 2020/12/15 下午5:38
#descriptions:

from decimal import Decimal, getcontext

# getcontext()

def htdf_to_satoshi(amount_htdf: [float, int, str]) -> int:
    return int(Decimal(str(amount_htdf)) * (10 ** 8))




if __name__ == '__main__':
    assert htdf_to_satoshi(139623.71827296) == 13962371827296
    assert htdf_to_satoshi('139623.71827296') == 13962371827296
    assert htdf_to_satoshi(13962371827296) == 13962371827296 * 10 ** 8
    pass


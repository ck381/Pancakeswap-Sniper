from web3 import Web3
import os
import json
import time
from functools import wraps
import time
import sys

import os

# System call
os.system("")

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class Token:
    ETH_ADDRESS = Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
    MAX_AMOUNT = int('0x' + 'f' * 64, 16)

    def __init__(self, address, provider=None):
        self.address = Web3.toChecksumAddress(address)
        self.provider = os.environ['PROVIDER'] if not provider else provider
        self.web3 = Web3(Web3.HTTPProvider(self.provider))
        from web3.middleware import geth_poa_middleware
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.wallet_address = None
        self.router = self.web3.eth.contract(
            address=Web3.toChecksumAddress('0x10ED43C718714eb63d5aA57B78B54704E256024E'),
            abi=json.load(open(
                os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/abi_files/" + "router.abi"))))
        self.erc20_abi = json.load(
            open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/abi_files/" + "erc20.abi")))
        self.gas_limit = 0
        self.gas_price = 0
        self.amount_purchased = 0
        self.nonce = None

        with open("configuration.json") as json_data_file:
            data = json.load(json_data_file)
            self.data = data.get('Data')



    def set_gas_values(self,gas_price,gas_limit):

        self.gas_limit = int(gas_limit)
        self.gas_price = int(gas_price)
        self.nonce = self.web3.eth.getTransactionCount(self.wallet_address)

    def setParameters(self):
        self.nonce = self.web3.eth.getTransactionCount(self.wallet_address)
        self.gas_price = int(self.web3.eth.gasPrice * 5)
        self.gas_limit = 500000



 
    def connect_wallet(self, wallet_address='', private_key=''):
        try:
            self.wallet_address = Web3.toChecksumAddress(wallet_address)
        except:
            print(style.RED + 'Your wallet address has the wrong format' + style.WHITE)
            sys.exit()
        try:
            self.private_key = private_key
        except:
            print(style.RED + 'Your private key has the wrong format' + style.WHITE)
            sys.exit()



    def is_connected(self):
        c_address = Web3.toChecksumAddress("0x4e6415a5727ea08aae4580057187923aec331227")
        token_contract = self.web3.eth.contract(c_address, abi=self.erc20_abi)
        return False if not self.wallet_address else True

    def require_connected(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.is_connected():
                raise RuntimeError('Please connect the wallet first!')
            return func(self, *args, **kwargs)

        return wrapper

    def create_transaction_params(self, value=0, gas_price=None, gas_limit=None):
        #x = self.web3.eth.getTransactionCount(self.wallet_address)
        if not self.is_connected():
            raise RuntimeError('Please connect the wallet first!')
        if not gas_price:
            gas_price = self.web3.eth.gasPrice
        if not gas_limit:
            gas_limit = self.gas_limit

        return {
            "chainId": 56,
            "from": self.wallet_address,
            "value": value,
            'gasPrice': self.gas_price,
            "gas": gas_limit,
            "nonce": self.nonce
        }

    def create_sell_transaction_params(self, value=0, gas_price=None, gas_limit=None):
        self.setParameters()
        if not self.is_connected():
            raise RuntimeError('Please connect the wallet first!')
        if not gas_price:
            gas_price = self.web3.eth.gasPrice
        if not gas_limit:
            gas_limit = self.gas_limit

        return {
            "chainId": 56,
            "from": self.wallet_address,
            "value": value,
            'gasPrice': self.gas_price,
            "gas": 300000,
            "nonce": self.nonce
        }



    def send_transaction(self, func, params):
        tx = func.buildTransaction(params)
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        return self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    @require_connected
    def is_approved(self, token_address=None, amount=MAX_AMOUNT):
        token_address = Web3.toChecksumAddress(token_address) if token_address else self.address
        erc20_contract = self.web3.eth.contract(address=token_address, abi=self.erc20_abi)
        approved_amount = erc20_contract.functions.allowance(self.wallet_address, self.router.address).call()
        return approved_amount >= amount


    # ------------------------------------------------------------------------------------------------------- #
 

    # ------------------------------------------------------------------------------------------------------- #



        
        

    @require_connected
    def approve(self, token_address, amount=MAX_AMOUNT, gas_price=None, timeout=900):
        if not gas_price:
            gas_price = self.web3.eth.gasPrice
        token_address = Web3.toChecksumAddress(token_address)
        erc20_contract = self.web3.eth.contract(address=token_address, abi=self.erc20_abi)
        func = erc20_contract.functions.approve(self.router.address, amount)
        params = self.create_transaction_params(gas_price=gas_price)
        tx = self.send_transaction(func, params)
        receipt = self.web3.eth.waitForTransactionReceipt(tx, timeout=timeout)
        return receipt

    def get_weth_address(self):
        # Contract calls should always return checksummed addresses
        address = Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
        return address

    def price(self, amount, swap_token_address=ETH_ADDRESS):

        swap_token_address = Web3.toChecksumAddress(swap_token_address)
        return self.router.functions.getAmountsOut(amount, [self.address, swap_token_address]).call()[-1]


    def received_amount_by_swap(self, input_token_amount, input_token_address):
        input_token_address = Web3.toChecksumAddress(input_token_address)
        route = [input_token_address, self.address]
        return self.router.functions.getAmountsOut(input_token_amount, route).call()[-1]

    def balance(self, address):
        address = self.wallet_address if not address else Web3.toChecksumAddress(address)
        if not address:
            raise RuntimeError('Please provide the wallet address!')
        erc20_contract = self.web3.eth.contract(address=self.address, abi=self.erc20_abi)
        return erc20_contract.functions.balanceOf(self.wallet_address).call()

    @require_connected
    def buy(self, consumed_token_amount, consumed_token_address=ETH_ADDRESS, slippage=20.00, timeout=900, speed=1):
        consumed_token_address = Web3.toChecksumAddress(consumed_token_address)
        #received_amount = self.received_amount_by_swap(consumed_token_amount, consumed_token_address)
        #print(received_amount)
        #self.amount_purchased = received_amount
        #min_out = int(received_amount * (1 - slippage))
        #print('---------')

        min_out = 0
        slippage = 20.0

        a = min_out
        b = [consumed_token_address,self.address]
        c = self.wallet_address
        d = int(time.time() + timeout)


        #print(self.is_approved(consumed_token_address, consumed_token_amount))
        if consumed_token_address == self.ETH_ADDRESS:

            func = self.router.functions.swapExactETHForTokens(min_out, [consumed_token_address,self.address],self.wallet_address, int(time.time() + timeout))

            params = self.create_transaction_params(value=consumed_token_amount, gas_price=self.gas_price)



        else:

            if not self.is_approved(consumed_token_address, consumed_token_amount):
                self.approve(consumed_token_address, gas_price=self.gas_price, timeout=timeout)
            func = self.router.functions.swapExactTokensForTokens(consumed_token_amount, min_out,
                                                                  [self.get_weth_address(), consumed_token_address, self.address],
                                                                  self.wallet_address, int(time.time() + timeout))
            params = self.create_transaction_params(gas_price=self.gas_price)

        a = time.perf_counter()
        b = time.perf_counter()

        return self.send_transaction(func, params)

    @require_connected
    def sell(self, amount, received_token_address=ETH_ADDRESS, slippage=20.00, timeout=900, speed=1):
        gas_price = int(self.web3.eth.gasPrice * speed)
        received_token_address = Web3.toChecksumAddress(received_token_address)
        received_amount = self.price(amount, received_token_address)
        min_out = 0
        if not self.is_approved(self.address, amount):
            self.approve(self.address, gas_price=gas_price, timeout=timeout)
        if received_token_address == self.ETH_ADDRESS:
            func = self.router.functions.swapExactTokensForETH(amount, min_out, [self.address, received_token_address],
                                                               self.wallet_address, int(time.time() + timeout))
        else:
            func = self.router.functions.swapExactTokensForTokens(amount, min_out,
                                                                  [self.address, received_token_address],
                                                                  self.wallet_address, int(time.time() + timeout))
        params = self.create_sell_transaction_params(gas_price=gas_price)
        return self.send_transaction(func, params)



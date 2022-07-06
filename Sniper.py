from Token import *
from blocknativesdk.blocknative.stream import Stream
import json
from web3 import Web3
import os.path
import time
import sys
from telethon import TelegramClient, events, sync
import re


import os
import requests
import keyboard
import webbrowser
from art import *
import time
from threading import Thread

#Start Trading
#Lock Liquidity
#Finalize # 0x4bb278f3
#openTrading
#Set Enable Swap And Liquify 0x57e814e30000000000000000000000000000000000000000000000000000000000000001


# Find original owner
# Check for transfer of ownership
# Listen to owners address for certain method

# System call
os.system("")

#0x0df8022e


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

# Configuration #
# --------------------------------------------------- #

import json
data = None
try:
    with open("configuration.json") as json_data_file:
        data = json.load(json_data_file)
        data = data.get('Data')

except Exception as e:
    print('No configuration file found - initialising setup...')

# --------------------------------------------------- #

def displayConfig():

    import json
    with open("configuration.json") as json_data_file:
        data = json.load(json_data_file)
        data = data.get('Data')
    print("======================================================================")
    print('Wallet address: ', data['wallet_address'])
    print('Private Key: ', data['private_key'])
    print('Blocknative API Key: ', data['blocknative'])
    print('HTTP Provider: ', data['provider'])

# --------------------------------------------------- #


def setupConfig():

    if not os.path.exists('configuration.json'):
        wallet = input('Enter your wallet address: ')
        private_key = input('Enter your private key: ')
        blocknative = input('Enter your Blocknative API Key: ')
        data = {'Data': {'blocknative':blocknative,'wallet_address':wallet,'private_key':private_key,'provider':'https://bsc-dataseed.binance.org/'}}
        import json
        with open('configuration.json', 'w') as f:
            json.dump(data, f)
        print('Configuration saved!')

    else:
        print(style.YELLOW + 'Loading configuration...' + style.WHITE)
        displayConfig()

# --------------------------------------------------- #


class Sniper:

    def __init__(self,data,mode):

        self.blocknative = None
        self.transaction = None
        self.data = None
        self.mode = mode.lower()
        self.purchase_amount = None
        self.token_object = None
        self.token = None
        self.purchased = False
        self.timestamp = None
        self.pinksale = False
        self.dxsale = False
        self.presale_address = None
        self.decimals = None
        self.provider = data['provider']  # Blocknative API key
        self.delay = 0

        self.type = input('Enter BNB / BUSD / USDT: ').upper()

        if mode.lower() == 'default':
            self.defaultSnipe()
        if mode.lower() == 'telegram':
            self.telegramSnipe()

        self.api_key = data['blocknative']  # Blocknative API key
        self.router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
        self.wallet_address = data['wallet_address']
        self.private_key = data['private_key'] # Your private key


    def defaultSnipe(self):

        self.token = input('Enter token address: ')
        self.purchase_amount = float(input('Enter purchase amount (BNB): '))

        try:
            self.token_object = Token(self.token, self.provider)
        except Exception as e:
            print(style.RED + 'Token format is incorrect' + style.WHITE)
            print(e)
            sys.exit()

        self.checkPresale()


    def checkPresale(self):

        print("======================================================================")

        print(style.YELLOW + 'Presale options' + style.WHITE)

        was_presale = input('(1) There was a presale\n'
                            '(2) There was no presale\n')

        print("======================================================================")

        if was_presale == '1':
            site = input('(1) Pinksale\n'
                         '(2) DXSale\n')

            print("======================================================================")

            if site == '1':
                presale = input('Pinksale presale address: ')
                self.pinksale = True
                self.presale_address = presale
            if site == '2':
                self.dxsale = True



    def telegramSnipe(self):
        self.purchase_amount = float(input('Enter purchase amount (BNB): '))
        self.telegram_names = input('Enter names of people to ignore (welcome bots) with a space between each username: ')
        self.telegram_names = self.telegram_names.split()
        print('Blocked usernames: ' + str(self.telegram_names))


    def checkBuyConfirmed(self,hash):


        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        receipt = web3.eth.wait_for_transaction_receipt(hash)
        status = receipt['status']

        if int(status) == 1:
            print(style.YELLOW + 'Token purchased' + style.WHITE)
            confirmed = True
        if int(status) == 0:
            print(style.RED + 'Token purchase failed' + style.WHITE)
            sys.exit()




    def buyBUSD(self):

        busd = Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')
        hash = self.token_object.buy(int(self.purchase_amount * 1000000000000000000), consumed_token_address=busd)
        print(style.GREEN + 'Buy transaction submitted')
        print(style.YELLOW + 'Transaction hash : https://bscscan.com/tx/' + str(hash.hex()) + style.WHITE)
        self.checkBuyConfirmed(hash)

        return hash.hex()

    def buyBNB(self):

        hash = self.token_object.buy(int(self.purchase_amount * 1000000000000000000))
        print(style.GREEN + 'Buy transaction submitted')
        print(style.YELLOW + 'Transaction hash : https://bscscan.com/tx/' + str(hash.hex()) + style.WHITE)
        self.checkBuyConfirmed(hash)


        return hash.hex()



    def connect_wallet(self):

        self.token_object.connect_wallet(self.wallet_address, self.private_key)

    def create_transaction(self):

        gas_price = self.data.get('gasPrice')
        gas_limit = self.data.get('gas')
        self.token_object.set_gas_values(gas_price,gas_limit)


    def getFilters(self):

        if self.mode == 'default':

            print(style.YELLOW + 'Scanning for liquidity add to token: ' + self.token + ' | Purchase Amount = ' + str(
                self.purchase_amount) + ' BNB' + style.WHITE)

            global_filters = [{
                'status': 'pending',

                "_join": "OR",
                "terms": [
                    {
                        'contractCall.methodName': "addLiquidity"
                    },
                    {
                        "contractCall.methodName": "addLiquidityETH"
                    }
                ],

                "_join": "OR",
                "terms": [
                    {
                        "contractCall.params.token": self.token
                    },
                    {
                        "contractCall.params.tokenA": self.token
                    },
                    {
                        "contractCall.params.tokenB": self.token
                    }]
            }]

        return global_filters

    def approve(self):

        # Approve the token for selling
        receipt = self.token_object.approve(self.token,115792089237316195423570985008687907853269984665640564039457584007913129639935)

        # Validate whether the approval was successful
        approval_confirmed = self.checkConfirmedApproval(receipt)


    def liquidityConfirmed(self,receipt):

        confirmed = False
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        status = receipt['status']

        if int(status) == 1:
            print(style.YELLOW + 'Liquidity confirmed' + style.WHITE)
            confirmed = True
        if int(status) == 0:
            print(style.RED + 'Liquidity failed' + style.WHITE)

    def transactionConfirmedApproval(self,receipt):

        confirmed = False
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        status = receipt['status']

        if int(status) == 1:
            print(style.YELLOW + 'Token Approved' + style.WHITE)
            confirmed = True
        if int(status) == 0:
            print(style.RED + 'Token approval failed' + style.WHITE)

        return confirmed

    def checkConfirmedSell(self,receipt):

        confirmed = False
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        status = receipt['status']

        if int(status) == 1:
            print(style.GREEN + 'Token sold successfully' + style.WHITE)
            sys.exit()
            confirmed = True
        if int(status) == 0:
            print(style.RED + 'Token sell failed' + style.WHITE)

        return confirmed

    def telegramBuy(self):

        if self.type == 'BNB':
            hash = self.buyBNB()
        if self.type == 'BUSD':
            hash = self.buyBUSD()
        if self.type == 'USDT':
            hash = self.buyBNB()
        print(style.GREEN + 'Token purchased' + style.WHITE)
        print(style.YELLOW + 'Transaction hash : https://bscscan.com/tx/' + hash.hex() + style.WHITE)


    def getBalance(self):

        provider = 'https://bsc-dataseed.binance.org/'
        web3 = Web3(Web3.HTTPProvider(provider))

        directory = './abi/'
        filename = "standard.json"
        file_path = os.path.join(directory, filename)
        with open(file_path) as json_file:
            standardAbi = json.load(json_file)

        token_abi = standardAbi
        token = Web3.toChecksumAddress(self.token)

        try:

            token_contract = web3.eth.contract(abi=token_abi, address=token)
            decimals = token_contract.functions.decimals().call()
            self.decimals = decimals
            balance = token_contract.functions.balanceOf(self.wallet_address).call()
            balance = float(balance)
            return balance / float(10 ** decimals)


        except Exception as e:
            print(e)
            print(style.RED + 'Error getting token balance' + style.WHITE)




    def snipe(self):

        global_filters = self.getFilters()

        stream = Stream(self.api_key)

        async def txn_handler(txn, unsubscribe):

            # This will only get called with transactions that have status of 'pending'
            # This is due to the global filter above
            if self.data == None:

                self.data = json.dumps(txn, indent=4)
                self.data = json.loads(self.data)


                # Output some transaction details
                tx_hash = str(self.data.get('hash'))
                print(style.GREEN + 'Sniped Transaction: ' + style.YELLOW + 'BscScan link : ' + 'https://bscscan.com/tx/' + tx_hash + style.WHITE)
                #for key, value in txn.items():
                #    print(style.YELLOW + str(key) + ': ' + style.WHITE + str(value))



                # Buy the token
                try:
                    self.create_transaction()
                    if self.type == 'BNB':
                        hash = self.buyBNB()
                    if self.type == 'BUSD':
                        hash = self.buyBUSD()
                    if self.type == 'USDT':
                        hash = self.buyBNB()

                    # Open the pancakeswap trade page in case need to sell manually
                    webbrowser.open('https://pancakeswap.finance/swap?outputCurrency=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&inputCurrency=' + self.token)

                    # Listen for user input as to whether to sell the token

                    balance = float(self.getBalance())
                    print('Balance = ' + str(balance))

                    print('\n')
                    print("======================================================================")
                    print(style.YELLOW + "Press 's' at any time to try and sell all the tokens" + style.WHITE)

                    start_price = self.token_object.price(int(1 * 10 ** self.decimals))

                    while True:

                        current_price = self.token_object.price(int(1 * 10 ** self.decimals))
                        change = abs(current_price - start_price) / start_price * 100.0
                        print('% profit: ' + str(change),end="\r")


                        try:
                            if keyboard.is_pressed('s'):
                                print(style.GREEN + 'Trying to sell token...')
                                web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
                                decimals = 10 ** self.decimals
                                balance = balance * 0.9
                                sell_hash = self.token_object.sell(int(balance * int(decimals)))
                                print(style.YELLOW + 'Transaction hash : https://bscscan.com/tx/' + sell_hash.hex() + style.WHITE)
                                receipt = web3.eth.wait_for_transaction_receipt(sell_hash)
                                confirmed = self.checkConfirmedSell(receipt)
                                break  # finishing the loop
                        except:
                            break  # if user pressed a key other than the given key the loop will break

                # Exception thrown
                except Exception as e:
                    print(style.RED + 'Failed: Insufficient funds' + style.WHITE)
                    print(e)
                    sys.exit()



        # Connect to the mempool explorer and subscribe
        stream.subscribe_address(self.router, txn_handler,filters = global_filters)



        #Pinksale
        if self.pinksale == True:
            presale_filters = [{
                    'status': 'pending',
                    "input": "0x4bb278f3"
                }]

            stream.subscribe_address(self.presale_address, txn_handler, filters=presale_filters)

            #presale_filters = [{
            #    'status': 'pending',
            #    "input": "0x4bb278f3"
            #}]

            #stream.subscribe_address('0x0000000000000000000000000000000000000000', txn_handler, filters=presale_filters)

            #presale_filters = [{
            #    'status': 'pending',
            #    "input": "0xc1d2e449"
            #}]

            #stream.subscribe_address('0x0000000000000000000000000000000000000000', txn_handler, filters=presale_filters)




        if self.dxsale == True:
            presale_filters = [{
                'status': 'pending',
                "input": "0x0df8022e"
            }]

            stream.subscribe_address('0x7100c01f668a5b407db6a77821ddb035561f25b8', txn_handler, filters=presale_filters)





        stream.connect()


        


# --------------------------------------------------- #


def TelegramSniper(data):

    client = TelegramClient('anon', '13906054', 'af7730c3939050ccdf4ab68c2463c19a')
    channel_name = input('Enter Telegram channel name: ')
    sniper = Sniper(data, mode='Telegram')
    try:
        default = '0xe9e7cea3dedca5984780bafc599bd69add087d56' #BUSD
        sniper.token_object = Token(default, sniper.provider)
    except:
        print(style.RED + 'Token format is incorrect' + style.WHITE)

    sniper.connect_wallet()
    sniper.token_object.setParameters()
    counter = 0
    @client.on(events.NewMessage(chats=channel_name))

    async def my_event_handler(event):

        try:

            sender = await event.get_sender()
            username = sender.username

            if username in sniper.telegram_names:

                print('IGNORE')

        except:

            username = ''

        if username in sniper.telegram_names:

            print('IGNORE')

        else:

            global counter
            print(event.raw_text)


            text = event.raw_text

            found_address = ''
            found = False

            text = text.lower()

            try:

                contract_address = re.search('0x[a-fA-F0-9]{40}', text)
                contract_address = contract_address.group(0)

                found_address = str(contract_address)

                if found_address == '0x961baee5168a8b6b5b3746608860ee7f0ca8f2c2':
                    print(style.RED + 'BLACKLIST' + style.WHITE)
                    sys.exit()
                    found = False
                    sys.exit()

                found = True

            except Exception as e:
                print(e)

            if found == True:
                print("======================================================================")

                import time


                sniper.token = found_address
                sniper.token_object.address = Web3.toChecksumAddress(sniper.token)
                print(sniper.token_object.address)
                sniper.telegramBuy()
                b = time.perf_counter()
                sys.exit()



    client.start()
    client.run_until_disconnected()



# --------------------------------------------------- #


def approveToken(data):

    print("======================================================================")

    print(style.YELLOW + "Token approval" + style.WHITE)
    token = input('Enter token address: ')

    provider = 'https://bsc-dataseed.binance.org/'
    token_object = Token(token, provider)
    wallet_address = data['wallet_address']
    private_key = data['private_key']  # Your private key
    token_object.connect_wallet(wallet_address, private_key)
    token_object.setParameters()

    # Approve the token for selling
    receipt = token_object.approve(token,115792089237316195423570985008687907853269984665640564039457584007913129639935)

    # Validate whether the approval was successful

    provider = 'https://bsc-dataseed.binance.org/'
    confirmed = False
    web3 = Web3(Web3.HTTPProvider(provider))
    status = receipt['status']

    if int(status) == 1:
        print(style.GREEN + 'Token approved' + style.WHITE)
        confirmed = True
    if int(status) == 0:
        print(style.RED + 'Token approval failed' + style.WHITE)

    run()

# --------------------------------------------------- #












logo = text2art("Token   Sniper")
print(logo)
setupConfig()


def run():
    print("======================================================================")

    choice = input(style.YELLOW + '(1) Mempool sniper \n'
                                  '(2) Telegram Sniper \n'
                                  '(3) Change the configuration file \n'
                                  '(4) Approve a token \n'
                                  '(5) Timestamp buy\n' + style.WHITE)

    if choice == '1':
        print("======================================================================")
        sniper = Sniper(data,mode = 'Default')
        sniper.connect_wallet()
        sniper.snipe()
    elif choice == '2':
        print("======================================================================")
        logo = text2art("Telegram   Sniper")
        print(logo)
        TelegramSniper(data)
    elif choice == '3':
        print("======================================================================")
        if os.path.exists('configuration.json'):
            os.remove("configuration.json")
            setupConfig()
            run()
    elif choice == '4':
        approveToken(data)
    elif choice == '5':
        sniper = Sniper(data, mode='Default')
        sniper.connect_wallet()
        sniper.timestampSnipe()
    else:
        run()


run()







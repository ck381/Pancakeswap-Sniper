# Pancakeswap Sniper (Binance Smart Chain)

<p align="center">
  <img src="https://www.asiacryptotoday.com/wp-content/uploads/2020/08/Binance-Smart-Chain-scaled.jpeg" width="350" title="Binance Smart Chain">
</p>



This is a cryptocurrency trading tool written in Python to perform low latency buy and sell trades on the binance smart chain. The program interfaces directly with the binance smart chain directly using the Web3 Python API which is a collection of libraries that allows connections to be created with a local or remote node. The application subscribes to the Blocknative API to listen for pending transactions that match the token address supplied. When a matching transaction is found the program executes a buy trade for the specified amount by copying various details from the identified transaction in the pending transaction pool. This ensures that your buy transaction gets broadcasted to a node in such a way that your transaction will be mined and confirmed in the fastest and most efficient way possible. 

## Features
* Mempool scanning for extremely low latency performance (Same block or next block)
* Stoploss
* Pre-defined buy and sell values
* Works for BNB, BUSD and USDT coin pairings
* Suitable for tokens that have undergone presales on sites such as pinksale and dxsale.
* Customisable techniques to bypass the most common bot protection techniques.
* Smart contract function filtering 
* Telegram Sniper (automatically discovers contract address and filters by specified users)







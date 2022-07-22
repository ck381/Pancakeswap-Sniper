# Pancakeswap Sniper (Binance Smart Chain)

<p align="center">
  <img src="https://www.asiacryptotoday.com/wp-content/uploads/2020/08/Binance-Smart-Chain-scaled.jpeg" width="350" title="Binance Smart Chain">
</p>



This is a cryptocurrency trading tool written in Python to perform low latency buy and sell trades on the binance smart chain. The program interfaces directly with the binance smart chain directly using the Web3 Python API. This is a collection of libraries that allows connections to be created with a local or remote node. The application subscribes to the Blocknative API to listen for pending transactions that match the token address supplied. When a matching transaction is found the program executes a buy trade for the specified amount by copying various details from the identified transaction in the pending transaction pool. This ensures that your buy transaction gets broadcasted to a node in such a way that your transaction will be mined and confirmed in the fastest and most efficient way possible. A stoploss and pre-defined sell values can be used to minimise the risk associated with using a tool like this. The program works for BNB, BUSD and USDT coin pairings as well as tokens that have undergone presales on sites such as pinksale and dxsale. It is fully customisable and includes functionality to bypass the most common bot protection techniques employed by new coins. In instances where tokens are launched without using the addLiquidity or addLiquidityEth contract functions the program offers the ability to filter the solidity smart contracts to isolate possible function names that may be used before launch. A Telegram version of the tool is also included that allows for the scanning of Telegram groups for the released token address at launch time. This can be filtered to only listen to messages sent by certain members of the groups. Token addresses are automatically captured using regex pattern matching. 






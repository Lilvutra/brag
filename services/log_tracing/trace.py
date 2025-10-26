import requests
from web3 import Web3 

#BLOCKSCOUT = "https://eth-sepolia.blockscout.com/api?"
#FACTORY = "0x76cc67FF2CC77821A70ED14321111Ce381C2594D"
#BLOCKSCOUT = "https://optimism.blockscout.com/api"     # Optimism
BLOCKSCOUT = "https://eth.blockscout.com/api"   
#FACTORY = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" #vitalik address
#FACTORY = "0x73bFE136fEba2c73F441605752b2B8CAAB6843Ec" # erc contract 
FACTORY = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9" # Aave pool 

"""Transaction Logs (Event Logs per Transaction)

Scope: Tied to a specific transaction (Tx hash).
What events were emitted during that transaction’s execution.
Inspect what happened during a given function call (Deposit, Borrow, Swap, etc.).

You check 0x123...txhash → see Borrow(address user, uint256 amount) event emitted by Aave.

Data source:

eth_getTransactionReceipt

Returns logs only for that one transaction."""

def get_logs(contract_address, from_block, to_block="latest"):
    params = {
        "module": "logs",
        "action": "getLogs",
        "fromBlock": from_block,
        "toBlock": to_block,
        "address": contract_address,
    }
    res = requests.get(BLOCKSCOUT, params=params)
    data = res.json().get("result", [])
    return data

def get_stats(contract_address):
    params = {
        "module": "stats",
        "action": "tokensupply",
        "contractaddress": contract_address,
    }
    try:
        r = requests.get(BLOCKSCOUT, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "1":
            return int(data["result"])
        else:
            print(f"Error: {data.get('message')}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def get_abi(contract_address):
    params = {
        "module": "contract",
        "action": "getabi",
        "address": contract_address
    }
    res = requests.get(BLOCKSCOUT, params=params)
    abi_json = res.json().get("result")
    return abi_json

def fetch_abi_from_logs(logs_response):
    abis = {}
    for log in logs_response:
        addr = log["address"]
        if addr not in abis: #avoid duplicate api call
            abi = get_abi(addr)
            if abi:
                abis[addr] = abi
    return abis 

def extract_new_contracts(logs):
    new_contracts = []
    for log in logs:
        for topic in log["topics"]:
            if topic.startswith("0x000000000000000000000000"):
                addr = "0x" + topic[-40:]
                new_contracts.append(addr)
    return list(set(new_contracts))

def aggregate_protocol_logs(contract_addresses, from_block):
    all_logs = []
    for addr in contract_addresses:
        logs = get_logs(addr, from_block)
        all_logs.extend(logs)
    return all_logs

#print("Detected new contracts:", contracts)
#print("get logs:", get_logs(FACTORY, 21000000))

#logs_result = get_logs(FACTORY, 21000000)

#print(get_stats(FACTORY))
#print(fetch_abi_from_logs(logs_result))

import requests

BLOCKSCOUT = "https://blockscout.com/eth/mainnet/api"
FACTORY = "hmmm"



"""Transaction Logs (a.k.a. Event Logs per Transaction)

Scope: Tied to a specific transaction (Tx hash).
What events were emitted during that transaction’s execution.
Inspect what happened during a given function call (Deposit, Borrow, Swap, etc.).

You check 0x123...txhash → see Borrow(address user, uint256 amount) event emitted by Aave.

Data source:

eth_getTransactionReceipt

Returns logs only for that one transaction."""

def get_logs(from_block):
    params = {
        "module": "logs",
        "action": "getLogs",
        "address": FACTORY,
        "fromBlock": from_block,
        "toBlock": "latest"
    }
    res = requests.get(BLOCKSCOUT, params=params).json()
    return res.get("result", [])

def extract_new_contracts(logs):
    new_contracts = []
    for log in logs:
        for topic in log["topics"]:
            if topic.startswith("0x000000000000000000000000"):
                addr = "0x" + topic[-40:]
                new_contracts.append(addr)
    return list(set(new_contracts))

logs = get_logs(from_block=19000000)
contracts = extract_new_contracts(logs)

def aggregate_protocol_logs(contract_addresses, from_block):
    all_logs = []
    for addr in contract_addresses:
        logs = get_logs(addr, from_block)
        all_logs.extend(logs)
    return all_logs
print("Detected new contracts:", contracts)

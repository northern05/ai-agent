import json
from web3 import Web3


class SMCDriver:

    def __init__(self,
                 web_provider: str,
                 contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(web_provider))
        self.prize_contract_address = contract_address
        with open('contract.abi', 'r') as file:
            self.prize_contract_abi = json.load(file)

        # Connect to the contract
        self.prize_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.prize_contract_address),
            abi=self.prize_contract_abi)

    def get_msg_hash(self, transaction_hash):
        try:
            transaction = self.w3.eth.get_transaction(transaction_hash)
            input_data = transaction.get("input")
            if input_data == '0x':
                print("No input data provided in this transaction.")
            else:
                print(f"Raw input data: {input_data}")
                # Decode the input data if it follows a specific ABI
                hashedPrompt = self.prize_contract.decode_function_input(input_data)[1].get("hashedPrompt")
                msg_hash = hashedPrompt.hex()
                print(f"Decoded input data: {msg_hash}")
                return msg_hash
        except Exception as e:
            print(f"Error fetching transaction: {e}")


if __name__ == '__main__':
    driver = SMCDriver(web_provider="https://1rpc.io/sepolia",
                       contract_address="0xE2ed2a7BeE11e2C936b7999913E3866D4cfc4f8E")
    tr_hash = "0xebcca293f19d597c492e25049665a66a9d8b9f163128c83948c86efbad9d3040"
    print(driver.get_msg_hash(transaction_hash=tr_hash))

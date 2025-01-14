import json
import os

from web3 import Web3


class SMCDriver:

    def __init__(self,
                 web_provider: str,
                 contract_address: str,
                 prize_key: str):
        self.w3 = Web3(Web3.HTTPProvider(web_provider))
        self.prize_contract_address = contract_address
        with open('contract.abi', 'r') as file:
            self.prize_contract_abi = json.load(file)

        # Connect to the contract
        self.prize_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.prize_contract_address),
            abi=self.prize_contract_abi)
        self.__prize_address = Web3.to_checksum_address("0x816a81fb3E083fD85d8ae4fd2e7Fe381a4883d87")
        self.__prize_private_key = prize_key

    def get_prize_pool_balance(self):
        balance = self.w3.eth.get_balance(self.__prize_address)
        return balance

    def transfer_prize(self, user_address) -> str:
        nonce = self.w3.eth.get_transaction_count(self.__prize_address)
        gas_price = self.w3.eth.gas_price
        gas_limit = Web3.to_wei(21000, 'wei')
        transaction_fee = gas_price * gas_limit
        balance = self.get_prize_pool_balance()
        value_to_send = balance - transaction_fee

        tx = {
            'nonce': nonce,
            'to': user_address,
            'value': value_to_send,
            'gas': gas_limit,
            'gasPrice': gas_price
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.__prize_private_key)  # send the transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

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
    private_key = os.environ.get("PRIZE_ADDRESS_PRIVATE_KEY")
    driver = SMCDriver(web_provider="https://1rpc.io/sepolia",
                       contract_address="0xE2ed2a7BeE11e2C936b7999913E3866D4cfc4f8E", prize_key=private_key)
    tr_hash = "0xebcca293f19d597c492e25049665a66a9d8b9f163128c83948c86efbad9d3040"
    print(driver.get_msg_hash(transaction_hash=tr_hash))

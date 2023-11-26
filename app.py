from flask import Flask, jsonify, render_template, session
from web3 import Web3
import requests
import json

app = Flask(__name__)

infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID '
web3 = Web3(Web3.HTTPProvider(infura_url))
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your secret key

@app.route('/new_account', methods=['GET'])
def new_account():
    account = web3.eth.account.create('YOUR_PASSWORD')
    session['account'] = {
        'privateKey': account.key.hex(),
        'address': account.address
    }
    return jsonify(session['account'])

with open('erc20_abi.json') as f:
    erc20_abi = json.load(f)

@app.route('/balance/<contract_address>', methods=['GET'])
def get_balance(contract_address):
    address = session.get('account').get('address')
    checksum_address = Web3.to_checksum_address(address)
    print(checksum_address)
    contract = web3.eth.contract(address=contract_address, abi=erc20_abi)
    balance = contract.functions.balanceOf(checksum_address).call()
    return jsonify({'balance': balance})

@app.route('/market_chart/<contract_address>/<days>', methods=['GET'])
def get_market_chart(contract_address, days):
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/ethereum/contract/{contract_address}/market_chart?vs_currency=usd&days={days}')
    market_chart = response.json()
    return jsonify(market_chart)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import json
import grpc

from solidity_parser import parser

from .stubs import sidechain_eth_pb2, sidechain_eth_pb2_grpc
from elastos_adenine.settings import REQUEST_TIMEOUT


class SidechainEth:

    def __init__(self, host, port, production):
        if not production:
            self._channel = grpc.insecure_channel('{}:{}'.format(host, port))
        else:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
        self.stub = sidechain_eth_pb2_grpc.SidechainEthStub(self._channel)

    def close(self):
        self._channel.close()

    def deploy_eth_contract(self, api_key, network, eth_account_address, eth_private_key, eth_gas, filename):
        with open(filename, 'r') as myfile:
            contract_source = myfile.read()
        contract_metadata = parser.parse_file(filename)
        contract_name = contract_metadata['children'][1]['name']
        req_data = {
            'eth_account_address': eth_account_address,
            'eth_private_key': eth_private_key,
            'eth_gas': eth_gas,
            'contract_source': contract_source,
            'contract_name': contract_name,
        }
        response = self.stub.DeployEthContract(sidechain_eth_pb2.Request(api_key=api_key, network=network, input=json.dumps(req_data)), timeout=REQUEST_TIMEOUT)
        return response

    def watch_eth_contract(self, api_key, network, contract_address, contract_name, contract_code_hash):
        req_data = {
            'contract_address': contract_address,
            'contract_name': contract_name,
            'contract_code_hash': contract_code_hash,
        }
        response = self.stub.WatchEthContract(sidechain_eth_pb2.Request(api_key=api_key, network=network, input=json.dumps(req_data)), timeout=REQUEST_TIMEOUT)
        return response

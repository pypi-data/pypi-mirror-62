import json
import grpc

from .stubs import hive_pb2, hive_pb2_grpc
from elastos_adenine.settings import REQUEST_TIMEOUT


class Hive:

    def __init__(self, host, port, production):
        if not production:
            self._channel = grpc.insecure_channel('{}:{}'.format(host, port))
        else:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
        self.stub = hive_pb2_grpc.HiveStub(self._channel)

    def close(self):
        self._channel.close()

    def upload_and_sign(self, api_key, network, private_key, filename):
        req_data = {
            "privateKey": private_key
        }
        with open(filename, 'rb') as myfile:
            file_contents = myfile.read()

        response = self.stub.UploadAndSign(hive_pb2.Request(api_key=api_key, network=network, input=json.dumps(req_data), file_content=file_contents))
        return response

    def verify_and_show(self, api_key, network, request_input):
        response = self.stub.VerifyAndShow(hive_pb2.Request(api_key=api_key, network=network, input=json.dumps(request_input)), timeout=REQUEST_TIMEOUT)
        return response

"""
:synopsis: Necessary setup for the pynetworking library
"""
import pynetworking as net


class ServerFunctions(net.ServerFunctions):
    from Server import greet_client, server_faculty


class ClientFunctions(net.ClientFunctions):
    from Client import client_faculty, client_func


class ServerCommunicator(net.ServerCommunicator):
    remote_functions = ServerFunctions
    local_functions = ClientFunctions


class ClientCommunicator(net.ClientCommunicator):
    remote_functions = ClientFunctions
    local_functions = ServerFunctions


#: alias for all server functions
server = ServerCommunicator.remote_functions


def get_client() -> ClientCommunicator:
    """Main purpose is to supply better auto completions"""
    return net.ClientManager().get()


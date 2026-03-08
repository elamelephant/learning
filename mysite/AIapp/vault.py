import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
keyVaultName = "AIapp-vault"


def get_secret(name):
    KVUri = f"https://AIapp-vault.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    secretName = name
    print(" done.")
    print(f"Retrieving your secret from KV_NAME.")
    retrieved_secret = client.get_secret(secretName)
    #print(f"Your secret is '{retrieved_secret.value}'.")
    return retrieved_secret.value

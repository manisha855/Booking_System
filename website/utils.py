

from django.conf import settings
import os
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12


def generate_token(data):
    message = f"MERCHANTID={data['MERCHANTID']},APPID={data['APPID']},APPNAME={data['APPNAME']},TXNID={data['TXNID']},TXNDATE={data['TXNDATE']},TXNCRNCY={data['TXNCRNCY']},TXNAMT={data['TXNAMT']},REFERENCEID={data['REFERENCEID']},REMARKS={data['REMARKS']},PARTICULARS={data['PARTICULARS']},TOKEN=TOKEN"
    
    # Create the message digest using SHA256
    digest = hashlib.sha256(message.encode('utf-8')).digest()
    
    # Load the private key and certificate
    with open(settings.CONNECTIPS_PRIVATE_KEY_PATH, 'rb') as key_file:
        pfx_data = key_file.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, settings.CONNECTIPS_PRIVATE_KEY_PASSWORD)
    
    # Sign the message digest
    signature = private_key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # Convert the signature to base64
    token = base64.b64encode(signature).decode('utf-8')
    
    return token



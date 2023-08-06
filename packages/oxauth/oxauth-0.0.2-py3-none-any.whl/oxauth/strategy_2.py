import jwe
import jwt

class Strategy2:

    def __init__(self, signature_public_key, signature_algorithm,
                 encryption_private_key, encryption_algorithm, encryption_method,
                 logging_enabled=False):

        # The library we use, PyJWE, only supports the 'A256GCM' encryption algorithm
        # and the 'dir' encryption method.
        # https://github.com/chrisseto/pyjwe#why-is-aes-256-gcm-the-only-encryption-methd
        # https://github.com/chrisseto/pyjwe#why-is-dir-the-only-algorithm-supported

        if 'A256GCM' != encryption_algorithm:
            raise ValueError('"A256GCM" is the only supported encryption algorithm')

        if 'dir' != encryption_method:
            raise ValueError('"dir" is the only supported encryption method')

        self.signature_public_key = signature_public_key
        self.signature_algorithm = signature_algorithm
        self.encryption_private_key = encryption_private_key
        self.logging_enabled = logging_enabled

    def decrypt(self, cookie):

        # Decoding is the reverse of what Accounts does to encode a cookie:
        # Accounts first signs the payload w/ the signature private key, then
        # it next symmetric encrypts that result w/ the encryption private key.

        try:
            decrypted_payload = jwe.decrypt(cookie.encode(), self.encryption_private_key.encode())

            decoded_payload = jwt.decode(
                decrypted_payload,
                self.signature_public_key,
                audience="OpenStax",
                algorithms=[self.signature_algorithm]
            )

            return Payload(decoded_payload)
        except Exception as ee:
            if self.logging_enabled:
                import logging
                logging.exception("Could not decrypt cookie")

            return None

class Payload:
    def __init__(self, payload_dict):
        self.payload_dict = payload_dict
        self.user_uuid = payload_dict['sub']['uuid']


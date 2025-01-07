import random
from byu_pytest_utils import max_score
from rsa import generate_key_pairs
from fermat import mod_exp


@max_score(20)
def test_key_pair_encoding_decoding():
    """Test RSA key pairs for various bit sizes to ensure encoding and decoding work correctly."""

    for bits in [64, 128, 256, 512, 1024]:

        # Generate key pairs
        N, e, d = generate_key_pairs(bits)

        # Ensure that N is large enough to encrypt/decrypt a message of the given bit size
        message: int = random.getrandbits(int(bits / 4))

        # Encrypt the message
        ciphertext = mod_exp(message, e, N)

        # Decrypt the message
        decrypted_message = mod_exp(ciphertext, d, N)

        # Check that the decrypted message matches the original message
        assert (
            message == decrypted_message
        ), f"Failed for bit size {bits}: message={message}, decrypted_message={decrypted_message}"

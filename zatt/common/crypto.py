from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

""" Computes the SHA256 hash of a message. """
def hash(msg):
	"""	
	msg 	- message as a string
	output 	- message digest as bytes
	"""
	digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
	digest.update(msg.encode())
	return digest.finalize()


""" Generates public and private key pair for asymmetric encryption. """
def generate_asymm_key():
	"""
	output	- key pair tuple (private key, public key, 
							serialized private key, serialized public key)
	"""
	private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
	serialized_private = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption()
	)
	serialized_public = private_key.public_key().public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return (private_key, private_key.public_key(), 
		serialized_private, serialized_public)

""" Loads public key for asymmetric encryption. """
def load_asymm_pub_key(s_key):
	"""
	s_key 	- serialized public key as a byte string
	output 	- deserialized public key
	"""
	return serialization.load_pem_public_key(
		s_key,
		backend=default_backend()
	)

""" Loads private key for asymmetric encryption. """
def load_asymm_pr_key(s_key):
	"""
	s_key 	- serialized private key as a byte string
	output 	- deserialized private key
	"""
	return serialization.load_pem_private_key(
		s_key,
		password=None,
		backend=default_backend()
	)

""" Computes an elliptic curve (ECDSA) signature of a message. """
def sign_message(msg, key):
	"""
	msg 	- message as a string
	key 	- private key generated by generate_asymm_key()
	output 	- signature as bytes
	"""
	signature = key.sign(msg.encode(), ec.ECDSA(hashes.SHA256()))
	return signature


""" Verifies the elliptic curve (ECDSA) signature of a message. """
def verify_message(msg, key, sig):
	"""
	msg 	- message as string
	key 	- public key generated by generate_asymm_key()
	sig 	- signature as bytes
	output 	- True if signature valid, False otherwise
	"""
	try:
		key.verify(sig, msg.encode(), ec.ECDSA(hashes.SHA256()))
	except InvalidSignature:
		return False
	return True

# msg1 = "Hello World!"
# msg2 = "Hello!"

# (pr_key1, pub_key1, s_pr_key1, s_pub_key1) = generate_asymm_key()
# (pr_key2, pub_key2) = generate_asymm_key()

# for i in range(4):
# 	(_, _, s_pr_key, s_pub_key) = generate_asymm_key()
# 	print(str(s_pr_key))
# 	print(str(s_pub_key))
# 	print("")

# sig11 = sign_message(msg1, pr_key1)
# sig12 = sign_message(msg2, pr_key1)
# s_sig11 = sign_message(msg1, load_asymm_pr_key(s_pr_key1))
# s_sig12 = sign_message(msg2, load_asymm_pr_key(s_pr_key1))
# sig21 = sign_message(msg1, pr_key2)
# sig22 = sign_message(msg2, pr_key2)

# print(verify_message(msg1, pub_key1, sig11))
# print(verify_message(msg2, pub_key1, sig12))
# print(verify_message(msg1, pub_key1, s_sig11))
# print(verify_message(msg2, pub_key1, s_sig12))
# print(verify_message(msg1, load_asymm_pub_key(s_pub_key1), sig11))
# print(verify_message(msg2, load_asymm_pub_key(s_pub_key1), sig12))
# print(verify_message(msg1, pub_key2, sig21))
# print(verify_message(msg2, pub_key2, sig22))

# print(verify_message(msg1, pub_key2, sig11))
# print(verify_message(msg2, pub_key2, sig12))
# print(verify_message(msg1, pub_key1, sig21))
# print(verify_message(msg2, pub_key1, sig22))
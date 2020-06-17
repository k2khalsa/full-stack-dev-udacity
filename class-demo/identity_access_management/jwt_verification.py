# Import Python Package
import jwt
import base64

# Init our Data
payload = {'park': 'madison square'}
algo = 'HS256'  # HMAC-SHA 256
secret = 'learning'

# Encode a JWT
encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(encoded_jwt)

# Decode a JWT
decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True)
print(decoded_jwt)

new_jwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoidW5pb24gc3F1YXJlIn0.N3EaAHsrJ9-ls82LT8JoFTNpDK3wcm5a79vYkSn8AFY'

# Decode with Simple Base64 Encoding
decoded_base64 = base64.b64decode(str(new_jwt).split(".")[1]+"==")
print(decoded_base64)

from datetime import datetime, timedelta
import jwt
from config import JWTConfig


class JWT:
    def encode_auth_token(self, email):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5*60),
                'iat': datetime.utcnow(),
                'email': email
            }

            return jwt.encode(
                payload,
                JWTConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as err:
            return err

    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, JWT.SECRET_KEY)
            return payload['email']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

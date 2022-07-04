from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid authentication scheme')
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail='Invalid token or expired token')
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403, detail='Invalid authorization code')

    def verify_jwt(self, jwt_token: str) -> bool:
        is_valid_token: bool = False

        try:
            payload = decode_jwt(jwt_token)
        
        except:
            payload = None
        
        if payload:
            is_valid_token = True

        return is_valid_token
        
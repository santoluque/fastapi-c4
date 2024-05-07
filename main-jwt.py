from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta


app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "ABC123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

''' SIMULADOR USER '''
simulador_user_db = {
    "_user":{
        "username": "santo.luque",
        "password": "Clave1234"
    }
}

# def create_access
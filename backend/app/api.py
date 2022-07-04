import json
import requests

from decouple import config
from fastapi import FastAPI, Body, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from . import schemas, models, crud
from .database import engine, get_db
from .auth.auth_handler import sign_jwt
from .auth.auth_bearer import JWTBearer


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='JD Prediction Backend Service', version='0.3.7')


@app.post('/user/signup', tags=['user'], response_model=schemas.User)
def create_user(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)


@app.post('/user/login', tags=['user'])
def user_login(user: schemas.UserLogin = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_from_login(db, email=user.email, password=user.password)
    if db_user:
        return sign_jwt(user.email)
        
    return {
        'error': 'Wrong login details!'
    }


@app.post('/predict', dependencies=[Depends(JWTBearer())], tags=['prediction'])
def predic(jd: schemas.JD) -> dict:
    jd = dict(jd)

    headres = {
        "accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }

    request_base_address = config('EXPOSE_PROTOCOL') + '://' + config('SERVE_TF_MODEL_EXPOSE_HOST_ADDR') + ':' + \
        config('SERVE_TF_MODEL_EXPOSE_PORT')
    res = requests.post(request_base_address + '/jd/predict', data=json.dumps(jd), headers=headres)

    return json.loads(res.text)

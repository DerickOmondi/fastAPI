from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



SECRET_KEY = "WBuOXbsIuBil-AWnCfUHXW1n9BEIRbvszgLiHNmlCzU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#function that takes user data

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    ##check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    ##hash the password and create a new user
    hashed_password = utils.hash_password(user.password)

    #creating new user
    new_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password,
        role=user.role
        )

    #saving user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #returning user data without password
    
    return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    

    #"sub" is a standard claim in JWT that represents the subject of the token, which in this case is the username. We also include the user's role in the token for authorization purposes.
    token_data = {"sub": user.username, "role": user.role}
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
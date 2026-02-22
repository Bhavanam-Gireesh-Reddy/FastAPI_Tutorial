from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Helper function that takes user data

def create_access_token(data: dict): # Token Generator
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "User Already Exists")

    # Hash the Password
    hashed_pass = utils.hash_password(user.password)

    # Create new User
    new_user = models.User(
        username = user.username,
        email = user.email,
        password = hashed_pass,
        role = user.role
    )
    # Add this user to database
    db.add(new_user)
    # Commit the Transaction
    db.commit()
    # Refresh the session
    db.refresh(new_user)
    # Return the Registered User details.
    return {"id" : new_user.id, "username" : new_user.username, "email" : new_user.email, "role" : new_user.role}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Credentials")

    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Credentials")

    token_data = {
        "sub" : user.username,
        "role" : user.role
    }

    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate Credentials",
        headers = {"WWW-Authenticate" : "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"username" : username, "role" : role}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message" : "This is a protected route", "user" : current_user}

def require_role(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to access this route")
        return current_user
    return role_checker

@app.get("/profile")
def profile(current_user : dict = Depends(require_role(["user", "admin"]))):
    return {"Message" : f"Profile of {current_user['username']} with role {current_user['role']}"}

@app.get("/user/dashboard")
def user_dashboard(current_user : dict = Depends(require_role(["user"]))):
    return {"Message" : "Welcome To User Dashboard"}

@app.get("/admin/dashboard")
def admin_dashboard(current_user : dict = Depends(require_role(["admin"]))):
    return {"Message" : "Welcome To Admin Dashboard"}
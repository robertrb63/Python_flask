from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2=OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username:str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    

users_db ={
    "mouredev":{
        "username": "robert",
        "full_name": "Robert Moure",
        "email": "rr@gmail.com",
        "disabled": False,
        "password": "1234"
    },
    "mouredev2":{
        "username": "robertrb",
        "full_name": "Robert2 Moure",
        "email": "rb@gmail.com",
        "disabled": True,
        "password": "1234"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas", headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario Inactivo", headers={"WWW-Authenticate":"Bearer"})
    
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    
    user= search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    return {"access_token": form.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) #Ejecutar el server en el puerto 8000

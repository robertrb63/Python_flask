"""
https://www.youtube.com/watch?v=_y9qQZXE24A&t=4420s
"""

from fastapi import FastAPI as fast
app = fast()
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name:str
    apellido: str
    direccion: str

usersList =[
            User(id=1 ,name="Roberto", apellido="builes", direccion="Calle escuelas"),
            User(id=2 ,name="Gabi", apellido="builes", direccion="Calle escuelas")
            ]


@app.get("/")  # Este metodo devuelve la lista en formato json
def index():
    return {"message": "Welcome to my FastAPI!"}


@app.get("/users")  # Este metodo devuelve la lista en formato json
async def users():
    try:
        return usersList
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


@app.get("/user/{id}")
async def user(id: int):
    users=filter(lambda user: user.id == id, usersList)
    #return usersList.index(id)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}

@app.get("/query/")
async def user(id: int):
    users=filter(lambda user: user.id == id, usersList)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
"""
    se llama desde el navegador:   http://localhost:8000/query/?id=1
"""

"""
se puede crer una funcion con la tarea de buscar un usuario
"""
def search_user(id: int):
    users=filter(lambda user: user.id == id, usersList)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}


#MUCHO MAS CORTO POR QUE SE USA LA FUNCION: def search_user, QUE SE PUEDE REUTILIZAR
@app.get("/user_def/{id}")
async def user(id: int):
    return search_user(id)


#POST: AGREAGAR UN USUARIO
@app.post("/user/")
async def add_user(user: User):
    if type(search_user(user.id))== User:
        return {"error":"El usuario ya existe"}
    else:
        usersList.append(user)
        return {"message": "Usuario agregado correctamente"}


#PUT:  ACTUALIZAR UN USUARIO
@app.put("/user/")
async def user(user:User):
    found = False
    for index, saved_user in enumerate(usersList):
        if saved_user.id == user.id:
            usersList[index] = user
            found = True       
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    return user

#DELETE: BORRAR DATOS
@app.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(usersList):
        if saved_user.id == id:
            del usersList[index]
            found = True       
    if not found:
        return {"error":"No se ha encontrado el usuario"}
    return {"message": "Usuario eliminado correctamente"}






@app.get("/usersJson")
async def root(): #Siempre que se llama un servidor la funcion deber ser asincrona
    return ({"name": "robert", "apellido":"Restrepo", "direccion": "Calle Escuelas 3"},
            {"name": "Antonio", "apellido":"builes", "direccion": "Calle Escuelas 3"},
            {"name": "robert", "apellido":"Restrepo", "direccion": "Calle Escuelas 3"},
            {"name": "Antonio", "apellido":"builes", "direccion": "Calle Escuelas 3"}
        )

@app.get("/index")
async def index(): #Siempre que se llama un servidor la funcion deber ser asincrona
    return {"message": "Ahora me encuentro en index!"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) #Ejecutar el server en el puerto 8000

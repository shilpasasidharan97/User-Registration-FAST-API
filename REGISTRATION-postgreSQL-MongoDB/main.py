import base64

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from routers import user
from passlib.context import CryptContext
from pymongo import MongoClient

from database import MONGO_DATABASE, mongo_db, pg_conn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Dependency to get the PostgreSQL connection
def get_postgres_conn():
    try:
        yield pg_conn
    finally:
        pg_conn.close()


# Dependency to get the MongoDB connection
def get_mongodb_conn():
    try:
        yield MONGO_DATABASE
    finally:
        MongoClient.close()


# Mount routers with dependencies
# app.include_router(user.router, prefix='/user', tags=['users'], dependencies=[Depends(get_postgres_conn), Depends(get_mongodb_conn)])

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# get all the users
@app.get("/")
async def register(request: Request):
    # Fetch all the user details from PostgreSQL database
    cursor = pg_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    # Fetch profile picture  from MongoDB database
    users_with_profile_picture = []
    collection = mongo_db["profile_picture"]
    for user in users:
        id, name, email, phone, password = user
        user_dict = {
            "id": id,
            "name": name,
            "email": email,
            "password": password,
            "phone": phone,
        }
        collection = mongo_db["profile_picture"]
        profile_pictures = collection.find_one({"user_id": str(user_dict["id"])})
        if profile_pictures:
            image = profile_pictures["profile_picture"]
            profile_picture_data = base64.b64encode(image).decode("utf-8")
            user_dict["profile_picture"] = profile_picture_data
        users_with_profile_picture.append(user_dict)
    return templates.TemplateResponse(
        "registration.html",
        {
            "request": request,
            "users": users_with_profile_picture,
        },
    )


# user registration
@app.post("/")
async def submit(request: Request):
    cursor = pg_conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL);"""
    )

    form_data = await request.form()
    full_name = form_data.get("name")
    email = form_data.get("email")
    phone = form_data.get("phone")
    password = form_data.get("password")
    profile_pic = form_data.get("profile")

    # checking email is exists or not
    query = f"SELECT email FROM users WHERE email='{email}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        return {"message": "Email already exists!"}
    # user details to PostgreSQL
    query = f"INSERT INTO users (full_name, email, password, phone) VALUES ('{full_name}', '{email}', '{pwd_context.hash(password)}', '{phone}') RETURNING id"
    cursor.execute(query)
    user_id = cursor.fetchone()[0]
    pg_conn.commit()
    cursor.close()
    # profile pic to MongoDB
    file_content = (
        await profile_pic.read()
    )  # read the contents of the uploaded profile pic
    collection = mongo_db["profile_picture"]
    result = collection.insert_one(
        {"user_id": str(user_id), "profile_picture": file_content}
    )
    return templates.TemplateResponse(
        "registration.html",
        {"request": request, "message": "Registration successful"},
    )


# unique registered user
@app.get("/user-details/{id}")
async def display_user_details(request: Request, id: int):
    # Fetch user data from PostgreSQL database
    cursor = pg_conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  
    user_dict = {"full_name": user[1], "email": user[2], "phone": user[3]}
    # Fetch profile picture from MongoDB database
    collection = mongo_db["profile_picture"]
    profile_picture = collection.find_one(
        {
            "user_id": str(id),
        }
    )
    if profile_picture:
        image = profile_picture["profile_picture"]

        decoded_profile_picture = {
            "image_data": base64.b64encode(image).decode("utf-8")
        }
        user_dict["profile_picture"] = decoded_profile_picture
    # Render the user details template
    return templates.TemplateResponse(
        "user_details.html",
        {
            "request": request,
            "user": user_dict,
        },
    )

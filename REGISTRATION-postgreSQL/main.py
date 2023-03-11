from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import pg_conn

# Define the FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Create the Users table
cur = pg_conn.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL UNIQUE
    )
"""
)
pg_conn.commit()

# Create the Profile table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS profile (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        profile_picture TEXT NOT NULL
    )
"""
)
pg_conn.commit()


# Template Loading
@app.get("/", response_class=HTMLResponse)
async def register_form(request: Request):
    # Return an HTML response with a success message
    return templates.TemplateResponse(
        "registration_form.html",
        {
            "request": request,
        },
    )


# registrarion
@app.post("/")
async def register_user(request: Request):
    form_data = await request.form()
    full_name = form_data.get("full_name")
    email = form_data.get("email")
    phone = form_data.get("phone")
    password = form_data.get("password")
    profile_picture = form_data.get("profile_picture")
    # Check if the email or phone number already exist
    cursor = pg_conn.cursor()
    cursor.execute(
        """SELECT * FROM users WHERE email = %s OR phone = %s""", (email, phone)
    )
    result = cursor.fetchone()
    if result:
        raise HTTPException(status_code=400, detail="Email or phone already exist")
    # Insert the user data into the user table
    cursor.execute(
        """
        INSERT INTO users (first_name, password, email, phone)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (full_name, password, email, phone),
    )
    user_id = cursor.fetchone()[0]
    # Insert the profile data into the profile table
    with profile_picture.file as profile:
        profile_picture_bytes = profile.read()
    cur.execute(
        """
        INSERT INTO profile (user_id, profile_picture)
        VALUES (%s, %s)
    """,
        (user_id, profile_picture_bytes),
    )
    pg_conn.commit()
    return templates.TemplateResponse(
        "registration_form.html",
        {
            "request": request,
        },
    )


# list of all users
@app.get("/users/", response_class=HTMLResponse)
async def get_user_profile(request: Request):
    # Retrieve the user details and profile picture from the database
    cursor = pg_conn.cursor()
    cursor.execute(
        """
            SELECT u.id, u.first_name, u.email, u.phone, p.profile_picture
            FROM users u
            JOIN profile p ON u.id = p.user_id
            WHERE u.id = p.user_id;
        """
    )
    result = cursor.fetchall()
    # Check if user was found
    if not result:
        return templates.TemplateResponse("user_not_found.html", {"request": request})
    # Render the results in the HTML template
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "registered_users": result,
        },
    )


# unique registered user
@app.get("/user-details/{user_id}")
async def display_user_details(request: Request, user_id: int):
    # Fetch user data from PostgreSQL database
    cursor = pg_conn.cursor()
    cursor.execute(
        """
            SELECT u.id, u.first_name, u.email, u.phone, p.profile_picture
            FROM users u
            JOIN profile p ON u.id = p.user_id
            WHERE u.id = %s;
        """,
        (user_id,),
    )
    user = cursor.fetchone()
    return templates.TemplateResponse(
        "user_details.html",
        {
            "request": request,
            "user": user,
        },
    )

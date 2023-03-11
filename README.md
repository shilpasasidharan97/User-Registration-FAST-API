# User-Registration-FAST-API
This repository contains two projects:  
  1. REGISTRATION-postgreSQL-MongoDB
  2. REGISTRATION-postgreSQL
  
 Prerequisite :
  1. Install virtualenv using command : 
        pip install virtualenv
  1. Install PostgreSQL and MongoDB on your machine

  
PROJECT 1 : 
REGISTRATION-postgreSQL-MongoDB
  This program is a user registration system developed in FastAPI that utilizes two databases - PostgreSQL and MongoDB. The registration process requires the user to provide their Full Name, Email, Password, Phone number, and Profile picture. The user's First Name, Password, Email, and Phone number are stored in PostgreSQL, while their Profile picture is stored in MongoDB. 
Installation :
  1. Clone the repository to your local machine using the following command:
        git clone https://github.com/shilpasasidharan97/User-Registration-FAST-API.git
  2. Change the Directiory to REGISTRATION-postgreSQL-MongoDB using the command :
        cd REGISTRATION-postgreSQL-MongoDB
  3. Create a virtual environment. For example, you can use virtualenv by running the command: 
        virtualenv venv
  4. Activate the virtual environment by running the command: 
        source venv/bin/activate (for Linux/Mac) or 
        venv\Scripts\activate (for Windows).
  5. Install the required dependencies by running the command:
        pip install -r requirements.txt
  6. Create a PostgreSQL database named "users"
  7. Create a MongoDB database named "profile_pictures".
  8. Start the FastAPI application by running the command: 
        uvicorn main:app --reload
  9. The application is now running on http://localhost:8000.
  
  
PROJECT 2 : 
REGISTRATION-postgreSQL
  This program is a user registration system developed in FastAPI that utilizes databases - PostgreSQL. Register a new user with the following information: Full Name, Email, Password, Phone, and Profile Picture. It stores user information in two separate tables in a PostgreSQL database - Users and Profile. The Users table stores First Name, Password, Email, and Phone, and the Profile table stores the Profile Picture. The program also checks whether the Email or Phone number already exists in the database before creating a new user.
Installation :
  1. Clone the repository to your local machine using the following command:
        git clone https://github.com/shilpasasidharan97/User-Registration-FAST-API.git
  2. Change the Directiory to REGISTRATION-postgreSQL using the command :
        cd REGISTRATION-postgreSQL
  3. Create a virtual environment. For example, you can use virtualenv by running the command: 
        virtualenv venv
  4. Activate the virtual environment by running the command: 
        source venv/bin/activate (for Linux/Mac) or 
        venv\Scripts\activate (for Windows).
  5. Install the required dependencies by running the command:
        pip install -r requirements.txt
  6. Create a PostgreSQL database named "user_db"
  8. Start the FastAPI application by running the command: 
        uvicorn main:app --reload
  9. The application is now running on http://localhost:8000.
 10. Get user details:
        URL: http://localhost:8000/user/
       

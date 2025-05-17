# Cleaning Service Platform: CSIT314 Team The ScrumLord's Assignment

A web platform for managing cleaning services involving User Admins, Platform Managers, Cleaners and Homeowners. Using **Flask**, each roles will have access to specific pages for managing users, services, bookings, and reports.
---
## Project Structure
CSIT314/
|- boundary/ ## UI Logic per user role
| |- admin/
| |- cleaner/
| |- homeownder/
| |- platformManager/
|
|- controller/ ## Business Logic per user role (create, retrive, update, delete, suspend, login, logout)
| |- admin/
| |- cleaner/
| |- homeownder/
| |- platformManager/
|
|- entity/ ## Database models per user role
| |- admin/
| |- cleaner/
| |- homeownder/
| |- platformManager/
|
|- templates/ ## HTML templates for each roles (create, retrive, update, delete, suspend, login, logout)
| |- admin/ 
| |- cleaner/ 
| |- homeownder/
| |- platformManager/
| - index.html ## Main Login Page/Template for Main Page
|
|- dataGenerator.py ## Script to populate DB with sample data 
|- db_config.py ## Database configuration setup
|- main.py ## Main Flask App Entry Point
|- requirements.txt ## Python Dependencies
|- readMe.md
---
## Technologies Used
- Python 3.11.0
- Flask
- Flask SQLAlchemy
- Jinja2 Templating
- MySQL Workbench(configured Database)
- VS Code (for development)
---
## Installation & Setup Instructions

Follow these steps to set up and run the project locally:

### Prerequisities
Ensure that the following are installed:
- Python 3.8 or above (3.11.0 used for developement of this app)
- MySQL Server and MySQL Workbench
- pip (Python package manager)
- Git (optional)

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/csit314-cleaning-platform.git
cd csit314-cleaning-platform 
```

### 2. Create and Activate a Virtual Environment
```bash
# For Windows
python3 -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installed Required Packages
```bash
pip install -r requirements.txt

# For missing requirements.txt, create with:
pip freeze > requirements.txt
```

### 4. My SQL Workbench Installation
If you do not have MySQL Server and MySQL Workbench installed:

For Windows/Mac: https://dev.mysql.com/downloads/installer/

MySQL Workbench only (if server is already installed): https://dev.mysql.com/downloads/workbench/ 

# Note: When setting up MySQL, rememeber the root password you set, it is needed in db_config.py

### 5. Configure Database

    1. Open MySQL Workbench and connect to your MySQL Server.
    2. Copy and paste SQL Query in schema.sql file and run.
    3. Run dataGenerator.py in terminal to populate database with sample data.

    OR 

    1. Open MySQL Workbench and connect to your MySQL Server.
    2. On the top menu bar, click File and Select Open SQL Script.
    3. Navigate to this project directory and select schema.sql.
    4. Run the SQL script to create database.
    5. Run dataGenerator.py in terminal to populate database with sample data.

---
After configuration, go to db_config.py and update your credentials.

### 6. Run the application
- Right click on main.py and run the Python file in terminal.
- Visit http://127.0.0.1:5000 for the applicaton.

### Default Login Credentials
User Admin
- username: john@gmail.com
- password: john678

Cleaner
- username: mary@gmail.com
- password: mary@345

Homeowner
- username: james@gmail.com
- password: james223

Platform Manager
Homeowner
- username: peter@gmail.com
- password: peter456
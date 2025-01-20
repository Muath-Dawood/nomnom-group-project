# NumNum Web Application

NumNum is a full-stack web application designed to bring food enthusiasts together by sharing and interacting with recipes.
This project was developed as part of the graduation requirements for the Full Stack Online Bootcamp by AXSOS Academy.

![image](https://github.com/user-attachments/assets/f4fc1184-bcac-470a-ad1c-6e64b5135d2b)

# Table of Contents:

* Project Description
* Features
* Technologies Used
* Installation and Setup
* Data Models
* File Structure
* Team


# Project Description:

NumNum provides a platform for users to:

* Browse, filter, and search recipes by title, ingredients, or rating.
* Share their own recipes with detailed descriptions and images.
* Interact with the community by rating and reviewing recipes.
* Manage their profiles and view their own recipes.
* The platform ensures secure user authentication and offers a responsive design for accessibility on various devices.


# Features:

* User Authentication:
* Secure login and registration using email as the primary identifier.
* Custom user profiles with profile pictures and addresses.



# Recipe Management:

* Add, edit, and delete recipes with fields like title, description, ingredients, and instructions.
* Upload and process recipe images with automatic resizing and renaming.


# Community Features:

* Rate and review recipes with AJAX-powered dynamic updates.
* View detailed recipe pages with ratings and reviews.
* Search and Filtering:
* Search for recipes by title or ingredients.
* Filter recipes by ratings and popularity.


# Responsive Design:

* Mobile-friendly layouts and dynamic user interactions.


# Technologies Used:

* Backend: Django 5.1.4, Django Environ
* Frontend: HTML, CSS, JavaScript, AJAX
* Database: MySQL
* Image Processing: Pillow

# requirements files:

* asgiref==3.8.1
* Django==5.1.4
* django-environ==0.11.2
* mysqlclient==2.2.6
* pillow==11.0.0
* sqlparse==0.5.3
* typing_extensions==4.12.2


# Installation and Setup

### Clone the repository

```bash
$ git clone (https://github.com/ENGBaselsaad/nomnom-group-project.git)
```

### Navigate to the project directory

```bash
$ cd nomnom
```

### Create and activate a virtual environment:

```bash
$ python -m venv venv
```
* On Windows: venv\Scripts\activate


### Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configure the environment variables:

Create a .env file in the project root.

Add database credentials and other configurations.


### Run database migrations:

```bash
python manage.py migrate
```

### Start the development server:

```bash
python manage.py runserver
```

* Access the application at http://127.0.0.1:8000.


# Data Models

## 1. User Model (Custom):

* Fields: Email, First Name, Last Name, Address, Profile Picture.
* Email is used as the primary identifier.



## 2. Recipe Model:

* Fields: Title, Description, Ingredients, Instructions, Image, Created By.
* Features: Average rating calculation, image processing for resizing and renaming.


## 3. Review Model:

* Fields: Recipe, Reviewer, Rating, Comment.
* Features: Validation for rating range and comment length.


# File Structure:

![image](https://github.com/user-attachments/assets/41f3e132-a3d7-4225-8465-642230a9d249)



# Team:
* Basel Saad
* Muath Dawood
* Aseel Khzaimiah
* Muath Nassar

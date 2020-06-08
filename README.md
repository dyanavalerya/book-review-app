CS50W Project 1
===============

Web Programming with Python and JavaScript
------------------------------------------

### [https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/)

Check the app on the Heroku link
--------------------------------

### [https://my-book-review-api.herokuapp.com/](https://my-book-review-api.herokuapp.com/)


Objectives
----------

*   Become more comfortable with Python.
*   Gain experience with Flask.
*   Learn to use SQL to interact with databases.

Project description
-------------------

This web app contains filtered (by isbn, title, author) book search, review submission, register session, get book info by isbn API, and integration with the Goodreads API to get reviews data per individual book. 

**Used tools:** Material Design Bootstrap, PostgreSQL, Flask, Heroku. 

**File description:** 
- `application.py` is the main program;
- `import.py` is the program that is used to import the `.csv` file into the database provided by Heroku;
- `templates` folder contains the `.html` files with suggestive names for each section, and the `includes` folder which contains specific section parts of the app that are included into the files from the templates folder. The purpose of it is to make it easier to make changes, find bugs and understand the code structure.
- `requirements.txt` is an auto-generated file that contains the necessary python packages neccessary to run the application

How to run
----------
```bash
# Clone repo
$ git clone https://github.com/dyanavalerya/book-review-app.git

$ cd book-review-app

# Before installing any python packages I would recommend to create a virtual environment first
# You can do that with Anaconda

# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables
$ export FLASK_APP=application.py
$ export FLASK_ENV=development
$ export DATABASE_URL=your remote or local database url
$ export GOODREADS_KEY=your Goodreads API key which you can get at: https://www.goodreads.com/api
$ flask run
```


DB Schema
---------
![](/img/2020-06-08_17-10.png)


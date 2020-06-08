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

This web app contains filrered (by isbn, title, author) book search, review submission, register session, get book info by isbn API, and integration with the Goodreads API to get reviews data per individual book. 

**Used tools:** Material Design Bootstrap, PostgreSQL, Flask, Heroku. 

**File description:** 
- `application.py` is the main program;
- `import.py` is the program that is used to import the `.csv` file into the database provided by Heroku;
- `templates` folder contains the `.html` files with suggestive names for each section, and the `includes` folder which contains specific section parts of the app that are included into the files from the templates folder. The purpose of it is to make it easier to make changes, find bugs and understand the code structure.
- `requirements.txt` is an auto-generated file that contains the necessary python packages neccessary to run the application


### Gallery
```gallery(42h)
![2020-06-08_10-23.png](:storage/03878f0e-7409-4dad-94f7-35fa70435bff/6769d480.png)
![2020-06-08_10-03.png](:storage/03878f0e-7409-4dad-94f7-35fa70435bff/01bf29d8.png)
![2020-06-08_10-04.png](:storage/03878f0e-7409-4dad-94f7-35fa70435bff/55fb889a.png)
![2020-06-08_10-05.png](:storage/03878f0e-7409-4dad-94f7-35fa70435bff/e3a9978e.png)
```

DB Schema
---------
![8a2e0743.png](:storage/03878f0e-7409-4dad-94f7-35fa70435bff/8a2e0743.png)


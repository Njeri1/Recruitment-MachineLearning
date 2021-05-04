# Recruitment-MachineLearning

Grading resumes according to job description using natural language processing.

DESCRIPTION: Comparision of text is done between JobDescription(.txt) file and bunch of resumes(.pdf) using natural language processing. Two python files resume.py and flask_old.py(which uses flask) are used in this project. Flask is a python web framework which uses python decorators. They help in calling a function before the user's request is processed.

REQUIREMENTS: Python 3.7.3 is used in this project. In addition to python following libraries are required to run the code. For resume.py code slate3K, re, logging, sklearn, pathlib, operator are required. For flask_old.py flask, werkzeug, os, pathlib, re, resume(i.e., resume.py) are used.

WORKING: In order to use flask framework, it should be running in background. So first run the flask_old.py code. It displays a link http://127.0.0.1:5000/. Click the link. Then upload the resumes and jobDescription files which will be stored in local machine. Click compare button. After clicking compare button it takes some time depending on the number of resumes uploaded, list of the names and scores will be appear.

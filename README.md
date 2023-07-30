Smart Finance
========================
Description:
-------------------------
Yatube is a social network with the ability to:  
     register,   
     create, edit and delete posts,  
     view, comment on posts by other authors,  
     subscribe and unsubscribe to authors.    

Technologies Stack:  
-------------------------
  * Python 3.9  
  * Django 2.2  
  * Pillow   
  * sorl-thumbnail  


Installation and launch:
-------------------------
 
Clone the repository. On the command line:
```
     git clone https://github.com/Ruzal-Z/smart_finance.git
```
or use SSH-key:
```
     git clone git@github.com:Ruzal-Z/smart_finance.git
```
Install and activate the virtual environment
```
     python -m venv venv
```
```
     source venv/Scripts/activate
```
Install dependencies from the file requirements.txt
```
     pip install -r requirements.txt
```
Make migrate:
```
     python manage.py migrate
```
Run a project in dev-mode:
```
     cd smart_finance/  
```
```
     python manage.py runserver
```
Open in your browser `localhost` or `127.0.0.1:8000`


Author:
-------------------------
Ruzal Zakirov

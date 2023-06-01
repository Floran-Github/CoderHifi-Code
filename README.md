# CoderHifi-Code `<Hi>`
CoderHi is a website, whose <b>backend</b> is written in <b>Python</b> and <b>Jquery</b>
and uses the <b>Django framework. The <b>frontend</b> is written by <b>html, css</b>. For
<b>beta mode Sqlite</b> is used as the database once the website will be live the
data will be transfer to <b>postgresQL</b>.<br>
Frontend framework used are <b>Bootstrap, FontAwesome .Admin,toastr.js,
Slick.js</b>.<br>
Javascript frameworks like <b>OverlayScrollbars, dataTables ,adminlte,
overlayScrollbars, jquery-cookie, pooper.js</b> are used in the system.
  
## Features
<ul>
  <li>Project Showcase
  <li>Event Management
  <li>Communication between Teacher and Student
  <li>Improve Job Recommendation system
  <li>Decrease job profile spamming
  <li>Job Applies sorting system
</ul>
  
## Pictures :- https://drive.google.com/file/d/1o3AuLwchXqyuo__VnxDTu0vPPRztiqhC/view?usp=sharing

## Usuage

### Clone Repository

Copy Paste the following commands to clone the repo

```bash
 git clone https://github.com/Floran-Github/CoderHifi-Code/
```
Go inside the directory and install the module from requirements.txt

```bash
  pip install -r requirements.txt
 ```
 
 Then make the migrations and then migrate the database
 
 ```bash
    python manage.py makemigrations
    python manage.py migrate
  ```
  
  Create the superuser 
  
  ```bash
    python manage.py createsuperuser
  ```
  
  Now run the django server
  
  ```bash
    python manage.py runserver
  ````
  
  <h2>Now you goto localhost:8000 to see the website</h2>
  
  ```bash
      http://127.0.0.1:8000/
  ```
  

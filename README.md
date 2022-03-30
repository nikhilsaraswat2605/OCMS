# OCMS

## How to Install and Run this project?

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]

*Alternative to Pip is Homebrew*

### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment


For Windows/Linux/Mac OS
```
$  python3 -m venv myenv
```
or
```
$  virtualenv myenv
```

Activate Virtual Environment

For Windows
```
$  source myenv/scripts/activate
```

For Linux/Mac OS
```
$  source myenv/bin/activate
```


**3. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```


**4. Now Run Server**


Command for Windows/Linux/Mac OS:
```python
$ python3 manage.py runserver
```

Note:- While running the server, if any module causes some problem (as such possibility is very less), then manually first unistall that particular module and then reinstall it using -  ***pip install {module name}***

**5. Login Credentials**

Create Super User (HOD)
```
$  python manage.py createsuperuser
```
Then Add Username and Password


*For HOD / SuperAdmin:*

For Example:

Username: admin@gmail.com
Password: admin

*For Teacher / Professor:*

Go on Teacher signup page and create account and login

*For Student:*

Go on Teacher signup page and create account and login
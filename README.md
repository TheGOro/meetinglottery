# Meeting lottery 
The purpose of this tool is to help our team (XFT Hercules) to decide who goes to the technical coordination (simply called as TeCo) meeting on the given week.

It does by tracking the participation of each member and defines a probability for every person based on their participations.

## Instructions to start the application
Create a virtualenv
```
virtualenv ~/.virtualenv/meetinglottery
```
Activate the previously created virtualenv
```
source ~/.virtualenv/meetinglottery/bin/activate
```
Install the application requirements
```
pip install -r requirements.txt
```
Start the application using the development server:
```
python manage.py runserver
```

# TalentHub_v1

How to install TalentHub locally:
- install python 3.7.2
- install [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- clone repo and install requirements
```
git clone https://github.com/Rychh/TalentHub_v1
pip install -r requirements.txt
```
- complete setup
```
chmod +x setup.sh
./setup.sh
```
- export two secret key environment variables 
   - they are located in docs, and contain secret keys hence should not be part
of public repository. It is propably best to add them to .bashrc

- run heroku localy 
``` 
heroku local web 
```

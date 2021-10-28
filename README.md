# 447Team1Project

### Steps to download database/tables/data:
(Prerequisites: Need MySQL Community Server (Full option) downloaded onto your computer)

1)  Download 'DB_Import.sql' (if you have this repository, it's included in here)
2)  Connect to your localhost instance on MySQL Workbench
3)  Once connected, click 'Server' on the menu bar
4)  Click 'Data Import'
5)  Enable the radio button 'Import from Self-Contained File'
6)  Browse for your locally downloaded 'DB_Import.sql' file, and open it
7)  Click 'Start Import'

The database, along with the pre-made tables should be populated with data

### Running the api
1. If you don't have pipenv, install pipenv with `pip install pipenv`
2. In the API folder, run the command `pipenv install`
3. Fill in the credentials for your MySQL server in `app.py` (line 11)
4. Run the flask server with `pipenv run flask run`

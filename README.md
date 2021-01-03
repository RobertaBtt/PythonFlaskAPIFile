# Python Flask API File


```
sudo apt install python3-venv
virtualenv -p /usr/bin/python3.8 PYTHON_ENV_3.8
source PYTHON_ENV_3.8/bin/activate
pip install -r requirements.txt 
```

```
FLASK_APP=app.py flask run
```

The CRUD operation are done using the HTTP protocol:

- GET for reading lists of files (Read)
- GET for read one file if it is specified
- POST for creating a new file  (Create)
- DEL for deleting the file (Delete)
- PUT for update the file (Update)



I test the API using curl and Postman


API are:

- http://localhost:5000/  [GET]
- http://localhost:5000/  [POST]
- http://localhost:5000/files [GET]
- http://localhost:5000/files/<file_name> [GET]
- http://localhost:5000/files/<file_name> [DELETE




Locally updated to Python3.8, fix virtual environment python 3.8

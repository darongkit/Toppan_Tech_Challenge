This API is:
1. build on Flask,
2. Database: MySql Workbench

Set Up steps:
Ensure all dependencies from requirements.txt is installed using pip or pip3

Set up ur api virtual environment (on powershell):
    $env:FLASK_APP =  "application.py"
    $env:FLASK_ENV = "development"
    venv/Scripts/activate

Set up and Run MySql Workbench
    create Database: University
    username: root
    password: root
    execute insert_data.py to load sample data
    (sample dat generated using ChatGPT)

Once Database is running, venv is activated.
type Flask run to run the API.

Postman was used to test the api response.
    refer to the postman_api_requests json file for reference.
    To use the json file: 
        Import file into your postman software.
        If not installed, install postman from official website.
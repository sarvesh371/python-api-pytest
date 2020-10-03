# python-api-pytest
This is a framework repo for api automation using python with pytest

**Pre Requisites**
1. Download and setup python3 from : https://www.python.org/downloads/
2. Before starting the tests perform the steps mentioned in https://github.com/digitalorigin/pg-qa-assignment#feature-2-test-automation-of-a-json-api to start the service in localhost

**Setup the framework and requirements and execute Test**
1. `cd python-api-pytest`
2. Run venv_setup.sh if you are mac or change the commands according to your os for setting up venv and downloading packages
    
    `sh venv_setup.sh`

3. Select the interpreter by going into preferences (No need if you are going to run tests from terminal)
4. `source venv/bin/activate`
5. Run test using pytest command and tests directory

    `pytest tests`

**Project Structure**
1. base - It contains all the common functions and workers functions
2. resources - It contains all url configurations which will be used throughout the project
3. tests - It contains the test class which needs to be triggered
5. allure-results - folder to save our allure report
    
    a. run `allure serve` to get the allure report on localhost
    
    b. run `allure generate` to generate a allure report and it will be saved under /allure-report

7. conftest - as it is heart of pytest, we will keep only fixture and pytest methods there
8. requirements.txt - we will write all our dependency there and then download in one shot using `venv_setup.sh`
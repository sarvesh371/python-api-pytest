# python-api-pytest

**Framework Setup**

**Prerequisites**

1. Download and set up python3 from Download Python or you can use brew to install.
2. This codebase supports 3.9+

It has been observed that sometimes the environment setup turns out to be a tedious and time taking task. But we have
made it simple, now you just have to run a shell script and you are good to go.

Please follow the below commands to set up the test framework:

1. Clone the project (use ssh if possible).


2. Go to the project directory.

   `cd python-api-pytest`


3. Run venv_setup.sh if you are mac or change the commands according to your os for setting up venv and downloading
   packages

   `sh venv_setup.sh`

**Framework Structure**

1. utils - It contains all the client's libraries like aws, k8, and Jenkins. For reference please have a look here.

   a. aws.py

   b. k8.py

   c. jenkins.py


2. docker - It contains the Dockerfile for creating the docker image of python in case if we need to run our test inside
   docker containers:

    1. /docker/


3. Jenkins-pipeline - It contains the Jenkinsfile which will be used to trigger our tests on Jenkins.

    1. Jenkinsfile


4. sample-jsons - It contains the environment data like baseUrl, database details.


5. tests - It contains the test class which needs to be triggered for execution.


6. allure-results - folder to save our allure report.


7. conftest - It is the heart of pytest, we will keep only fixture and pytest methods here. This file contains all the
   before and teardown fixtures and also database connections

    1. conftest.py


8. requirements.txt - we will write all our dependencies there and then download in one shot using venv_setup.sh

    1. requirements.txt

**Execution**

Running the pytest tests is very easy as it gets.

1. Complete the framework setup step


2. Activate the virtual environment source `venv/bin/activate` (run command inside python-api-pytest)


3. If you want to run the tests with default parameters passed in the source code, Just run `pytest tests` and the
   execution will start.


4. If you want to run the test with different params, you can pass the parameters as additional arguments in the command
   like `pytest tests --baseurl https://test.com`

**Reporting**

We are using Allure Report as a reporting tool for this framework. Once your test execution is completed you can
run `allure serve` and it will open the allure report on your default browser.

Allure report is a very fancy report and you can publish a lot of meaningful logs to it. It also shows the function
description there.


**Useful Doc’s**

pytest: https://docs.pytest.org/en/6.2.x/index.html

Allure: https://docs.qameta.io/allure/#_python

PEP 8 -- Style Guide for Python Code: https://www.python.org/dev/peps/pep-0008/

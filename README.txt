You can find Manuel Test Cases in TestCases.xlsx
You can find automations in Autamation folder.

For automation (https://automationexercise.com/test_cases 12)
required apps : chromedriver.exe (exists in repo) (https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip), chrome.exe
required python version >= 3.11.4 (https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe)
for required python packages, run command :
-cd Automation
-pip install -r requirements.txt
------------------------------------------------------------
!!!!!Please edit data.json for number of product or other related data!!!!!
------------------------------------------------------------
run command :
-cd Automation
-pytest seleniumAutomation.py --html=report.html 
test result report file will be : ./Automation/report.html
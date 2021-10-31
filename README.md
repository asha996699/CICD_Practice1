# CICD_Practice2

### Authors:
1. Ben Anderson
2. Jonah Beers

## Walkthrough:

**1) Make repo/fork/clone**

- Create a MoravianCollege GitHub repository and fork it to your own account. Then clone your forked repository onto your laptop in a new directory. 
	- `git clone <github clone link>`

**2) Setup virtual environment**

- Make sure that you are in your new directory where you cloned the repo
	- `python3 -m venv .venv`
- Activate virtual environment `source .venv/bin/activate`

**3) Setup project structure (pytest)**

- Create a new branch to add your code: 
	- `git checkout -b <branch_name>`
- Ensure that any written python code is placed in a folder called `src`. 
- Tests should be created and placed in the repository in a folder called `tests/`. This is important to separate our production code from test code and avoid `import` statement and path issues.
- Create an empty file in the `src` folder called `__init__.py`. This is to recognize and install our code as a package to address the import issues mentioned above.
- Install the pytest module 
	- `pip install pytest`
- Create a new file `setup.py` such as: 

```
from setuptools import setup, find_packages

setup(
    name="<your_subfolder_title_within_src>",
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
```

- Create `.gitignore` file
- Create `requirements.txt` file and add `pytest` to first line

**4) Write a test and function (make sure the test passes!)**

- Create a new .py file in `src/<new_folder>` and then write your function
	- `<text editor (such as atom/nano)> <filename>.py`
- Create a new .py file in `tests`
	- `<text editor (such as atom/nano)> <filename_test>.py`
- You must import the name of your method from the function file at the top of your test
	- `from <new_folder>.<filename> import <function>`
- Run your test using pytest to check if it passes or fails
	- `pytest`
- Add and commit each file:

```
git add <filename>
git commit -m “<insert commit message>”
```
- Push files to origin: `git push origin <branch_name>`
- Create a pull request to the upstream repository (in our case Moravian College)
- Get pull request merged into upstream

**5) Make a .travis.yml file w/ CI** 

- Create a new branch `git checkout -b <branch_name>
- Create a `.travis.yml` file. This will be used to tell Travis-CI to install the requirements found in `requirements.txt` and execute pytest.

```
dist: xenial
language: python
python: 3.7
install:
- pip install -r requirements.txt
- python setup.py install
script: pytest
```

**6) Setup Travis to run build**

- Go to [Travis CI’s] (https://travis-ci.com) website and login with your GitHub account.
- Navigate to install Travis CI to your MoravianCollege GitHub repository and click approve and install.

**7) Push to upstream**

- Add and commit the .travis.yml file

```
git add <filename>
git commit -m “<insert commit message>”
```
- Push your changes to upstream master 
	- `git push upstream master`
- Navigate back to Travis website and click on your GitHub repository. Travis should automatically launch a virtual machine and run a test build after you push to upstream.

**8) Add new test/code**

- Add another test to <filename_test> that will test a new functionality
	- `<text editor (such as atom/nano)> <filename_test>.py`
- Add more code to your source file in `src/<new_folder>` 
	- `<text editor (such as atom/nano)> <filename>.py`
- Run your test using pytest to check if it passes or fails
`pytest`

**9) Push to origin & P.R.**

- Push your local changes to your forked GitHub repository. `git push origin master`
- Create a pull request on GitHub to request a merge between origin and upstream

**10) Get Travis to run on P.R.**

- Ensure that within your pull request Travis CI appears above the merge button and runs a check on your tests and passes.

**11) Add Flask server to repo**

- If your local repository is not up to date with upstream, `git pull upstream master`
- Create a new branch for your following code `git checkout -b <branch_name>`
- Edit the `requirements.txt` file to include `flask` and `gunicorn`
- Create a basic flask server that returns something from a given endpoint

**12) Add test(s) to repo**

- Create a test client for your flask server to test the result of accessing the flask server endpoint. [Reference] (https://github.com/MoravianCollege/CICD_Practice2/blob/master/tests/test_app.py)

**13) P.R. - CI should pass**

- Create a pull request and see if Travis will run the build and pass all tests.
- Someone accepts the merge after Travis passes tests 

**14) Clone MC repo on AWS**

- `ssh` onto an Amazon Web Service instance and clone the upstream Moravian College repository onto the instance

```
ssh -i <.pem> ubuntu@<instance ip>
sudo apt update
sudo apt install python3-pip
git clone <MC repo URL>
sudo pip3 install -r requirements.txt
```

**15) Setup systemd launch**

- While still connected to the Amazon Web Service instance, set up a script to launch the flask server on boot. 
- Navigate to the systemd directory: `cd /etc/systemd/system/`
- Create a new file `<foo>.service` and enter the following: 

```
[Unit]
Description=Start CICDPractice on Boot
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/local/bin/gunicorn -b 0.0.0.0:80 --chdir /home/ubuntu/<your git repository directory folder containing server.py> <server file>:app

[Install]
WantedBy=multi-user.target
```
[Reference] (https://github.com/MoravianCollege/CICD_Practice2/blob/master/scripts/cicd.service)

**16) Setup CD process**

- Create an SSH key
	- `ssh-keygen -b 4096 -C 'build@travis-ci.com' -f ./deploy_rsa`
- Encrypt the new private key 
	- `travis encrypt-file deploy_rsa --pro --add`
- Make changes to the `.travis.yml` file: change `before_install` to `before_deploy`, change IP in `ssh_known_hosts` and `scripts`, and edit path in `script`
- `.travis.yml` should look similar after changes:

```
addons:
  ssh_known_hosts:
  - 3.16.42.52
before_deploy:
  - openssl aes-256-cbc -K $encrypted_f1cee75f37b0_key -iv $encrypted_f1cee75f37b0_iv -in deploy_rsa.enc -out deploy_rsa -d
  - chmod 600 deploy_rsa
deploy:
  provider: script
  skip_cleanup: true
  script: ssh -i deploy_rsa ubuntu@3.16.42.52 'source /home/ubuntu/ci-cd-repo/scripts/deploy.sh'
```
Reference: [Continuous Deployment Setup] (https://github.com/MoravianCollege/ci-cd-repo/blob/master/README.md)

**17) New feature (test, code, P.R., merge)**

- Create a new branch before making changes
	- `git checkout -b <branch_name>`
- Create a new test and add code to your flask server
- Add and commit each change, then push to origin 
	- `git push origin <branch_name>`
- Create a new pull request, give it a title and check if Travis passes tests. If everything is good to go, someone can accept the merge.

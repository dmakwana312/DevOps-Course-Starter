# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Trello Setup

In order to run the application, some setup is required to performed once in order to get the necessary Trello config setup.

Main thing to ensure is that you have a 'To Do' and 'Done' list on your board as the functionality of this app is dependent on that.

Steps are as follows:

1. [Create an account](https://trello.com/signup)
2. [Generate API key and token](https://trello.com/app-key)
3. Assign the values obtained to there corresponding variables in the .env file:
    - TRELLO_API_KEY
    - TRELLO_API_TOKEN
    - TRELLO_BOARD_ID

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running Tests

Tests can be run from the terminal by running `poetry run pytest`

If you want to skip running the end-to-end tests, you can do this by running `poetry run pytest tests`. Similarly, if you only want to run the end-to-end tests, you can do this by running `poetry run pytest tests_e2e`

You can also run tests individually within VSCode by following the instructions on [this page](https://code.visualstudio.com/docs/python/testing#_configure-tests)

## Provision VM via Ansible

***Following instructions should be run on control node only***

1. Create a file called 'vault.yaml'
2. Use the following as a template, but replace placeholders with actual values
```yaml
trello_api_key: <trello_api_key>
trello_api_token: <trello_api_token>
trello_board_id: <trello_board_id>
```
3. Create a file called vault-pass and add a line with what you would like the pasword for the vault to be
4. Execute the following to encrypt the vault.yaml file created during step 2
```bash
ansible-vault encrypt --vault-password-file vault-pass vault.yaml
```
5. Run the playbook with following command
```bash
ansible-playbook playbook.yaml -i inventory.ini --vault-password-file vault-pass
```
6. If you need to view the content of the vault, you can run the following to decrypt
```bash
ansible-vault decrypt --vault-password-file vault-pass vault.yaml
```
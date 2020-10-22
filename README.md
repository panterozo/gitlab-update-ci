
# Gitlab Update CI

The project's goals is to update every file `.gitlab-ci.yml` into the Gitlab instance of our company in three different ways

- Individual Project
- Projects in group
- Individul Projects from File

## How it works?

### Token

You should put your token for interact with gitlab inside de `python-gitlab.cfg` file, uder `private_token` key:


```
PRIVATE_TOKEN = put_your_token_here
```

### Branch Name

Also, you need to identify wich branch do you want to update, under `BRANCH_NAME` key:


```
BRANCH_NAME = you_awesome_branch
```

### Type update

Finally, you identify what kind of update do you want, "individual", "group" or "file":

```
TYPE_UPDATE = ìndividual
```

### Use cases for type update

If you choose individual, the script will read the `PROJECT_NUMBER` id

If you choose group, the script will read the `GROUPS_ID` array

If you choose file, the script will read the file defined in `FILE` key. By default, db.json.


## Running It

### Environments

I suggest you to use a virtual environment for python projects:

```sh
$ python3 -m venv virtual_env
```

And, activating...

```sh
$ source virtual_env/bin/activate
```
### Installation

Follow the instruction below to install dependencies through `pip`:

```sh
$ pip install -r requirements.txt 
```


### Execution

To launch the program, just type de code below:

```python
$ python start.py
```


## To-Do

- Use Lint validation for de yaml file to update
- Existance of variables inside config file
- Running with arguments

Example 

*Update project with id 77 and branch develop*

`$ python start.py -p 77 -branch develop`

*Update group 101 and 102, develop branch*

`$ python start.py -g [101,102] -branch develop`

*Update from file `my-file.json`*

`$ python start.py -f my-file.json -branch develop`





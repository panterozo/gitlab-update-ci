
# Gitlab-update-ci

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
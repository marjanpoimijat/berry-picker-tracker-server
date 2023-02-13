# Berry Picker Tracker back-end server


!\[my badge\](https://badgen.net/https/ohtup-staging.cs.helsinki.fi/bpt-stage/status)


## Installation

### Install script for frontend and backend in documentation
[Documentation for install script](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/README.md#installation)

### Requirements

- `python3`
- `pip3`

## Set-up

```bash
python3 -m venv .venv && \            # Create a virtual environment in `./.venv`
source ./.venv/bin/activate && \      # Activate the virtual environment
pip3 install -r requirements.txt && \ # Install dependencies — see `./requirements.txt` for more info
pre-commit install && \               # Install the pre-commit hook
pre-commit autoupdate && \            # Update the pre-commit hooks
touch .env                            # For environmental variables
```
### Database schema

Database schema can be found [HERE](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/bpt_schema.png).

If database is set up correctly, there's no need for any precautionary measures.  

**database's tables are created automatically upon running the program first time**.

### Environment variables
  
.env file should contain following variables:  

```
NLS_API_KEY=*API KEY*
```
API key for getting map tiles from National Land Survey of Finland. Instructions for acquiring one can be found [HERE](https://www.maanmittauslaitos.fi/rajapinnat/api-avaimen-ohje). The right API is found from [HERE](https://www.maanmittauslaitos.fi/karttakuvapalvelu/tekninen-kuvaus-wmts#avoin-rajapintayhteys) but it is already hard coded in the application.

```
DATABASE_URI=*local database address*
```
This is only needed if you're connecting to database locally. Instructions to connect to database locally are [HERE](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/db_locally_instructions.md).

As one can see from [DATABASE MODULE](https://github.com/marjanpoimijat/berry-picker-tracker-server/blob/main/src/utilities/db.py#L17), there is hard coded address for connecting to database which is run on virtual machine inside docker container (db password is acquired as a docker secret), but this is just original developer team's solution. For further development own solution should be implemented.

```
TEST_DATABASE_URI=sqlite:///test.db
```
For testing purposes SQLite is used instead of PostgreSQL. 

```
LEGEND_URI=*URI for downloading the map's legend*
```
Downloading the map legend is done through back end server in case the URI is modified or changed. The most recent (12.12.2022) working one is:

https://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/attachments/2020/01/karttamerkkien_selitys.pdf


### Updating dependencies

```bash
pip3 freeze > requirements.txt
```

### Running

Either start the "Run the app" task in VSCode or run

```bash
uvicorn --app-dir=src main:app --reload
```

### Testing


Even though SQLite is used for testing database purposes, the PostgreSQL database must be running as well.


Run tests

```bash
pytest
```

If you stumble upon `ModuleNotFoundError`, run

```bash
python3 -m pytest
```

## Licenses

[Licenses](https://github.com/marjanpoimijat/berry-picker-tracker-server/tree/main/licenses)

## General Information about the App
[App Documentation](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/README.md)

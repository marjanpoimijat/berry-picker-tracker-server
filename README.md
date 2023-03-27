<div align="center">
  <a href="https://github.com/marjanpoimijat">
    <img
        alt="Berry Picker Tracker logo"
        height=150
        src="https://raw.githubusercontent.com/marjanpoimijat/berry-picker-tracker-docs/main/docs/images/logo.png"
        title="Berry Picker Tracker logo"
        width=150
    />
  </a>
  <h1>
    <a href="https://github.com/marjanpoimijat">
      Berry Picker Tracker
    </a>
  </h1>
</div>

# Server

![Status](https://badgen.net/https/ohtup-staging.cs.helsinki.fi/bpt-stage/status)

## Installation

### Installation Script

There is a script for automating the installation process for both the frontend and the backend. You can find the [instructions](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/README.md#installation) in the official Berry Picker Tracker documentation.

## Manual Set-up

```bash
python3 -m venv .venv && \            # Create a virtual environment in `./.venv`
source ./.venv/bin/activate && \      # Activate the virtual environment
pip3 install -r requirements.txt && \ # Install dependencies — see `./requirements.txt` for more info
pre-commit install && \               # Install the pre-commit hook
pre-commit autoupdate && \            # Update the pre-commit hooks
touch .env                            # For environmental variables
```

### Development Using Docker

1. Install [Docker](https://docs.docker.com/get-docker)
2. add your API key to the enviroment section in the docker compose as NLS_API_KEY
3. use `docker compose up -d --build` to build and launch the containers
4. use `docker exec berry-picker-tracker-server-web-1 pytest ./tests/` to run tests
5. use `docker logs -f berry-picker-tracker-server-web-1`to view and follow backend logs
6. To connect to the backend server while using the emulator, set your URI in the frontend .env to http://10.0.2.2:8008

### Requirements

- `python3`
- `pip3`

### Database schema

Database schema can be found [here](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/docs/images/bpt_schema.png).

If the database is set up correctly, there's no need for any precautionary measures.

> **Note**
> The database tables are created automatically when running the program for the first time

### Environment variables

The `.env` file should contain following variables:

```bash
NLS_API_KEY=<API KEY>
```

API key for getting map tiles from National Land Survey of Finland. Instructions for acquiring one can be found [HERE](https://www.maanmittauslaitos.fi/rajapinnat/api-avaimen-ohje). The right API is found from [HERE](https://www.maanmittauslaitos.fi/karttakuvapalvelu/tekninen-kuvaus-wmts#avoin-rajapintayhteys) but it is already hard coded in the application.

```bash
DATABASE_URI=<local database address>
```
This is only needed if you're connecting to database locally. Instructions to connect to database locally are [HERE](https://github.com/marjanpoimijat/berry-picker-tracker-docs/blob/main/db_locally_instructions.md).

As one can see from [DATABASE MODULE](https://github.com/marjanpoimijat/berry-picker-tracker-server/blob/main/src/utilities/db.py#L17), there is hard coded address for connecting to database which is run on virtual machine inside docker container (db password is acquired as a docker secret), but this is just original developer team's solution. For further development own solution should be implemented.

```bash
TEST_DATABASE_URI=sqlite:///test.db
```
For testing purposes SQLite is used instead of PostgreSQL.

```bash
LEGEND_URI=<URI for downloading the map's legend>
```

Downloading the map legend is done through back end server in case the URI is modified or changed. The most recent (12 Dec 2022) working one is:

https://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/attachments/2020/01/karttamerkkien_selitys.pdf

### Updating Dependencies

```bash
$ pip3 freeze > requirements.txt
```

### Running

Either start the "Run the app" task in VSCode or run

```bash
$ uvicorn --app-dir=src main:app --reload
```

### Testing

Even though SQLite is used for testing database purposes, the PostgreSQL database must be running as well.

Run tests

```bash
$ pytest
```

If you stumble upon `ModuleNotFoundError`, run

```bash
$ python3 -m pytest
```

## Licenses

[Licenses](https://github.com/marjanpoimijat/berry-picker-tracker-server/tree/main/licenses)


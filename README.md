# dw-project

### This is an project for DW course at UFMG

#### Install python 3.9 and `pip install requirements.txt`

You can use the Makefile in this folder to get the csv data from online repository

Run:
- `pip install -r requirements.txt`
- `make # this will print the commands to run`

In folder `Metabase/` you can construct the container of Metabase with duck-db plugin using

`make dbuild`

and running the server locally with

`make drun`

The server will be acessible on http://localhost:3000

You need to configure metabase with duckdb conector, mount the duckdb file from host machine to container and specify the path inside container in the `Metabase/Makefile` under `drun` target.

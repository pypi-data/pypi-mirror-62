# Sermos Utils

Utilities for interacting with Sermos.

## Deployments

### Prerequisites

To deploy your application to Sermos, there are a few prerequisites:

1. Deployment environment created and configured
1. A `deploy key` has been issued for that deployment
1. Your app is a valid Python package with a standard structure (see below)
1. You have a `sermos.yaml` file written with your defined API endpoints, workers, etc.
1. Your application has `sermos-utils` as a dependency and it's installed.

### Deployment

You can initiate a Sermos deployment in two ways: programmatically or using the
CLI tool.

It is recommended to keep your deployment key in the environment and to set the
client package directory in the environment as well, for convenience.

    SERMOS_DEPLOY_KEY=abc123
    SERMOS_CLIENT_PKG_NAME=your_package

#### Programmatic Deployment

Invoking a pipeline programmatically (e.g. as part of a build pipeline) can
be done similar to below (assumes deployment key/client package direcotry
are available in the environment per note above).

    from sermos_utils.deploy import SermosDeploy

    sd = SermosDeploy()
    status = sd.invoke_deployment()
    print(status)

#### CLI Deployment

For a cli-based deployment, there is a `sermos_deploy` command installed
as part of the sermos-utils package.

    honcho run -e .env sermos_deploy

### Deployment Status

Assuming your environment is set up per notes in the `Deployment` section above:

#### Programmatic Status Checks

    from sermos_utils.deploy import SermosDeploy

    sd = SermosDeploy()
    status = sd.get_deployment_status()
    print(status)

#### CLI Status Checks

    honcho run -e .env sermos_status

### Proper Python Package Structure

Assuming your package is called "my_sermos_client":

    setup.py
    my_sermos_client/__init__.py
    my_sermos_client/sermos.yaml

`my_sermos_client/__init__.py` has only one requirement, to contain your
application's version assigned as a variable `__version__`, e.g.:

    __version__ = '0.1.0'

Common practice is to use that value in your `setup.py` file, e.g.

    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open('my_sermos_client/__init__.py', 'rb') as f:
        __version__ = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))

## Local Development

Sermos provides a local development environment in two ways:

1. Local 'sandbox' environment
1. Cloud-connected environment that proxies into your deployment's databases

### Local Development Prerequisites

To develop locally, you must have the following:

1. Functional [Docker](https://docs.docker.com/install/) environment along with [docker-compose](https://docs.docker.com/compose/)
1. A [Docker Hub](https://hub.docker.com/) account that has been given access
to the `Sermos` base image.

### Prepare Client Repository

The local development environment is accomplished by mimicing your Sermos
cloud services through injecting your local client code into the Sermos engine.
To prepare your environment is relatively quick:

1. Copy all files from `sermos-utils/dev/*` to your client's codebase. It is
recommended to keep with the convention of `client-pkg/dev/*` but you can
place anywhere (fyi, some minor modifications will be required if you do change
convention).
1. Create a valid `.env` file with your application's secrets.
  * Rename `example.env` to `.env` (important to have this name)
  * Add in your specific secret values.
  * __NOTE__: It is recommended you do *not* track this `.env` file in your
  git repository. Add `.env*` to your `.gitignore` file.
1. Any new environment variables you include in your `.env` file will need to
be added explicitly in the respective `docker-compose-*.yaml` files in order
for them to be available in your local environment.

### Prepare Local Image

To speed local development, you can build your own version of your Sermos
application for *local development purposes*. This is recommended but not
required. If you do *not* want to do this, then you can update the `image:`
in the provided `docker-compose-*.yaml` files:
  * `sermos-local:latest` changes to -> `rhoai/sermos:latest`

If you do want to proceed with the recommended local image strategy:

1. Modify provided `build-image.sh` script as necessary.
1. Modify provided `Dockerfile.tmpl` file as necessary.
1. `cd dev` then run `./build-image.sh`

To use the provided files without modification, your client package needs to
follow a convention for specifying package requirements using a file that is
then imported into your setup.py file. This allows easy access for the build
script. `sermos-utils` follows this convention, so you can see how it is
accomplished by reviewing the `setup.py` and `requirements.txt` files.

Using WSL, line endings need to be dealt with appropriately, requiring `sudo apt
 install dos2unix` and `dos2unix ./build-image.sd` before bullet 3 above.

### Starting Services

#### First Start & Any Mandatory DB Upgrades

Sermos has a small set of required database models for your relational database.
When running in `sandbox` mode, you need to ensure your database has the
most up-to-date models:

1. Navigate to the `dev` directory, e.g. `cd dev`
1. Start databases with
  * `docker-compose -f ./docker-compose-dbs.yaml up -d`
  * Note: Some deployments utilize an external/public elasticsearch service,
  in which case you can modify the docker-compose file to omit elasticsearch
  and kibana assuming you have the connection information in your `.env` file.
1. Build initial db models.
  * `docker-compose -f ./docker-compose-migrate.yaml up`
  * Note: this is only required for your initial sandbox setup or if Sermos
  informs you of required migration. It is OK to run this at every start, but
  is not required.

#### Normal Operation

After your databases are started and relational models have been created with
the migrate script, you generally interact with only 2 files that control
your admin console + API endpoints, and the other that controls your workers.

You can modify these files in any way you like to suite your development style.
For example, the `docker-compose-workers.yaml` file may be better split into
multiple files with a subset of workers.

1. Navigate to the `dev` directory, e.g. `cd dev`
1. Start Admin console and API endpoints/documentation
  * `docker-compose -f ./docker-compose-app.yaml up`
1. Start workers
  * `docker-compose -f ./docker-compose-workers.yaml up`
  * Note: Modify this file to suit your exact needs. Every deployment has
  different workers, so the provided docker-compose file is intended as a
  reference.

## Testing

To run the tests you need to have `pyenv` running on your system and `tox` in
your environment.

Refer to RhoAI documentation for instructions on installing `pyenv` correctly.

After `pyenv` is intalled, then install `tox`

    $ pip install tox

Then install the different python versions in `pyenv`

    $ pyenv install 3.7.4

Now, run the tests:

    $ tox

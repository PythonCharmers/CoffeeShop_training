# Python Charmers Coffee Reviews

This is the Python Charmers Coffee Shop application.

## Getting Started

Create and activate a virtual environment, and then install the requirements:

    pip install -r requirements.txt
    pip install -r dev_requirements.txt

Copy sample environment file from the `environment_config` folder into a file
`.env` in the base folder:

    cp environment_config/sample.env .env

### Setting up environment variables

The following environment variables should be updated in the `.env` files:

| Variable | Description |
|-|-|
| `SECRET_KEY` | The application secret key. You could use `python3 -c "import os; print(os.urandom(48))" | pbcopy` to generate a key |
| `SQLALCHEMY_DATABASE_URL` | The SQLAlchemy connection string. The application is tested with both SQLite and PostgreSQL |
| `SECURITY_PASSWORD_SALT` | The database salt. Can be generated in the same way as the `SECRET_KEY` |
| `UPLOADED_PHOTOS_DEST` | The absolute path to the folder where uploaded photos will be stored on your local machine |

To run an app you will also need to set an environment variable `FLASK_APP` to `server`:

    export FLASK_APP=server

### Create DB

You can use Alembic to set up the database:

    flask db upgrade
    
### AWS

Ultimately this application is intended to be deployed on AWS. As such there's
a dependency on the `boto3` library. The application will work locally
provided you have `boto3` installed, but for uploading files to S3 and
deployment to AWS Lambda you will need the AWS CLI installed and configured.

Installing the AWS CLI is easy (if you wish there is [complete documentation
available as well](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)):

1. Outside your Virtual Environment (to install globally on your system) run:
   ```sh
   pip3 install awscli
   ```
2. Copy your AWS Access Key ID and your AWS Secret Access Key from your IAM
   role in the AWS managment console
3. From the command line run:
   ```sh
   aws configure
   ```
   to complete the configuration process
4. Test the configuration by running:
   ```sh
   aws s3 ls
   ```
   to list all of your S3 buckets along with their unique identifiers

## Runing the application locally

You can run the server locally using the standard flask comands.

    flask run


## Extended exercises

There will be an extended exercises per day based on the coffee shop
application.

The solutions will be separated into individual branches (in the form 
`day_n_exercise`), and there is a `combined_solutions` branch where all
extended exercises are merged together.

### Day 2 Extended exercise: Templating

The front page of the coffee shop application is very bare at the moment. We
can do better:

1. Update the / endpoint to display the 10 most recently added shops.

   Since we haven't covered SQLAlchemy yet, use the following to generate
   shops to pass through to the template:

   ```python
   from coffeeshop.server.shop.models import Shop
   shops = Shop.query.order_by(Shop.date_added.desc()).limit(10)
   ```

2. Update the template to show a list of these shops, linking to the
   individual shop page (see the search results for inspiration if you get
   stuck)


### Day 3 Extended exercise: API Access

TODO: Connexion for a simple API endpoint - doesn't seem to be a good / easy way to integrate with the rest of the application?

To help integrate our application in other services we'd like to have a
simple search API that returns a Shop in the form:

```json
{
  "id": "int",

}
```


### Day 4 Extended exercise: Cleaning up your code

Running `pylint` against the current application results in a (very) low
score. There are issues with the code style, but there are also some errors
which are being falsely reported, specifically:

- E1101 (instance of object doesn't have member)
- R0401 (circular imports)

Generate a .pylintrc file for your project with:

```sh
pylint --generate-rcfile > .pylintrc
```

In the `.pylintrc` file add those two errors to the disabled messages list.

Re-run `pylint` and update the files so that the score is at least 8 out of 10.


### Day 5 extended exercise: Preparation for deployment

#### Prepping your application for deployment

To deploy to AWS Lambda you'll need:

1. To have the AWS CLI installed and configured
2. To install Zappa (if you're using Python 3.7 use `pip install
   git+https://github.com/itamt/Zappa.git`)
3. You will need a database setup on RDS where the application data will be
   stored - the connection string for an accessible PostGreSQL database will be
   provided via a download link by the trainers.
4. You'll need to create a new bucket on S3 to store photos. It should not block
   public ACLs from uploading. It will be used to store uploaded photos.
5. You'll need to update the following environment variables in your `.env`
   file (**note:** it's a good idea to backup your development `.env` file first - 
   possibly with `cp .env environment_config/dev.env`):
   - `SECRET_KEY` should be generated for production as per the instructions
     above
   - `SECURITY_PASSWORD_SALT` likewise the password salt should be updated
   - `SQLALCHEMY_DATABASE_URI` the connection string for your RDS database
   - `FLASK_ENV` should now be set to `production`
   - `WTF_CSRF_ENABLED` should be `True`
6. Run the Alembic upgrade to add your database tables on the server

#### Photos in S3

Your goal is to upload photos to a S3 bucket. As such you'll need to update your 
S3 settings accordingly (in your `.env` file):

| Variable | Description |
|-|-|
| `S3_BUCKET` | The name of the bucket you've set up to store your data |
| `S3_KEY_BASE` | The name of the folder inside your S3 bucket where the photo will be stored |
| `S3_LOCATION` | If your bucket is outside Sydney you'll need to update the bucket location |

Finally, to ensure the upload works, set the environment variable that will
control your app:

On Windows:

```sh
set APP_SETTINGS="coffeeshop.server.config.ProductionConfig"
```

On Unix or OS X:

```sh
export APP_SETTINGS="coffeeshop.server.config.ProductionConfig"
```

Then run the app as normal. Test that when you create a new shop and add a photo
that instead of being stored locally, the file is uploaded to your S3 bucket.

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

## Runing the application locally

You can run the server locally using the standard flask comands.

    flask run

## Workflow during challenge competitions

Before each exercise, the participants run:

```
git pull origin/day_2/quiz_1
```


## Longer (challenge) exercises

There will be around two longer exercises per day based on the coffee shop application.

The solutions will be separated into individual branches as noted below (in
the form `day_n/quiz_x`), and there is a `combined_solutions` branch where
all quizzes are merged together.


### Day 2 Extended exercise: Templating

The front page of the coffee shop application is very bare at the moment. We
can do better:

1. Update the / endpoint to display the 10 most recently added shops.

   Since we haven't covered SQLAlchemy yet, use the following to generate
   shops to pass through to the template:

   ```python
   from .models import Shop
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
  "id": int,

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


## Deployment

### Deploying to AWS Lambda with Zappa

To deploy to AWS Lambda you'll need:

1. To have the AWS CLI installed and configured
2. To install Zappa (if you're using Python 3.7 use `pip install
   git+https://github.com/itamt/Zappa.git`)
3. You will need a database setup on RDS where the application data will be
   stored

From this point you can configure your Zappa application:

1. Use `zappa init` to generate your `zappa_settings.json`
2. Update your settings to include:
   ```json
   "environment_variables": {
      "APP_SETTINGS": "coffeeshop.server.config.ProductionConfig"
   }
   ```
3. Update your `.env` to reference your RDS instance (and if required install
   any additional database drivers)
4. Use `zappa deploy` to deploy your application

Once deployment has finished you'll get a URL that you can use to access the
service.


### Day 5 Extended exercise 1: Photos in S3

Finally, you'll need to create a new bucket on S3 to store photos. It should
not block public ACLs from uploading. It will be used to store uploaded
photos.

### Production environment variables

If you're deploying on AWS Lambda you won't have local file storage available.
Instead you should be looking to store static files on a dedicated server, for
example S3. The production settings for the server assume this is the case, and
you will need to set your S3 settings accordingly:

| Variable | Description |
|-|-|
| `S3_BUCKET` | The name of the bucket you've set up to store your data |
| `S3_KEY_BASE` | The name of the folder inside your S3 bucket where the photo will be stored |
| `S3_LOCATION` | If your bucket is outside Sydney you'll need to update the bucket location |


### Day 5 Extended exercise 2: Prep your application for production

Create a new production database in RDS. Back up your development `.env` file.
Then update your `.env` file to reflect a production environment. You should
update the following environment variables:

- `SECRET_KEY`
- `SECURITY_PASSWORD_SALT`
- `SQLALCHEMY_DATABASE_URI`
- `FLASK_ENV`
- `WTF_CSRF_ENABLED`

Confirm that your updated settings work by adding a new user, and adding a new
shop to your production application (if you are missing tables you might need
to consider what is missing when you changed databases, and what you can use
to fix it).

Create an S3 bucket

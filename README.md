# Python Charmers Coffee Reviews

This is the Python Charmers Coffee Shop application.

## Getting Started

Create and activate a virtual environment, and then install the requirements:

    pip install -r requirements.txt
    pip install -r dev_requirements.txt
    
Copy sample environment file from the `environment_config` folder into a file
`.env` in the base folder:

    cp environment_config/sample.env .env
    
Finally, you'll need to create a new bucket on S3 to store photos. It should 
not block public ACLs from uploading. It will be used to store uploaded 
photos.
    
### Setting up environment variables

The following environment variables should be updated in the `.env` files:

| Variable | Description |
|-|-|
| `SECRET_KEY` | The application secret key. You could use `python3 -c "import os; print(os.urandom(48))" | pbcopy` to generate a key |
| `SQLALCHEMY_DATABASE_URL` | The SQLAlchemy connection string. The application is tested with both SQLite and PostgreSQL |
| `SECURITY_PASSWORD_SALT` | The database salt. Can be generated in the same way as the `SECRET_KEY` |
| `S3_BUCKET` | The name of the bucket you've set up to store your data |
| `S3_LOCATION` | If your bucket is outside Sydney you'll need to update the bucket location |

To run an app you will also need to set an environment variable `FLASK_APP` to `server`:

    export FLASK_APP=server

### Create DB

You can use Alembic to set up the database:

    flask db upgrade

## Runing the application locally

You can run the server locally using the standard flask comands.

    flask run

## Deploying to AWS Lambda with Zappa

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

## Quizzes

There will be two quizzes per day based on the application for the coffee shop
application.

Quizz solutions will be separated into individual branches as noted below (in
the form `day_n/quiz_x`), and there is a `combined_solutions` branch where
all quizzes are merged together.

### Day 2 Quiz 1: Templating

The front page of the coffee shop application is very bare at the moment. We
can do better:

1. Move the `/` endpoint from the main blueprint to the shop blueprint.
   Likewise move the template.
2. Update the endpoint to pass through the 10 most recently added shops. Since
   we haven't covered SQLAlchemy yet, use the following to generate shops to
   pass through to the template:
   ```python
   from .models import Shop
   shops = Shop.query.order_by(Shop.date_added.desc()).limit(10)
   ```
3. Update the template to show a list of these shops, linking to the
   individual shop page (see the search results for inspiration if you get
   stuck)

### Day 2 Quiz 2: Debugging

What is the current value of the `PERMANENT_SESSION_LIFETIME` configuration
variable? Hint: It's not in the `.env` so what tool can you use to find out?
Note when you do which other environment variables are also easily
accessible.

Try running an arbitrary command on your computer through the web browser.

**Warning!** This is why we must never use `FLASK_ENV=development` for a publicly visible site!!

### Day 3 Quiz 1: Database migrations

To help avoid spam and fake reviews in our application we want to record the
user's location when they write a review.

1. Add new latitude and longitude fields to the `Review` model
2. Create a new migration using `flask db migrate` and then upgrade the
   database
3. Update the form to include the hidden latitude and longitude fields,
   and update the template so the `getLocation()` function is also called
   `onload`.
4. Update the view to get the latitude and longitude data from the form and
   pass it through to create the Review object
5. Test adding a review which should now include the location.

### Day 3 Quiz 2: API Access

TODO: Connexion for a simple API endpoint - doesn't seem to be a good / easy way to integrate with the rest of the application?

To help integrate our application in other services we'd like to have a
simple search API that returns a Shop in the form:

```json
{
  "id": int,
  
}
```

### Day 4 Quiz 1: Cleaning up your code

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

### Day 4 Quiz 2: TODO?

### Day 5 Quiz 1: Prep your application for production

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

### Day 5 Quiz 2: Deploying your application to AWS Lambda

The final step in the process of building a web application is deploying it
for the world to use and see. Install Zappa and run the initialisation
process. Once you've put the settings together for a dev environment deploy
the application to AWS lambda and test that it works as a serverless
application. You should be able to access the application with the same
users you created when testing the application locally in the previous 
exercise. 

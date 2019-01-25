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

Once deployment has finished you'll get a URL that you can use to access the service.

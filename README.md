# mturk_template
 Django template for mturk external questions.


This repository is a template for mturk external questions that saves the participant data into Postgresql database and AWS S3 Bucket.
Here are the instructions for running this Django application in Heroku server and connecting it to mturk:

<b>1-</b> Set up an Heroku application: Create a new app through Heroku website. Open your app and go to settings. Through there, add heroku/python as a buildpack.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>1.1-</b> To use Heroku's default postgres database (easy to configure), go to resources and add Heroku Postgres add-on.

<b>2-</b> Clone/Fork this repository and make sure you push it to GitHub after you have made the changes you need. We will use that repository to host it on Heroku.

<b>3-</b> Create an S3 bucket through AWS (keep default settings). You will use this bucket to store the data files, in addition to the Postgresql server. In order to reach to this bucket, create an IAM user. Through permissions, give the user full access to S3.

<b>4-</b> Go back into your Heroku app through heroku dashboard and go into settings. Through there you need to setup config vars. All required variables are given below:

    DATABASE_URL: Your postgresql database URL. It should be there already, if you have completed step 1.1.
    
    AWS_REGION: Region of your S3 bucket (i.e. us-east-1).
    
    HEROKU_URL: URL of your heroku app (i.e. https://mturk-template.herokuapp.com/).
    
    AWS_ID: Access key ID of your IAM user.
    
    AWS_SECRET_KEY: Secret access key of your IAM user.
    
    BUCKET_NAME: Name of your S3 bucket.
    
    SECRET_KEY: Secret key for Django. You can generate one here: https://djecrety.ir/
    
    HEROKU_HEADER: i.e. mturk-template.herokuapp.com 

<b>5-</b> Link your GitHub account with your Heroku app and deploy the server.

<b>6-</b> Through Heroku CLI, run: \
`heroku run python manage.py makemigrations`\
`heroku run python manage.py migrate`\
in order to setup the database for our participant model.

<b>7-</b> Once your server is started, you can create/delete the mturk task by running mturk.py file. Make changes according to your needs.

<b>8-</b> Do not forget to set debug to False in settings.py in production and change DEV_ENVIRONMENT_BOOLEAN to False, to run on real mturk instead of the sandbox.

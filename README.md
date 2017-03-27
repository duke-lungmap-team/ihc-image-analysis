# ihc-image-analysis
A (django) web application for analyzing immunohistochemistry images.


## Standing up the project
As a django project, there are many steps that are taken by interacting with
the `manage.py` file. This section aims to help explain steps with `manage.py` to
help with the reproducibility of the production environment.

```
git clone <this repo>
cd ./<this repo>
pip install -r requirements.txt
```

Next, we need to get the inital metadata from the
lungmap website. To do this, we've created the application (python package) 
`lungmap_sparql_client`. In order to facilitate using this resource, we've also
created a small python script that demonstrates how to use. Included in this repository are
possible `django model choices` in the module repository.models_choices. This file is generated
from the lungmap website via `python generate_repositoryExecute the following
command to generate all `fixtures` for our relational database:

```
python generate_analytics_models_choices.py
python generate_analytics_fixtures.py
```

Now, if you navigate to `repository/fixtures` you'll see several json
files that contain metadata for the image files (.tif or .tiff only). We need
to use these files along with the `repository/models` definined to initialize
our database.

Up to this point, we've downloaded the source code and installed the required
python packages. Let's now initialize our database (**note this requires sqlite to be 
installed on the host machine**).

```
python manage.py makemigrations analytics
python manage.py migrate
```

Now, let's create the migration script for our specific data model. To
do this, we need the following command(s):

```
python manage.py loaddata experiment.json probe.json
```

## Managing the project
At this point, we've loaded our database, now we'd like to add some administrative abilities so that we can view the data from an admin panel.

```
python manage.py createsuperuser
```

## Utilizing Docker
Of course, we could "dockerize" our application. We will begin to do this with
the `Dockerfile` within this repo. To take advantage of the dockerized solution follow
these commands:

```
docker build -t ihc-image-analysis .
```

In progres...


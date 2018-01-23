# ihc-image-analysis
A (django) web application for analyzing immunohistochemistry images. As this 
project progresses, we will try to use continuous integration to deploy to a 
[demo](http://rapid-609.vm.duke.edu:8000) application. However, in the 
early stages of this project, this may or may not be operational.


### Standing up the project
As a django project, there are many steps that are taken by interacting with
the `manage.py` file. This section aims to help explain steps with `manage.py` 
to help with the reproducibility of the production environment.

```
git clone <this repo>
cd ./<this repo>
pip install -r requirements.txt
```

### Modify ihc-image-analysis/lap/settings.py
You will need to have a database for setup. Enter this information
in the usual `django` settings file. We've placed an example, `settings_example.py`.

Up to this point, we've downloaded the source code and installed the required
python packages. Let's now initialize our database (**note this requires sqlite 
to be installed on the host machine**).

```
python manage.py makemigrations analytics
python manage.py migrate
```

### Managing the project
Now we'll want to populate our database with data useful for the application. To 
do this:

```
python manage.py loaddata analytics/fixtures/*.json
python preload_analytics_models.py
```
At this point, we've loaded our database, now we'd like to add a user and fire up a test server.

```
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```
You should now be able to see the application here: 
[0.0.0.0:8000](0.0.0.0:8000)


### Docker
```
docker build -t lap .

docker run -it \
-p 8000:8000 \
-v $(pwd):/ihc-image-analysis \
lap bash 

docker run -d \
-p 8000:8000 \
-v $(pwd):/ihc-image-analysis \
--restart always \
lap
```
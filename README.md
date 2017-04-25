# ihc-image-analysis
A (django) web application for analyzing immunohistochemistry images. As this 
project progresses, we will try to use continuous integration to deploy to a 
[demo](http://rapid-235.vm.duke.edu:8000/docs) application. However, in the 
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

Up to this point, we've downloaded the source code and installed the required
python packages. Let's now initialize our database (**note this requires sqlite 
to be installed on the host machine**).

```
python manage.py makemigrations analytics
python manage.py migrate
```

### Managing the project
At this point, we've loaded our database, now we'd like to add some administrative abilities so that we can view the data from an admin panel.

```
python manage.py createsuperuser
python manage.py runserver
```

# Utilizing Docker
Of course, we could "dockerize" our application. We will begin to do this with
the `Dockerfile` within this repo. To take advantage of the dockerized solution follow
these commands:

```
docker build -t lap .  
  


#Background
docker run -d \
-p 8000:8000 \
-v $(pwd):/ihc-image-analysis \
--restart always \
lap python /ihc-image-analysis/manage.py runserver 0.0.0.0:8000
  
#Interactive
docker run -it \
-p 8000:8000 \
-v $(pwd):/ihc-image-analysis \
lap bash
```


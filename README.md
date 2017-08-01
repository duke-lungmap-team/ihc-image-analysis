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
lap
  
#Interactive
docker run -it \
-p 8000:8000 \
-v $(pwd):/ihc-image-analysis \
lap bash  
```

## SPARQL Server
As part of this project, we are building our own ontology. For research purposes, it is of interest
to host a SPARQL server (ontop of our DJANGO RESTful interface) to demonstrate the refactor of the ontology.
To do this, the Python SParql queries are not performant, so we will turn to a 3rd party applicaiton to server
our triples. We will use [Apache Jena-fuseki](https://jena.apache.org/documentation/fuseki2/index.html). We will
use a dockerized version from [stain/jena-docker](https://github.com/stain/jena-docker/tree/master/jena-fuseki).

To deploy we use:
```
docker run -d \
-p 3030:3030 \
-e ADMIN_PASSWORD=xxxxx \
--restart always \
stain/jena-fuseki
```

We then load our `.owl` file. This is a way more performant way to make our SPARQL queries.
You can demo this resource [here](http://rapid-609.vm.duke.edu:3030).




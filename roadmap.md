## Project setup
  - Determine technology stack
    - includes Python version, DB, and web server
  - Identify software library dependencies
    - includes web frameworks, analysis packages,
  - Identify coding styles and project license

## Begin ontology development
  - Can be done in parallel with the next stage
  -

## Query lung map (LM) site to retrieve, store, and display images
  - Write functions to communicate w/LM SPARQL interface (put LM functions in their own module)
  - Data modelling for image and metadata storage
    - Need both TIFF (analysis) and JPEG (display) images
    - How to cache or sync images from LM?
      - Do not store in git repo
      - Who gets to retrieve new images? shouldn't be done by any user on the fly...too many hits to LM
      - Data model for users and permissions
    - UI and API for retrieving new images
    - UI and API for displaying currently retrieved images
      - User should be able to filter by probe combos, development stage, magnification (and in the future on structures)
    - Organize retrieved LM images into image sets using metadata

## Create training set of sub-regions for a set of images
  - An image set has the same combination of probes, species, dev. stage, and magnification
  - Training sets can only be created by a user w/ that permission
  - UI and API for creating and editing training sets
    - Do we limit to structures for now, i.e. no cells? We may be able to generate these automatically later.
  - How to prevent duplicates?
    - Possible rabbit hole...don't code logic preventing duplicates, just make sure the privileged user has all the information to approve or edit regions...display all of them while creating new ones
    - What about concurrent users? Lock an image while a user is creating sub-regions for training set?...this gets a bit hairy to implement though.
  - Incorporate ontology to limit what the user can use for structure labels

## Create a fitted model from a set of training images
  - Action must be restricted to privileged user
  - Warn user of computational time of doing this
  - If training set is modified, delete fitted model
  - Data model for storing fitted model & associated sub-regions
  - Feature metrics must be defined. If they change, all fitted models must be deleted and re-created
  - Requires entire analysis pipeline to be established

## Use fitted model to classify user selected regions
  - UI and API for drawing regions, sending to server back-end, and getting back the results
  - What to do with the results?
    - If we save them, then we need a data model to store them
    - If we want to add them to the training set, how to avoid the duplicate problem? And, this means re-creating the fitted model every time.

## Implement automatic classification pipeline for entire image
  - We should know at this point what to do with results from the single region stage above, but we will now have many more regions.
  - The pipeline still has a lot of overlapping regions using the hue & saturation candidates.
  - Filtering classified regions is still less than optimal.

## Tying it all together
  - Note, the candidate selection is independent of of the classification pipeline. So, once we are at this point we could drive the whole process of the candidate creation
    - Could we combine the metadata with the ontology and use some clustering technique on the candidates' feature metrics to group and label them in bulk?

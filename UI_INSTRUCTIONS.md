# User Interface Instructions

Welcome to `ihc-image-analysis`, an application that exposes, curates, and brings computer vision to Lungmap data. 
The following instructions provide additional details to the use of our applicatoin. Specifically,

1.  [Choosing an Image Set](#choosing-an-imageset)
- [Side Panel](#side-panel)
- [Image Set Selection](#image-set-selection)
2.  [Navigating within an Image Set](#navigating-an-imageset)
- [Generating Training Data](#generating-training-data)
- [Classifying Anatomy](#classifying-anatomy)
- [RESTful Application Programming Interface](#restful)

## Choosing an Image Set <a id="choosing-an-imageset"></a>
`ImageSets` are a collection of LungMap images grouped together according to the following four variables:  
- Species
- Magnification
- Development Stage
- Probe

These groups of images make up a critical component of the `ihc-image-analysis` application because our solution to 
automatically annotate a given image segmentation relies on strata defined models made up of these four variables.
Our first page provides functionality to narrow focus to imagesets by allowing users to subset based on these four 
variables.

### Side Panel <a id="side-panel"></a>
The `side panel` allows users to subset `ImageSets`. Here is a quick overview of the side panel:
![mail](ui-instructions/sidepanel.png)

To utilize the side panel to narrow the scope of available `ImageSets`, it is important to remeber that all chosen 
options are chained together with an `OR` statement within a given variable and `AND` between different variables. So for example, if I were to click `Apply` with the boxes checked 
above, the system would interpret this request as:
> Give me all imagesets with (species='mus musculus`) **AND** (sidepanel='100X' *OR* sidepanel='40X') **AND** (probe='Acetylated Tubulin' *OR* probe='Muc5AC' *OR* probe='Lyve-1')
 
### Image Set Selection <a id="image-set-selection"></a>
Once the results have been narrowed sufficiently, a user will want to choose a given image set. Use the `Apply` button to filter
the results. Once filtered, results are displayed to the right of the side panel:

![mail](ui-instructions/imagesets_results.png)

To actually filter the results, click the `View` button and a new user interface will be given.

## Navigating within an Image Set <a id="navigating-an-imageset"></a>

### Generating Training Data <a id="generating-training-data"></a>
Training data can be defined as the segmentation of anatomy within a given Imageset/Image. An example of this can be
see here:


### Classifying Anatomy <a id="classifying-anatomy"></a>


### RESTful Application Programming Interface <a id="restful"></a>
# Deployer 

## This tool deploys your ML models using flask. 
## Just setup the config fields and you are good to go.

* Currently only supports Keras models(h5 files) for image classification.

## Usage:

Download the repo and setup the config files,

* config.json
* labels.txt

### config.json

`model_path` : the path to the model file(h5 file). Just copy your h5 file in `models` directory and add the path here.

`img_rows` : Height of the image input for the model.

`img_cols` : Width of the image input for the model.

`img_channels` : 1 for grayscale, 3 for RGB image input for the model.

`nclasses` : Total number of model classes.


### labels.txt

Put the label names in each line in order.

### Run

After setting up the config files, run the flask server using:
`python prediction.py`

Now, the HTTP POST request can be made to `http://127.0.0.1:5000/predict`. Use the following for sending a POST request using curl.

`curl -F 'file=@/path/to/image' 'http://127.0.0.1:5000/predict'`

Or you can navigate to `http://127.0.0.1:5000/index` to utilize GUI and upload image.
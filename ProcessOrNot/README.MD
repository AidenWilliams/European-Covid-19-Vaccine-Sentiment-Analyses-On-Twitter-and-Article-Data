# To Process or Not

In this folder I use a subset of the dataset used in the complete project to see whether I should process the dataset.
This also the first fully complete iteration of the project which includes data collection, filtering, analyses and visualization.

# Guide
Included in this folder are 4 ipynb files, 1 py file and 2 sub folders.

# Twitter.py
In this file includes the Tweets class and a demo for the class.

# Collect Tweet ID.ipynb
In this file I go over filterring the dataset and collecting only what I want.

# Translate,ipynb
In this file I developed the translate function used in the Twitter.py file.

# Get Tweets.ipynb
In this file I use the Tweets class to get, pre-process (or not) and translate the tweets from the filtered dataset.

# Analyse Tweets.ipynb
In this file I use the VADER sentiment analyzer and visualise the results so that I can decide on the matter of pre processing
for the full project.

# Data Folder
This is the folder that contains the dataset used in each stage.

### pancealab
The files stored here were taken from the pancealab [github repo](https://github.com/thepanacealab/covid19_twitter).

### FilteredTwitterIDs
The files stored here are filtered versions of the pancealab files. These files are generated in the Collect Tweet ID.ipynb notebook.

### Text
The two sub folders here **NotProcessed** and **Processed** contain their share of the Tweet json files. These files are
generated in the Get Tweets.ipynb notebook.

# Output
Visualizations are saved in this folder.
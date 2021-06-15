# European Covid-19 Vaccine Sentiment Analyses On Twitter and Article Data

In this project I use the Sentiment Analyses VADER model on 2 datasets, one consisting of Tweets and another of article headings
to analyze patterns related to the COVID-19 pandemic.

# Guide
Included in this folder are 4 ipynb files, 1 py file and 3 sub folders.

# Twitter.py
In this file includes the Tweets class and a demo for the class.

# Collect Tweet ID.ipynb
In this file I go over filtering the dataset and collecting only what I want.

# Get Tweets.ipynb
In this file I use the Tweets class to get, pre-process (or not) and translate the tweets from the filtered dataset.

# VADER Sentiment Analyses.ipynb
In this file I use the VADER sentiment analyzer on the 2 datasets.

# Visual Analyses.ipynb
I use the multiplex library to plot several time series graphs.

# Wordcloud.ipynb
I use the wordcloud and matplotlib libraries to plot several word clouds.

# Data Folder
This is the folder that contains the dataset used in each stage.

### Analyzed Articles
The article dataset with the compound sentiment score.

### Analyzed Tweets
The twitter dataset with the compound sentiment score .

### Articles
Article dataset in 6 separate country csv files or 1 complete csv file.

### FilteredTwitterIDs
The files stored here are filtered versions of the pancealab files. These files are generated in the Collect Tweet ID.ipynb notebook.

### Flags
6 flags used as masks for the word clouds, taken from wikipedia.

### pancealab
The files stored here were taken from the pancealab [github repo](https://github.com/thepanacealab/covid19_twitter).

### Text
The two sub folders here **NotProcessed** and **Processed** contain their share of the Tweet json files. These files are
generated in the Get Tweets.ipynb notebook.

# Output
Visualizations are saved in this folder.

# ProcessOrNot
See readme in folder.
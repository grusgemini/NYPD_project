# NYPD_project

Goal of this project was to create a Python package that performs analysis on data concerning fire incidents, number of alcohol selling concessions, population and area.
This package cleans and prepares the data for analysis, calculates 17 correlations between data and returns the results in a txt file. 

Main hypothesis was that the number of alcohol selling concessions is correlated with number of fire incidents, and it is but not as much as one would expect (corr on a city level = 0.8093052879773235, corr on a voievodship level = 0.8710712833439904 ).

Another observation is that number of fire incidents is highly correlated with population on a voievodship level:
Correlation between the number of all fire incidents and population (voievodship): 	0.9594230219651461
Correlation between the number of actual fire incidents and population (voievodship): 	0.9245265472341879
Correlation between the number of false reports of fire incidents and population (voievodship): 	0.9441734210171577


# Profling
Profiling results can be found in the folder `profile_results`. Profiling has been done using cProfile

# Data
The data is available in the `data` folder. It comes from https://dane.gov.pl/ database. Exact links can be found in the `task.pdf` file. 

# Testing
To run the tests, please run `pytest ./tests`.

# README #

## What is this repository for? ##

This repo houses a vectorised python implementation of the Self-Organising Map (SOM) algorithm. It was created for use in the author's master dissertation and has now been released for anyone who might want to benefit from it. Please inform me of any additional functionality that might be desired.

### Getting started: ###

* Pull this repository to your local machine using git.
* Create a virtual environment
* Install the required libraries with: "pip install -r requirements.txt"
* Run examples of different settings and functionality with "python example.py" (based on the Iris dataset)
* Change which scenarios to run using the ScenariosToRun dictionary in example.py

### Features: ###

* Fits and plots features, Best Matching Unit (BMU) counts and training curves for SOM 
* Quantisation or topological error based stopping criteria
* Hypercube or random uniform weight initialisation
* Periodic Boundary Conditions (PBC) allowing the SOM to wrap like a torous
* Semi-Supervised training mode whereby the labels for a supervised learning problem are used to update the weights of the SOM but not to find the BMU
* Clusters SOM nodes using K-Means clustering and plots cluster maps
* Models, clusters and images are automatically saved (this is configurable)
* Quantisation and topological errors are automatically logged to a csv file for each run of the model (with parameter values saved for reproducibility)
* Has been used to fit data for a masters dissertation on a dataset with an excess of 1 million records

### Acknowledgements ###

* The poltting and preiodic boundary condition (PBC) functionality was adapted from the package SimpSOM (https://pypi.org/project/SimpSOM/)

### Author ###

Geoffrey Clark (geoffreyrussellclark@gmail.com)

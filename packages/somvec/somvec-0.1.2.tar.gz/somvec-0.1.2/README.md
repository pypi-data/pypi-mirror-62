# README #

## Description ##

This is a vectorised python implementation of the Self-Organising Map (SOM) algorithm. It was created for use in the author's master dissertation and has now been released for anyone who might want to benefit from it. Please inform me of any additional functionality that might be desired.

## Features: ##

* Fits and plots features, Best Matching Unit (BMU) counts and training curves for SOM 
* Quantisation or topological error based stopping criteria
* Hypercube or random uniform weight initialisation
* Periodic Boundary Conditions (PBC) allowing the SOM to wrap like a torous
* Semi-Supervised training mode whereby the labels for a supervised learning problem are used to update the weights of the SOM but not to find the BMU
* Clusters SOM nodes using K-Means clustering and plots cluster maps
* Models, clusters and images are automatically saved (this is configurable)
* Quantisation and topological errors are automatically logged to a csv file for each run of the model (with parameter values saved for reproducibility)
* Has been used to fit data for a masters dissertation on a dataset with an excess of 1 million records

## Example Plots on Iris Dataset ##

![Petal Length](/Docs/_images/petalLength.png)
![Sepal Width](/Docs/_images/sepalWidth.png)
![Clusters](/Docs/_images/Clusters.png)
![BMU Counts](/Docs/_images/Map_BMU_Counts.png)

## Example Script with the Iris Dataset: ##

	
	import numpy as np
	import pandas as pd
	from somvec import SOM
	from sklearn.datasets import load_iris
	
	if __name__ == '__main__':
		#load dataset and create dataframe
		iris = load_iris()
		target = iris['target']
		cols = ['sepalLength','sepalWidth','petalLength','petalWidth']
		df = pd.DataFrame(iris['data'], columns=cols)
		print('Shape of dataset: ', df.shape)

		#scenarios to test:
		show_plot = True
		ScenariosToRun = {
			'Base': True
			,'Quantisation_Error': False
			,'Hypyercube': False
			,'Non_PBC': False
			,'Other_Params': False
			,'Semi_Supervised': False
			,'Fully_Supervised': False
			,'OtherFunctionality': False
		}

		if ScenariosToRun['Base']:
			#Base scenario
			scenarioName = 'Base'
			#create class with some of the default parameters to demonstrate parameterisability
			som = SOM(df, scenarioName=scenarioName, save=True, savePath='SavedModels/', load=False
				, loadPath='SavedModels/', saveImages=True, imagePath='Images/', saveClusters=True, clusterPath='Clusters/')
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Quantisation_Error']:
			#Quantization Error scenario
			scenarioName = 'Quantisation_Error'
			som = SOM(df, scenarioName=scenarioName, errType='Quantisation')
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Hypyercube']:
			#Hypercube Intialisation scenario
			scenarioName = 'Hypyercube'
			som = SOM(df, scenarioName=scenarioName, weightInitialisation='hypercube')
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Non_PBC']:
			#Non_PBC scenario (without periodic boundary conditions so that the cube does not wrap around)
			scenarioName = 'Non_PBC'
			som = SOM(df, scenarioName=scenarioName, PBC=False)
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Other_Params']:
			#Other_params scenario: change some of the training params to suit the specific problem
			scenarioName = 'Other_Params'
			som = SOM(df, scenarioName=scenarioName, epochs=200, initialLearnRate=0.2
				, initialKernelWidth=10, decayLearnRate=10, decayKernelWidth=20, errWindow=40
				, errThreshold=1e-6, seed=99)
			som.fit(show_plot=show_plot, verbose=False)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Semi_Supervised']:
			#semi-supervised learning (include the target in the training data)
			scenarioName = 'Semi_Supervised'
			copy_df = df.copy()
			copy_df['target'] = target
			classificationAttributes = np.array([4])
			som = SOM(copy_df, scenarioName=scenarioName, classificationAttributes=classificationAttributes)
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['Fully_Supervised']:
			#fully-supervised learning (include the target in the training data)
			scenarioName = 'Fully_Supervised'
			copy_df = df.copy()
			copy_df['target'] = target
			som = SOM(copy_df, scenarioName=scenarioName)
			som.fit(show_plot=show_plot)

			labels = som.cluster(K=3, show_plot=show_plot)

		if ScenariosToRun['OtherFunctionality']:
			scenarioName = 'Base'
			som = SOM(df, load=True, scenarioName=scenarioName)

			#load model and clusters and plot the features and clusters
			som.loadModel()
			som.loadClusterLabels()
			labels = som.assignClusterLabels()

			#plot the Som map subsequently
			for f in range(som.n_features):
				som.plotMap(f, 'Blues', show_plot=True)

			#plot clusters
			som.plotMap(toPlot=som.mapClusters, FeatureName='Clusters', show_plot=True)#Note that som.mapClusters represents the cluster labels for each training record

			#use Silhouette score to optimise number of clusters (it seems to always recommend very few numebrs of clusters - not certain this is a reliable technique)
			som.optimiseCluster(maxK=10)

### Acknowledgements ###

* The plotting and preiodic boundary condition (PBC) functionality was adapted from the package SimpSOM (https://pypi.org/project/SimpSOM/)

### Author ###

Geoffrey Clark (geoffreyrussellclark@gmail.com)

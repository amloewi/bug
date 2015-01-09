#from future import division
import random
import csv

import networkx as nx
#from matplotlib import pyplot as plt
#import numpy as np

N = 50
num_iterations = 10
densities = []#np.zeros((num_iterations, (N*(N-1))/2.))

for n in range(num_iterations):
	print 'iteration: ', n
	densities.append([])

	g = nx.DiGraph()
	g.add_nodes_from(range(N))
	order = range(N)
	random.shuffle(order)

	for i in order:
		g.add_edges_from([(order[i],j) for j in order[i+1:]])

	h = nx.DiGraph()
	h.add_nodes_from(range(N))
	edges = g.edges()
	random.shuffle(edges)

	for ei, e in enumerate(edges):
		h.add_edge(*e)
		num_paths = 0
		paths = nx.all_pairs_shortest_path(h)
		for ego in paths:
			for alter in paths[ego]:
				if len(paths[ego][alter]) > 1:
					num_paths += 1
		densities[-1].append(num_paths*2./(N*(N-1)))#[n,ei] = num_paths*2./(N*(N-1))

#for i in densities:
#	plt.plot(densities[i])

# Output results as csv
#np.savetxt("/Users/shellicious/Sites/bug/densities.csv", densities, delimiter=",")


with open("/Users/shellicious/Sites/bug/densities.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(densities)


# The code in R that shows -- gamma is a great fit. (If ...
#	you ignore the negative values, the existence of which
#   is still puzzling.)
# setwd("/Users/shellicious/Sites/bug")
# data = as.matrix(read.csv("densities.csv", header=FALSE))

# library(drc)
# library(fitdistrplus)

# plot(-5, xlim=c(0,1200), ylim=c(0,1))
# for(i in 1:nrow(data)){
#   lines(data[i,])
# }
# avg.cdf = colMeans(data)
# avg.pdf = diff(avg.cdf)

# fit.gamma = fitdist(avg.pdf[avg.pdf > 0], "gamma")
# plot(fit.gamma)



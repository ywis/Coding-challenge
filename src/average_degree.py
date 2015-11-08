# example of program that calculates the average degree of hashtags

import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from datetime import datetime

txt = open('/Users/siqi/DataEngineering/coding-challenge/tweet_output/ft1.txt')
content = txt.read()  # return a string object
line = content.split('\n')
txt.close()

# Extract hashtag from each tweet
N = len(line)  # number of tweets in tweets.txt
output = [0] * N  # number to be decided later
timestamp = [0] * N  # Number of timestamps

for i in range(len(line)):
    timestamp[i] = re.findall(r'\w+ \d\d \d\d:\d\d:\d\d', line[i])
    output[i] = re.findall(r'#(\w+)', line[i])

# Select the tweets that have at least two distinct hashtags
j = 0  # Initialize the number of clean hashtags
for i in range(len(line)):
    output[i] = list(set(i.lower() for i in output[i]))
    if len(output[i]) >= 2:
        j += 1

clean_output = [0] * j
clean_timestamp = [0] * j
k = 0
for i in range(len(line)):
    if len(output[i]) >= 2:
        clean_output[k] = output[i]
        clean_timestamp[k] = timestamp[i]
        k += 1

# Set the initial number of tweets of reading
n0 = 0
n1 = 1
FMT = '%b %d %H:%M:%S'
t0 = clean_timestamp[n0][0]
t1 = clean_timestamp[n1][0]
tdelta = datetime.strptime(t1, FMT)-datetime.strptime(t0, FMT)

while tdelta.seconds < 60:
    n1 += 1
    t1 = clean_timestamp[n1][0]
    tdelta = abs(datetime.strptime(t1, FMT) - datetime.strptime(t0, FMT))

n1_start = n1
f = open('/Users/siqi/DataEngineering/coding-challenge/tweet_output/ft2.txt', 'w')

# Add another tweet and see how the another tweet works
for i in range(n1_start, len(clean_timestamp)-1):
    n1 += 1
    t1 = clean_timestamp[n1][0]
    tdelta = abs(datetime.strptime(t1, FMT) - datetime.strptime(t0, FMT))
    while tdelta.seconds > 60:
        n0 += 1
        t0 = clean_timestamp[n0][0]
        tdelta = abs(datetime.strptime(t1, FMT)-datetime.strptime(t0, FMT))
    nodes = list(itertools.chain(*clean_output[n0:n1+1]))
    # remove the duplicate list items
    clean_nodes = list(set(i.lower() for i in nodes))

    # remove https character at the end of the node character
    for i1 in range(len(clean_nodes)):
        if len(re.findall('https$', clean_nodes[i1])) == 1:
            clean_nodes[i1] = clean_nodes[i1].replace('https', '')

    # Add nodes to the graph
    G = nx.Graph()
    for k in range(len(clean_nodes)):
        G.add_node(clean_nodes[k])

    # Generate the edges
    edges = [0]*len(clean_output)
    i = 0
    for item in clean_output[n0:n1+1]:
        temp = [x.lower() for x in tuple(item)]
        edges[i] = list(itertools.combinations(tuple(temp), 2))
        i += 1

    # Add the edges to the graph
    for k in range(len(clean_output[n0:n1+1])):
        G.add_edges_from(edges[k])
    # Calculate the average number of vertexes and print out in a 60 second window
    def average_degree():
        return 2.0*G.number_of_edges()/G.number_of_nodes()

    f.write("{0:.2f}".format(average_degree())+'\n')
    G.clear()

f.close()

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:47:39 2021

@author: mburk
"""
import sys
import math
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name



class Search(Node):
    def __init__(self):
        self.visited = []
        self.queue = []
        self.weightedQueue = {}
        self.newNodes = []
        self.neighborL = []
        self.return_path = []

    
    def dfs(self, node, goalCity, G):
        self.visited.append(node)

        self.queue.insert(0,node)
        
        self.node = str(node)
        self.neighborList = (G.adj[node])
     
        while self.queue:
            print("DFS Queue: ",self.queue[0])
            s = self.queue.pop(0) #right  here
            nList = self.getNeighbor_dfs(s)
            if (s == goalCity):
                print('\n'*2)
                print("*"*10,"DFS SOLUTION","*"*10)
                print("These are visited nodes\n >>>", self.visited, "\n")
                
                print("Found:", goalCity,"")
                self.return_path.append(goalCity)
                self.find_path(goalCity)
                print("*"*10,"DFS END","*"*10)
                break
            else:
                for neighbor in nList:
                    if neighbor not in self.visited:
                        #by appending it's a queue, if it's insert then its a stack
                        self.visited.append(neighbor) ###insert cmd instead
                        self.queue.insert(0,neighbor)   
   
    def getNeighbor_dfs(self, CurrNode):
        new_nodes = []
        inpt = str(CurrNode)
        neighbor = list(G.adj[inpt])
        for n in neighbor:
            if n not in self.queue:
                if n not in self.visited:
                    new_nodes.insert(0,n)
                    
        newNeighbor = new_nodes
        self.neighborL.append(new_nodes)
        return newNeighbor  
                    
    def bfs(self, node, goalCity, G):
        self.visited.append(node)
        self.queue.append(node)
        self.node = str(node)
        self.neighborList = (G.adj[node])
   
        while self.queue:
            print("BFS Queue: ",self.queue[0])

            s = self.queue.pop(0)
            nList = self.getNeighbor(s)
            if (s == goalCity):
                print('\n'*2)
                print("*"*10,"BFS SOLUTION","*"*10)
                print("These are visited nodes\n >>>", self.visited, "\n")
                
                print("Found:", goalCity,"")

                self.return_path.append(goalCity)
                self.find_path(goalCity)
                print("*"*10,"BFS END","*"*10)

                break
            else:
                for neighbor in nList:
                    if neighbor not in self.visited:
                        self.visited.append(neighbor)
                        self.queue.append(neighbor)
     
    def astar_pseudocode(self):
        return      """Notes: Pseudocode copied from online source for astar implementation
                    Initialise open and closed lists
                    Make the start vertex current
                    Calculate heuristic distance of start vertex to destination (h)
                    Calculate f value for start vertex (f = g + h, where g = 0)
                    WHILE current vertex is not the destination
                        FOR each vertex adjacent to current
                            IF vertex not in closed list and not in open list THEN
                                Add vertex to open list
                            END IF
                            Calculate distance from start (g)
                            Calculate heuristic distance to destination (h)
                            Calculate f value (f = g + h)
                            IF new f value < existing f value or there is no existing f value THEN
                                Update f value
                                Set parent to be the current vertex
                            END IF
                        NEXT adjacent vertex
                        Add current vertex to closed list
                        Remove vertex with lowest f value from open list and make it current
                    END WHILE""" 
                    
    def astar(self, node, goalCity, G):
        print('\n'*5)
        #print(self.astar_pseudocode())
        self.visited.append(node)
        self.queue.append(node)
        self.node = str(node)
        self.neighborList = (G.adj[node])

        while self.queue:
            s = self.queue.pop(0)
            nList = self.getNeighbor(s)
            OptimizationResults = {}
            
            if (s == goalCity):
                        #print("These are visited nodes\n >>>", self.visited, "\n")
                        
                        print("Found:", goalCity,"")
                        self.return_path.append(goalCity)
                        self.find_path(goalCity)
                        break
            else:
                print("Calculate f = g + h for each neighbor of ", s)
                for neighbor in nList:
                    if neighbor not in self.visited:
                        self.LastParent = s
                        self.visited.append(neighbor)
                        OptimizationResults[neighbor] = self.astar_Calculate_H(s,neighbor)
                        self.queue.append(neighbor)
                print("Having f for eligible nodes - choose least cost (H)")
                print("OptimizationResults: ", OptimizationResults)
                
     
    def astar_Calculate_H(self,nodePar,n):
        print(n)
        h = G[nodePar][n]['weight'] 
        g = G[nodePar][n]['KM']
        print(f"Parent {nodePar} to Node {n} calculated f= {h} ADD {g}")
        return float(h) + float(g)
               
    def getNeighbor(self, CurrNode):
        new_nodes = []
        inpt = str(CurrNode)
        neighbor = list(G.adj[inpt])
        for n in neighbor:
            if n not in self.queue:
                if n not in self.visited:
                    new_nodes.append(n)
                    
        newNeighbor = new_nodes
        self.neighborL.append(new_nodes)
        return newNeighbor    

   
    
    def find_path(self, goalCity):
        #may get a recursion error can attempt to solve it
        currNode = goalCity
        neighbor = list(G.adj[currNode])
        
        for n in neighbor:
            if n == self.visited[0]:
                self.return_path.insert(0, n)
                print("Here is the path to the goal")
                print(self.return_path)
                break
         
            if n in self.visited and n not in self.return_path:
                self.return_path.insert(0, n)
                self.find_path(n)
                if self.return_path[0] == self.visited[0]:
                    break
            
###End Search class

#Helper functions

def open_file(in_file):
    roadsList = []
    weightsList = []
    
    with open(in_file, 'r') as words:
        i = 0
        for line in words:
            if i > 5 and i < 71:
                mystring = line
                myString = re.sub(r"[\n\t\s]*", "", mystring)
                weightsList.append(myString.strip().split(','))
            elif i >= 74:            
                mystring = line
                myString = re.sub(r"[\n\t\s]*", "", mystring)
                roadsList.append(myString.strip().split(','))
            i = i + 1    

    return roadsList,weightsList

def create_tree(node_list):
    # edge attr distance between cities
    df = pd.DataFrame(node_list, columns=['City1', 'City2', 'KM'])
    
    #Call heuristic function here - netity1', 'City2')
    G = nx.from_pandas_edgelist(df, 'City1', 'City2', edge_attr='KM')
    
    
    return G

def create_tree_with_weights(node_list,weights_list):
    print("in create tree with weights")
    # edge attr distance between cities
    df = pd.DataFrame(node_list, columns=['City1', 'City2', 'KM'])
    
    dfWeights = pd.DataFrame(weights_list,columns=(['City1','lat','long']))
    dfWeights = dfWeights.set_index('City1')
    dfWeights["lat"] = pd.to_numeric(dfWeights["lat"])
    dfWeights["long"] = pd.to_numeric(dfWeights["long"])
    
    print(dfWeights.head())
    print (dfWeights.loc["albanyNY"].lat)
    print (dfWeights.loc["albanyNY"].long)
    
    
    
    df["weight"] = dfWeights.loc["albanyNY"].lat
    for index,row in df.iterrows():
        Lat1 = dfWeights.loc[row["City1"]].lat
        Long1 = dfWeights.loc[row["City1"]].long
        Lat2 = dfWeights.loc[row["City2"]].lat
        Long2 = dfWeights.loc[row["City2"]].long
        h = math.sqrt((69.5 * (Lat1 - Lat2)) ** 2 + (69.5 * math.cos((Lat1 + Lat2)/360 * math.pi) * (Long1 - Long2))  ** 2)
        
        
        row["weight"] = h
        print(index, ":", row["City1"], row["City2"], row["weight"])
    

 #   df["weight"] = dfWeights.loc[df["City1"]].lat 
    
    
    #replace with calc
    #df["weight"] = df["KM"]
#   wt = sqrt((69.5 * (dfWeights[Lat1 - Lat2)) ^ 2 + (69.5 * cos((Lat1 + Lat2)/360 * pi) * (Long1 - Long2)) ^ 2)

    #df['weight'] = df.City1 + df.City2
    #Call heuristic function here - networkx see formula in input data
    #HEURISTIC IS THE WEIGHT OF THE NODE
    ##https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html
    
    G = nx.from_pandas_edgelist(df, 'City1', 'City2', edge_attr=['KM','weight'])
    
    #debug
    #print (G["albanyNY"])
    #G["albanyNY"]['boston']['weight'] = 3
    #G["albanyNY"]['montreal']['weight'] = 3
    
    #for (u, v, wt) in G.edges.data('weight'):
    #    print(f"({u},{v}, wt:{wt})")
    #for (u, v, km) in G.edges.data('KM'):
    #    print(f"({u},{v}, KM:{km}")
        
    return G

def callingSearch(startCity, goalCity, typeOfSearch):
    g = Search()

    #G is global and created in MAIN    
    if typeOfSearch == "bfs":
        g.bfs(startCity, goalCity, G)   
    
    if typeOfSearch == "dfs":
        g.dfs(startCity, goalCity, G)       

    if typeOfSearch == "astar":
        g.astar(startCity, goalCity, G)       

#MAIN
if __name__ == "__main__":
    
    for i, arg in enumerate(sys.argv):
      if (i > 0):
        print(f"Argument {i}: {arg}")  

    #assign runtime parms
    in_file = sys.argv[1]
    start_city = sys.argv[2]
    goal_city = sys.argv[3]
    
    search_algos = ["bfs","dfs","astar"]
    roadsList,weightsList = open_file(in_file)
    
    #print('\n'*3)
    #print("EDGE list: ",roadsList)
    #print('\n'*3)
    #print("WEIGHTS List: ",weightsList)
    
    print('\n'*3)
    print(f"Starting Node: {start_city} -- Goal Node: {goal_city}")
    print('\n'*3)
   
    for x in range(0,3):
        if ( search_algos[x] == "bfs"  or search_algos[x] == "dfs"):
            #create global G
            print("Invoking search algo:", search_algos[x])
            #G = create_tree(roadsList)
            #callingSearch(start_city, goal_city, search_algos[x])
            print('\n'*5)
        else:
            #create global G
            print("Invoking search algo:", search_algos[x])
 
            G = create_tree_with_weights(roadsList,weightsList)
            callingSearch(start_city, goal_city, search_algos[x])
            print('\n'*5)
            
    
# -*- coding: utf-8 -*-
from gurobipy import *

############################################################
#### Please run extractor.py before running this script ####
############################################################

print("Optimizing best secure points location")

#### Model iniciation ####

m=Model("P2")

#### Decision Variables ####
B=6000000
M=1000000000000
x={}    
y={}
P={}
T={}
for j in idsecure:
    #### Binary, if node j is used safe point ####
    x[j]=m.addVar(vtype=GRB.BINARY, name="x_%s" %(j))
    
for i in N:
    for j in idsecure:
        #### Binary, if people travels from i to j ####
        y[i,j]=m.addVar(vtype=GRB.BINARY, name="y_%s_%s" %(i,j))
        #### Interger, Flow of people from i to j ####
        P[i,j]=m.addVar(vtype=GRB.INTEGER, name="P_%s_%s" %(i,j), lb=0)


m.update()

#### Objective Function ####

m.setObjective(quicksum(y[i,j]*ultimatematrix[i,j] for (i,j) in nodetosecure))

#### Constraints ####

for i in N:
    for j in idsecure:
        
        #### Only if node is safe point then it can has flow ####
        m.addConstr(x[j]>=y[i,j])
        
        #### Flow has to be positive ####
        m.addConstr(P[i,j]>=0)
        
        #### if there are no people going to j then there can be no flow ####
        m.addConstr(P[i,j]<=M*y[i,j])
        
#### Node can only be assigned to at least 1 safe point and maximum 2 safe ponts ####
for i in N:
    m.addConstr(quicksum(y[i,j] for j in idsecure) >= 1)
    m.addConstr(quicksum(y[i,j] for j in idsecure) <= 2)
    
#### Outwards flow has to be equal to population in node ####
for i in N:
    m.addConstr(quicksum(P[i,j] for j in idsecure) == p[i])
    

#### Budget ####
    
m.addConstr(quicksum(C[j]*x[j] for j in idsecure) +
            quicksum(P[i,j]*V[j] for (i,j) in nodetosecure)+
            quicksum(D[j]*x[j] for j in idsecure) <= B)    

m.update()

m.ModelSense = 1

m.update()

m.optimize()

if m.Status == GRB.OPTIMAL:
    print("Opt.Value", m.ObjVal)


#### Draw nodes and edges ####
import networkx as nx
G = nx.Graph()
G.add_nodes_from(N)
#G.add_nodes_from(idsecure)
#for (i,j) in A:
#    G.add_edge(i,j)
securenodes=[]
for (i,j) in nodetosecure:
    if y[i,j].X==1 or y[i,j].X==2  :
        G.add_edge(i,j)
        if j not in securenodes:  
            securenodes.append(j)
#        print(y[i,j])   
G.add_nodes_from(securenodes)
position={}
for i in range(len(nodeswithposition)+1):
    if i == 0:
        pass
    else:
        a=nodeswithposition[i]
        position[i]=a
nx.draw(G, position, node_color="red",node_size=20, nodelist=N)
nx.draw(G, position, node_color="green",node_size=30, nodelist=idsecure)
nx.draw(G, position, node_color="blue",node_size=70, nodelist=securenodes)





from pulp import *
import numpy as np
import random
import pandas as pd 
 

def LP():
    #Generating 15 random numbers for R15 polytope that will be assigned to each node in objective function
    randomlist = []
    for i in range(0,15):
        n = random.randint(-100,100)
        randomlist.append(n)
    #print(randomlist) #used for checking the output whether the objective function modelled correctly
    random_numbers= np.array(randomlist)

    #creating LP problem
    global model #defining variable as global so can be accessed outside of the function
    model = LpProblem("problem", LpMaximize)
   
    # Creating problem variables, weight of each node of R15 polytope
    x1= LpVariable('w1', cat='Integer') #top vertex
    x2= LpVariable('w2', cat='Integer')
    x3= LpVariable('w3', cat='Integer')
    x4= LpVariable('w4', cat='Integer')
    x5= LpVariable('w5', cat='Integer') #right hand bottom vertex (corner) of polytope
    x6= LpVariable('w6', cat='Integer')
    x7= LpVariable('w7', cat='Integer')
    x8= LpVariable('w8', cat='Integer')
    x9= LpVariable('w9', cat='Integer') #left hand bottom vertex (corner) of polytope
    x10= LpVariable('w10', cat='Integer')
    x11= LpVariable('w11', cat='Integer')
    x12= LpVariable('w12', cat='Integer')
    x13= LpVariable('w13', cat='Integer')
    x14= LpVariable('w14', cat='Integer')
    x15= LpVariable('w15', cat='Integer')

    #creating list of weights
    list_nodes=[]
    list_nodes.extend([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15])

    #converting list into array for further processing
    nodes=np.array(list_nodes)
    #print(nodes) #used for checking the output whether the objective function modelled correctly
    
    # Problem Constraints

    # Nonnegativity constraints
    model += x1 >= 0
    model += x2 >= 0
    model += x3 >= 0
    model += x4 >= 0
    model += x5 >= 0
    model += x6 >= 0
    model += x7 >= 0
    model += x8 >= 0
    model += x9 >= 0
    model += x10 >= 0
    model += x11 >= 0
    model += x12 >= 0
    model += x13 >= 0
    model += x14 >= 0
    model += x15 >= 0

    # Constraints for each node 
    #(nodes were numbered as shown in attached file: [nodes_numbered.jpg], with 1,5,9 being the vertices of the polytope )
    
    #1st node
    model += x1+0 <= 10
    model += x1+6 >= 16
    model += x1+4 >= 13
    model += x1+7 >= 4+x2
    model += x1+12 >= x12+6
    model += x1+x13 <= x12+x2
    model += x2+7 >= x1+9
    model += x12+12 >= x1+16
    model += x1+x12 >= 12+x2
    model += x1+x2 >= x12+7
    #2nd node
    model += x2+9 >= 7+x3
    model += x2+x15 <= x3+x13
    model += x2+11 <= x3+9
    model += x2+x11 <= x12+x13
    model += x2+x13 >= x12+x3
    model += x2+x3 >= 9+x13
    #12rd node
    model += x12+16 >= 12+x11
    model += x12+x14 <= x11+x13
    model += x12+19 <= x11+16
    model += x12+x11 >= 16+x13
    #11th node
    model += x11+19 >= x10+16
    model += x11+x8 <= x10+x14
    model += x11+22 <= 19+x10
    model += x10+x11 >= x14+19
    model += x14+x11 >= x13+x10
    model += x11+x15 <= x13+x14
    #13th node
    model += x13+x7 <= x14+x15
    model += x13+x15 >= x3+x14
    model += x13+x4 <= x15+x3
    #3rd node
    model += x3+x6 <= x15+x4
    model += x3+11 >= x4+9
    model += x3+x4 >= 11+x15
    model += x3+13 <= x4+11
    #10th node
    model += x10+16 <= x11+19
    model += x10+x14 >= x11+x8
    model += x10+27 <= x9+x8
    model += x10+22 >= x9+19
    model += x10+25 <= x9+22
    model += x10+x8 >= x14+x9
    model += x10+x9 >= x8+22
    model += x10+x7 <= x8+x14
    #14th
    model += x14+26 <= x8+x7
    model += x14+x6 <= x7+x15
    model += x14+x7 >= x8+x15

    #15th
    model += x15+25 <= x7+x6
    model += x15+x6 >= x7+x4
    model += x15+x5 <= x6+x4
    #node 4
    model += x4+23 <= x5+x6
    model += x4+13 >= 11+x5
    model += x4+x5 >= 13+x6
    model += x4+14 <= x5+13

    #node 9
    model += x9+25 >= 22+28
    model += 28+25 >= x9+28
    model += x9+27 >= x8+28
    model += x9+28 >= 25+27
    model += x8+27 >= 26+x9

    #node 8
    model += x8+25 <= 26+x7
    model += x8+26 >= x7+27

    #node 7
    model += x7+25 >= 26+x6
    model += x7+23 <= x6+25

    #node 6
    model += x6+20 <= 23+x5
    model += x6+23 >= x5+25

    #node 5
    model += x5+14 >= 20+13
    model += x5+15 <= 20+14
    model += x5+20 >= 23+14



    # Objective function defined to maximize
    model += lpSum(nodes*random_numbers)  

    # Solve the problem
    status = model.solve(GLPK(msg=0)) #specifying GLPK glpsol solver is used
    #status = model.solve() #deafult solver

    # Display the problem
    #print(model)
 
    # Printing the final solution
    for variable in model.variables():
        print(variable.name, "=", variable.varValue)
    print ("Total value objective function:")
    print(value(model.objective))
    

# Running model 1000 times and generating 1000 .lp files  
for i in range(0,1000):
    global model
    LP()
    model.writeLP('LPfile' +str(i+1)+ '.lp')
pass

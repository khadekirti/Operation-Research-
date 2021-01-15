from gurobipy import * 
"""
Team: 
Vikram Rayakottai Niranjanvel (Student ID: 45484450)
Kirti Khade (Student ID: 45733130)
"""
#----------------------------------------------------------------------------------------------------#
#Sets
d_c=["DO","D1","D2"] # Set for Distribution Centers
s_m=["SO","S1","S2","S3","S4","S5","S6","S7","S8","S9"] #Set for SuperMarket


#----------------------------------------------------------------------------------------------------#
#Data

# Cost of transportation of one truckload from each distribution centre to each store. 
cost=[[1938,1424,1407,918,2140,1421,1876,1194,1459,900],
      [1801,1843,1898,1613,919,912,1063	,1553,1453,2220],
      [3074,2575,857,2171,2800,1942	,2699,1223,2525,2038]]  


# Distribution centre capacity  - the maximum capacity of distribution system.	  
dc_capacity= [28,58,66]

# Weekly demand at the store, including the surges	  
sm_demand=[[8,   12, 12 ,18 ,7  ,8  ,9  ,10 ,8  ,18],
           [8,   12	,12	,18	,7	,8	,9	,14	,8	,21],
           [8	,12	,12	,18	,7	,8	,9	,10	,8	,18],
           [8	,12	,14	,18	,7	,8	,31	,17	,8	,18],
           [33	,12	,12	,18	,7	,8	,9	,15	,8	,18],
           [8	,12	,12	,18	,7	,8	,31	,11	,8	,18]]

d_capacity_max = 75

# Specifying the length of the above arrays
S_C = range(len(sm_demand))
S = range(len(s_m))
D = range(len(d_c))

#----------------------------------------------------------------------------------------------------# 
# Initialising the model
m = Model("logistics")

# Declaring variables for the model
X={}
for d in D:
    for s in S:
        X[d,s]=m.addVar()
#----------------------------------------------------------------------------------------------------# 
# Objective Function
# Setting up the objective function of the model- Proportion of contribution of each distribution center for a shopping market
m.setObjective(quicksum(X[d,s]*cost[d][s] for d in D for s in S),GRB.MINIMIZE)

#----------------------------------------------------------------------------------------------------# 
# Adding Constraints

# The sum of proportion for every distribution = 1  
sm_demand_constrain={}
for s in S:
   sm_demand_constrain[s]=m.addConstr((quicksum(X[d,s] for d in D))==1)  
   
# Total capacity of the distribution centres should be maintained for each scenario
cap_c={}
for s_c in S_C:
    for d in D:
        cap_c[d]=m.addConstr(quicksum(X[d,s]*sm_demand[s_c][s] for s in S)<=dc_capacity[d])   
        
# Constriants on D0 + D1 = 75 should be maintained for each secnario 
for s_c in S_C:
    labour=m.addConstr(quicksum((X[0,s]*sm_demand[s_c][s])+(X[1,s]*sm_demand[s_c][s]) for s in S ) <=d_capacity_max)

m.optimize()
#----------------------------------------------------------------------------------------------------#
# Getting final values 

# Getting values for proportion   
# Variabale with dummy data to store the final proportions
final=[[0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]
total=0
# Display the proportions and push it to final
print("Common proportion from each Distribution Centre for each Supermarket")
for s in S: 
    print("\n"+s_m[s]+": ")                                #skim through each supermarket
    for d in D:   
        print("  "+d_c[d]+": "+str(X[d,s].x))               #Within each supermarket skim through the Distribution centre
        final[d][s]=float(X[d,s].x)
 
 
# Verifying the resulting by cross checking the quantity and results for all scenarios and getting the expense 
print("The quantity of load from each distribution centre sent to each supermarket split by scenario")
for s_c in S_C:                                             #Skim through each scenario  
    dis_cen=[0,0,0]                                         #Dummy variables used to calaculate the total usage for the scenario
    total=0
    print("------------------------------------------------------------------------------------")
    print("Scenario: "+str(s_c))                            #Print scenario number
    for s in S:                                             #Skim through each supermarket in the scenario
        s_total=0
        print("\n"+s_m[s])                                  #Print the supermarket name
        for d in D:                                         #Print the distribution centres
            print("  "+d_c[d]+": "+str(final[d][s]*sm_demand[s_c][s]))               #Print the quantity from the current distribution centre to the current supermarket
            total+=(final[d][s]*sm_demand[s_c][s]*cost[d][s])  #Total cost for this scenario
            s_total+=final[d][s]*sm_demand[s_c][s]             #Total for this super market 
            dis_cen[d]+=final[d][s]*sm_demand[s_c][s]          #Total for that distribution centre
        print("  Total:"+str(s_total))                        #Displaying supermarket total for that scenario
    print("\nTotal Expense for the scenario: "+str(total))                          #Displaying the total expense for that scenario
    print("\nDistribution Centre Constraints:")                        
    for d in D:
        print(d_c[d]+" capacity: "+str(dc_capacity[d])+"    Answer:"+str(dis_cen[d]))  #displaying the quantity from the distribution centre and the constraint value
    print("Labour capacity in North: "+str(d_capacity_max)+"\nLabour used now: "+str(dis_cen[0]+dis_cen[1]))

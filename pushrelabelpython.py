#!/usr/bin/env python
# coding: utf-8

# In[1]:


#define a class for the nodes in the network. This will hold network information about their position, neighbours and variables for use during the algorithm.
class Network:
    def __init__(self, source, sink, neighbours, residual_capacity):
        self.flow = source
        self.sink = sink
        self.excess = max(0,source - sink)
        self.neighbours = neighbours
        self.degree = len(neighbours)
        self.arc_flow = [0]*self.degree
        self.arc_capacity = residual_capacity
        self.label = 0
        
#assume s,t are well-formatted. N.B. nodeID = 0 usually won't exist but the code can support it.
s = [1, 1, 1, 2, 3, 4,5,5,5,5,5,5,  6, 6,7,8,3,1] #input value - of length the number of edges
t = [2, 3, 4, 3, 4, 5,6,7,8,9,10,11,10,9,11,9,9,11] #input value - of length the number of edges

source = [0,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #input value - of length the number of nodes
sink = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #input value - of length the number of nodes
edge_capacity = [5]*18 #input value - of length the number of edges
limit = 100 #input value - size should be around log(number of nodes)

#When the first item of the queue cannot be pushed, increase it's label value by one, then setup the Queue so that the lowest label is at the front.
#Assertion: For each neighbour of 'node', there is a reason why 'node' cannot push. This can be for either of the following reasons:
#arc_capacity[node][neighbour] == arc_flow[node][neighbour], so the 'node' has already pushed as much 'flow' as possible onto this neighbour. 
#node.label != neighbour.label + 1. In this case, the node.label should be increased so that the problem might be fixed at a later time.
#Assertion: node.label > neighbour.label + 1 => arc_capacity[node][neighbour] == arc_flow[node][neighbour].
#This is because, at some time, we had: node.label == neighbour.label + 1, AND 'node' chose to relabel.
def Relabel(node,current_neighbour,Queue):
    N[node].label += 1
    node = Queue[0].pop(0)
    if not len(Queue) == 1:
        Queue[1].insert(0,node)
    Queue = maintainQueue(Queue)
    if Queue:
        node = Queue[0][0]
        current_neighbour = 0
    return node,current_neighbour,Queue
    
#Route the maximum possible amount of flow from 'node' to 'target_node'.
#Assertion: node.label == target_node.label + 1, so flow always travels downwards with respect to label.
#Assertion: node.excess is > 0, as the 'node' is in the 'Queue'.
#Assertion: arc_capacity[node][current_neighbour] > arc_flow[node][current_neighbour], as this statement is checked before 'Push' is called.
def Push(node,current_neighbour,target_node):
    Amount = min(N[node].excess,N[node].arc_capacity[current_neighbour] - N[node].arc_flow[current_neighbour])
    N[node].flow -= Amount
    N[target_node].flow += Amount
    N[node].excess = max(0,N[node].flow - N[node].sink)
    N[target_node].excess = max(0,N[target_node].flow - N[target_node].sink)
    N[node].arc_flow[current_neighbour] += Amount
    N[target_node].arc_flow[N[target_node].neighbours.index(node)] -= Amount
    return
        
#Runs directly after a 'Push' to make sure the 'Queue' is correctly formatted. It is essential that the Queue maintain nodes with excess supply in labelled order.
def AfterPush(node,current_neighbour,Queue,target_node):
    if N[node].excess == 0:
        node = Queue[0].pop(0)
    if N[target_node].excess > 0:
        Queue.insert(0,[target_node])
    Queue = maintainQueue(Queue)
    if not Queue:
        return node,current_neighbour,Queue
    if node != Queue[0][0]:
        node = Queue[0][0]
        current_neighbour = 0
    return node,current_neighbour,Queue

#Removes empty values from the front of the Queue. The Queue is setup to keep empty values at the back up to the limit value, but must keep it's first value non-empty.
def maintainQueue(Queue):
    if Queue:
        if not Queue[0]:
            Queue.pop(0)
            Queue = maintainQueue(Queue)
    return Queue

#Decides whether to increase 'current neighbour', push(node - > target_node), or relabel(node).
def PushRelabelMain(node,current_neighbour, Queue):
    if current_neighbour > N[node].degree - 1:
        current_neighbour = 0
        node,current_neighbour,Queue = Relabel(node,current_neighbour,Queue)
    else:
        target_node = N[node].neighbours[current_neighbour]
        if N[node].label == N[target_node].label + 1:
            if N[node].arc_capacity[current_neighbour] - N[node].arc_flow[current_neighbour] > 0:
                Push(node,current_neighbour,target_node)
                node,current_neighbour,Queue = AfterPush(node,current_neighbour,Queue,target_node)
            else:
                current_neighbour += 1
        else:
            current_neighbour += 1
    return node, current_neighbour, Queue

#setting up the remaining variables. These variables are indexed: [nodeID][neighbour_number], rather than [nodeID][neighbourID].
def PushRelabel(limit,number_nodes):
    number_nodes = max(max(s),max(t)) + 1
    number_edges = len(s)
    neighbours_network = []
    residual_network = []
    for i in range(number_nodes):
        neighbours = []
        residual_capacity = []
        for j in range(number_edges):
            if s[j] == i:
                neighbours.append(t[j])
                residual_capacity.append(edge_capacity[j])
            if t[j] == i:
                neighbours.append(s[j])
                residual_capacity.append(edge_capacity[j])
        neighbours_network.append(neighbours)
        residual_network.append(residual_capacity)
    N = [Network(source[i],sink[i],neighbours_network[i],residual_network[i]) for i in range(number_nodes)]
    Queue = [[i for i in range(number_nodes) if N[i].excess > 0]]
    for i in range(limit):
        Queue.append([])
    if Queue:
        current_neighbour = 0
        node = Queue[0][0]
        while Queue:
            node, current_neighbour, Queue = PushRelabelMain(node,current_neighbour, Queue)  
    return

PushRelabel(limit,number_nodes)
for i in range(number_nodes):
    print(N[i].arc_flow)
    print(N[i].label)


import sys
from collections import defaultdict
"""
Notes:
- For three-digit value of 123, position 0 is 3 and position 2 is 1

To-Do:
- Implement avoiding cycling (same value, same children nodes)
- IDS, A*, Greedy, Hill Climbing
- Add some sort of enum/struct for arguments in expand functions
- Implement case for when loop is more than 1000!
- Nodes MAY need ONE LAYER children array to check for cycles....
- Append 0s in front of digits less than 3 .... (easy)
"""

# global value
global nodesExpanded

class Node:
    def __init__(self, value, previousPosition, prevNode):
        self.value = value
        self.previousPosition = previousPosition
        self.prevNode = prevNode

def getSpecificDigit(value, position):
    return value // 10 ** position % 10

def getArgs():
    # Get the values from the argument
    try:
        return str(sys.argv[2]), str(sys.argv[1])
    except IndexError:
        #print("ERROR1")
        exit()

def getAdditionValue(index):
    dict = {0:-100, 1:100, 2:-10, 3:10, 4:-1, 5:1}
    return dict[index]

def expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):

    global nodesExpanded
    if nodesExpanded > 1000 or endState in traversedList:
        return

    # base class for recursion
    traversedList.append(node.value)
    if(not visitedDict.__contains__(node.value)):
        visitedDict[node.value] = [node.previousPosition]
    else:
        visitedDict[node.value].append(node.previousPosition)

    nodesExpanded += 1
    if node.value == endState:
        while(node.prevNode != None):
            pathList.insert(0,node.prevNode.value)
            node = node.prevNode
        pathList.append(endState)
        return

    # Loop over the 6 possibilities and transformations
    for i in range(6):
        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            if (i == 5):
                if(len(traversedQueue) != 0):
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
            continue

        # Use the getAdditionValue to add value to the current node and set it as a new node
        temp = Node(node.value + getAdditionValue(i), position,node)

        # Check if the computed value is forbidden
        if temp.value not in forbiddenSet:
            # Now check if it is in a cycle...
            # It is in a cycle if:
            # 1. 3 digits are same and
            # 2. Their children is same
            # which can be checked by the value of three digits and the value of
            # the previously disallowed position, called previousPosition
            if temp.value in visitedDict:
                if(temp.value == 234):
                    print("Check: " + str(temp.previousPosition in visitedDict[temp.value]))
                if temp.previousPosition in visitedDict[temp.value]:
                    if (i == 5):
                        if (len(traversedQueue) != 0):
                            temp = traversedQueue.pop(0)
                            expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
                    continue
                else:
                    visitedDict[temp.value].append(temp.previousPosition)


            # If its not in a cycle, then add it to the queue
            traversedQueue.append(temp)
            if (i == 5):
                if (len(traversedQueue) != 0):
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList,visitedDict)
        else:
            if (i == 5):
                if (len(traversedQueue) != 0):
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList,visitedDict)
            continue

def bfs(startState, endState, forbiddenSet):

    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    return traversedList, pathList

def expandDFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):
    # Need to complete this too....
    global nodesExpanded
    if nodesExpanded > 1000 or endState in traversedList:
        return

    # Base class for recursion
    traversedList.append(node.value)
    if (not visitedDict.__contains__(node.value)):
        visitedDict[node.value] = [node.previousPosition]
    else:
        visitedDict[node.value].append(node.previousPosition)
    nodesExpanded += 1

    # In the case that the root value is the end goal state value
    if node.value == endState:

        # Get the path values
        while(node.prevNode != None):
            pathList.insert(0,node.prevNode.value)
            node = node.prevNode
        pathList.append(endState)
        return

    # Loop over the 6 possibilities and transformations
    for i in range(6):
        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            continue

        # Use the getAdditionValue to add value to the current node and set it as a new node
        temp = Node(node.value + getAdditionValue(i), position, node)

        # Check if the number is forbidden
        if temp.value not in forbiddenSet:
            # Now check if it is in a cycle...
            # It is in a cycle if:
            # 1. 3 digits are same and
            # 2. Their children is same
            # which can be checked by the value of three digits and the value of
            # the previously disallowed position, called previousPosition
            if temp.value in visitedDict:
                if temp.previousPosition in visitedDict[temp.value]:
                    continue
                else:
                    visitedDict[temp.value].append(temp.previousPosition)
            expandDFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
        else:
            continue

def dfs(startState, endState, forbiddenSet):

    # 1. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandDFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    return traversedList, pathList

def aStar(startState, endState, forbiddenSet):
    #stub
    return [], []

def expandIDS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):
    return [],[],[]

def ids(startState, endState, forbiddenSet):
    #stub
    return [], []

def greedy(startState, endState, forbiddenSet):
    #stub
    return [], []

def hillClimbing(startState, endState, forbiddenSet):
    #stub
    return [], []

if __name__ == '__main__':

    global nodesExpanded
    nodesExpanded = 1
    sys.setrecursionlimit(1500)
    filename, searchStrategy = getArgs()

    # 1. Open up file first and get start, end and forbidden states
    unpack = (open(filename, "r")).read().split("\n")

    # 2. Turn states into int or int array
    with open(filename) as file:
        values = [num.strip() for num in file.readlines()]
    startState, endState = int(values[0]), int(values[1])

    if len(values) >= 3:
        # there are forbidden states, insert them in a list
        forbiddenSetStr = set(values[2].split(','))
    else:
        forbiddenSetStr = set()
    forbiddenSet = [int(num) for num in forbiddenSetStr]
    # 3. According ot the search strategy, call different functions
    strategyDict = {"D": dfs,"B": bfs, "I": ids, "G":greedy, "A": aStar, "H":hillClimbing}
    traversedList, pathList = strategyDict[searchStrategy](startState, endState, forbiddenSet)
    # 4. Print output
    if nodesExpanded < 1000:
        print(','.join([str(num).zfill(3) for num in pathList]))
        print(','.join([str(num).zfill(3) for num in traversedList]))
    else:
        print("No solution found.")
        print(','.join([str(num).zfill(3) for num in traversedList]))

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
global exitRecursion
class Node:
    def __init__(self, value, previousPosition, prevNode):
        self.value = value
        self.previousPosition = previousPosition
        self.prevNode = prevNode
    def setLevel(self, level):
        self.level = level

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

def getChildren(node):
    nodeList = []
    for i in range(6):

        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            continue
        nodeList.append(Node(node.value + getAdditionValue(i), position, node))

    return nodeList

def calculateManhattanHeuristic(previousValue, currentValue):
    return abs(getSpecificDigit(previousValue, 2) - getSpecificDigit(currentValue, 2)) + \
    abs(getSpecificDigit(previousValue, 1) - getSpecificDigit(currentValue, 1)) + \
    abs(getSpecificDigit(previousValue, 0) - getSpecificDigit(currentValue, 0))

def expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):
    global nodesExpanded
    if nodesExpanded > 1000 or endState in traversedList:
        return

    # append to traversed list
    traversedList.append(node.value)
    traversedQueue.append(node)

    # append to visited list
    if (not visitedDict.__contains__(node.value)):
        visitedDict[node.value] = [node.previousPosition]
    else:
        visitedDict[node.value].append(node.previousPosition)

    while traversedQueue:
        temp = traversedQueue.pop(0)

        if(temp.value in forbiddenSet):
            continue
        traversedList.append(temp.value)

        # get the neighbour of this node
        nodeList = getChildren(temp)

        for n in nodeList:
            if (not visitedDict.__contains__(n.value)):
                visitedDict[n.value] = [n.previousPosition]
            elif (n.previousPosition not in visitedDict[n.value]):
                visitedDict[n.value].append(n.previousPosition)
            else:
                continue
            traversedQueue.append(n)
        if (temp.value == endState):
            while(temp.prevNode != None):
                pathList.insert(0,temp.value)
                temp = temp.prevNode
            return

def bfs(startState, endState, forbiddenSet):

    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    pathList.insert(0, node.value)
    return traversedList[1:], pathList

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
            if temp.value in visitedDict:
                if temp.previousPosition in visitedDict[temp.value]:
                    continue
                else:
                    visitedDict[temp.value].append(temp.previousPosition)
            expandDFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)

def dfs(startState, endState, forbiddenSet):

    # 1. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandDFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    return traversedList, pathList

def expandIDS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict, level):
    global nodesExpanded
    global exitRecursion
    if nodesExpanded > 1000 or endState in traversedList or exitRecursion is True:
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

        #nodesExpanded = 1001 # to make it quit
        exitRecursion = True
        return

    # Loop over the 6 possibilities and transformations
    for i in range(6):
        if node.level >= level:
            continue
        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            continue

        # Use the getAdditionValue to add value to the current node and set it as a new node
        if(node.value + getAdditionValue(i) not in forbiddenSet):
            temp = Node(node.value + getAdditionValue(i), position, node)
            temp.setLevel(node.level+1)

            # Check if the number is forbidden
            if temp.value in visitedDict:
                if temp.previousPosition in visitedDict[temp.value]:
                    continue
                else:
                    visitedDict[temp.value].append(temp.previousPosition)
            expandIDS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict, level)

def ids(startState, endState, forbiddenSet):
    # 1. Make first node
    global exitRecursion
    fullTraversedList = []
    level = 0
    while(nodesExpanded < 1000 and fullTraversedList[-1:] != endState and exitRecursion is False):
        node = Node(startState, None, None)
        node.setLevel(0)
        traversedQueue, pathList, traversedList, visitedDict = [], [], [], {}
        expandIDS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict, level)
        for i in range(len(traversedList)):
            fullTraversedList.append(traversedList[i])
        level += 1
    return fullTraversedList, pathList

def getManhattanHeurChildren(node, endState):
    nodeList = []
    sortedNode = []
    for i in range(6):

        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            continue
        nodeList.append(Node(node.value + getAdditionValue(i), position, node))

    # Sort by manhattan heuristic value
    if(len(nodeList) > 0):
        sortedNode.append(nodeList[0])
        for i in range(len(nodeList)):
            val = len(sortedNode)
            for j in range(val):
                if calculateManhattanHeuristic(endState, nodeList[i].value) > \
                        calculateManhattanHeuristic(endState, sortedNode[j].value):
                    sortedNode.insert(j,nodeList[i])
                    break
                elif j == len(sortedNode) - 1:
                    sortedNode.append(nodeList[i])
                    break
    return sortedNode

def expandAStar(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):
    global nodesExpanded
    if nodesExpanded > 1000 or endState in traversedList:
        return

    # append to traversed list
    traversedList.append(node.value)
    traversedQueue.append(node)

    # append to visited list
    if (not visitedDict.__contains__(node.value)):
        visitedDict[node.value] = [node.previousPosition]
    else:
        visitedDict[node.value].append(node.previousPosition)

    while traversedQueue:
        temp = traversedQueue.pop()

        if(temp.value in forbiddenSet):
            continue
        traversedList.append(temp.value)

        # get the neighbour of this node
        nodeList = getManhattanHeurChildren(temp, endState)

        for n in nodeList:
            if (not visitedDict.__contains__(n.value)):
                visitedDict[n.value] = [n.previousPosition]
            elif (n.previousPosition not in visitedDict[n.value]):
                visitedDict[n.value].append(n.previousPosition)
            else:
                continue
            traversedQueue.append(n)
        if (temp.value == endState):
            while(temp.prevNode != None):
                pathList.insert(0,temp.value)
                temp = temp.prevNode
            return

def aStar(startState, endState, forbiddenSet):
    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [], [], []
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandAStar(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    pathList.insert(0, node.value)
    return traversedList[1:], pathList

def getHeurGreedy(node, endState):
    nodeList = []
    sortedNode = []
    for i in range(6):

        position = 2 - int(i / 2)
        constraints = [position == node.previousPosition,
                       getSpecificDigit(node.value, position) == 0 and i % 2 == 0,
                       getSpecificDigit(node.value, position) == 9 and i % 2 != 0]

        # if any constraints are met, skip this loop
        if any(constraints):
            continue
        nodeList.append(Node(node.value + getAdditionValue(i), position, node))

    # Sort by manhattan heuristic value
    if(len(nodeList) > 0):
        sortedNode.append(nodeList[0])
        for i in range(len(nodeList)):
            val = len(sortedNode)
            for j in range(val):
                if calculateManhattanHeuristic(endState, nodeList[i].value) > \
                        calculateManhattanHeuristic(endState, sortedNode[j].value):
                    sortedNode.insert(j,nodeList[i])
                    break
                elif j == len(sortedNode) - 1:
                    sortedNode.append(nodeList[i])
                    break
    return sortedNode

def expandGreedy(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict):
    global nodesExpanded
    if nodesExpanded > 1000 or endState in traversedList:
        return

    # append to traversed list
    traversedList.append(node.value)
    traversedQueue.append(node)

    # append to visited list
    if (not visitedDict.__contains__(node.value)):
        visitedDict[node.value] = [node.previousPosition]
    else:
        visitedDict[node.value].append(node.previousPosition)

    while traversedQueue:
        temp = traversedQueue.pop()

        if(temp.value in forbiddenSet):
            continue
        traversedList.append(temp.value)

        # get the neighbour of this node
        nodeList = getHeurGreedy(temp, endState)

        for n in nodeList:
            if (not visitedDict.__contains__(n.value)):
                visitedDict[n.value] = [n.previousPosition]
            elif (n.previousPosition not in visitedDict[n.value]):
                visitedDict[n.value].append(n.previousPosition)
            else:
                continue
            traversedQueue.append(n)
        if (temp.value == endState):
            while(temp.prevNode != None):
                pathList.insert(0,temp.value)
                temp = temp.prevNode
            return

def greedy(startState, endState, forbiddenSet):
    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [], [], []
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandGreedy(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, visitedDict)
    pathList.insert(0, node.value)
    return traversedList[1:], pathList

def hillClimbing(startState, endState, forbiddenSet):
    #stub
    return [], []

if __name__ == '__main__':

    global nodesExpanded
    global exitRecursion
    nodesExpanded = 1
    exitRecursion = False
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

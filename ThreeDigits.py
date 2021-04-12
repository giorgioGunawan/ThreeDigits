import sys

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
        print("ERROR1")
        exit()

def getAdditionValue(index):
    dict = {0:-100, 1:100, 2:-10, 3:10, 4:-1, 5:1}
    return dict[index]

def bfs(startState, endState, forbiddenSet):
    def expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict):

        # base class for recursion
        traversedList.append(node.value)
        visitedDict[node.value] = node.previousPosition
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
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict)
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
                if (temp.value in visitedDict and visitedDict[temp.value] == temp.previousPosition):
                    continue

                # If its not in a cycle, then add it to the queue
                traversedQueue.append(temp)
                if (i == 5):
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded,visitedDict)
            else:
                if (i == 5):
                    temp = traversedQueue.pop(0)
                    expandBFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded,visitedDict)
                continue

    # 1. Set out iterator to ensure less than 1000 nodes are expanded
    nodesExpanded = 0

    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandBFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict)
    return traversedList, pathList, nodesExpanded

def dfs(startState, endState, forbiddenSet):
    def expandDFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict):

        # Need to complete this too....
        if nodesExpanded > 1000:
            print("more than 1000")
            return

        # Base class for recursion
        traversedList.append(node.value)
        visitedDict[node.value] = node.previousPosition
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
                if(temp.value in visitedDict and visitedDict[temp.value] == temp.previousPosition):
                    continue
                traversedQueue.append(temp)
                return expandDFS(temp, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict)
            else:
                continue

    # 1. Set out iterator to ensure less than 1000 nodes are expanded
    nodesExpanded = 0

    # 2. Make first node
    node = Node(startState, None, None)
    traversedQueue, traversedList, pathList = [],[],[]
    visitedDict = {}

    # 3. Call recursive expand on first node
    expandDFS(node, endState, forbiddenSet, traversedQueue, traversedList, pathList, nodesExpanded, visitedDict)
    return traversedList, pathList, nodesExpanded

def aStar(startState, endState, forbiddenSet):
    #stub
    return None

def ids(startState, endState, forbiddenSet):
    #stub
    return None

def greedy(startState, endState, forbiddenSet):
    #stub
    return None

def hillClimbing(startState, endState, forbiddenSet):
    #stub
    return None

if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    filename, searchStrategy = getArgs()

    # 1. Open up file first and get start, end and forbidden states
    unpack = (open(filename, "r")).read().split("\n")

    # 2. Turn states into int or int array
    if len(unpack) == 2:
        startState, endState = unpack
        startState, endState = int(startState), int(endState)
        forbiddenSet = set()
    elif len(unpack) == 3:
        startState, endState, forbidden = unpack
        startState, endState, forbiddenSet = int(startState), int(endState), set([int(n) for n in forbidden.split(',')])

    # 3. According ot the search strategy, call different functions
    strategyDict = {"D": dfs,"B": bfs, "I": ids, "G":greedy, "A": aStar, "H":hillClimbing}
    traversedList, pathList, nodesExpanded = strategyDict[searchStrategy](startState, endState, forbiddenSet)
    # 4. Print output
    if nodesExpanded < 1000:
        print(','.join([str(num) for num in pathList]))
        print(','.join([str(num) for num in traversedList]))
    else:
        print("No solution found.")
        print(','.join([str(num) for num in traversedList]))

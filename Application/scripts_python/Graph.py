# Python program to print all paths from a source to destination.

from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def printAllPathsUtil(self, u, d, visited, path, paths):
        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)
        # If current vertex is same as destination, then print
        # current path[]

        if len(path) <= 3:  # and len(paths)<=6
            if u == d:
                print(path)
                paths.append(path.copy())
            else:
                # If current vertex is not destination
                # Recur for all the vertices adjacent to this vertex
                for i in self.graph[u]:
                    if not visited[i]:
                        self.printAllPathsUtil(i, d, visited, path, paths)

        # Remove current vertex from path[] and mark it as unvisited

        path.pop()
        visited[u] = False
        return paths

    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):
        paths = []

        # Mark all the vertices as not visited
        visited = [False] * self.V

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        paths = self.printAllPathsUtil(s, d, visited, path, paths)
        return paths

# if __name__ == "__main__":
# Create a graph given in the above diagram
#   g = Graph(4)
#  print(g)
# g.addEdge(0, 1)
# g.addEdge(0, 2)
# g.addEdge(0, 3)
# g.addEdge(2, 0)
# g.addEdge(2, 1)
# g.addEdge(1, 3)

# s = 2;
# d = 3
# print("Following are all different paths from % d to % d :" % (s, d))
# g.printAllPaths(s, d)

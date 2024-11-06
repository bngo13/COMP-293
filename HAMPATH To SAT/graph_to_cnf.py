"""

Goal:
    1) Write a program (python or java or c++) that solves HAMPATH using
       the MiniSAT solver
    2) Input: a graph
    3) Output: corresponding boolean formula that can be fed into MiniSAT


Example

2 3
1 3 4
1 2
2

represents a graph where:

1) Node 1 is connected to nodes 2 and 3
2) Node 2 is connected to nodes 1, 3, and 4
3) Node 3 is connected to nodes 1 and 2
4) Node 4 is connected to nodes 2


"""

import sys

DEBUG = False
NEGATE_SYMBOL = "-"

VAR_NAMES = {}
VAR_COUNT = 0

def varToVarname(var):
    global VAR_COUNT
    if var in VAR_NAMES:
        return str(VAR_NAMES[var])
    else:
        VAR_COUNT += 1
        VAR_NAMES[var] = VAR_COUNT 
        return str(VAR_NAMES[var])

class Graph_to_CNF():
    def __init__(self, input_file):
        # read in the data from the file and create a
        # graph representation
        self.graph = {}
        i = 1
        with open(input_file, "r") as f:
            for line in f:
                data = line.split()
                # convert string to numerical value
                for j in range(0, len(data)):
                    data[j] = int(data[j])

                self.graph[i] = data
                i = i + 1
        if DEBUG:
            print("Graph: \n{}\n".format(self.graph))
    
        # initialize clause variables
        self.clauses = []
        self.keyNum = len(self.graph)


    def generatecnf(self):
        self.generateReq1()
        self.generateReq2()
        self.generateReq3()
        self.generateReq4()
        self.generateReq5()

        if DEBUG:
            print(self.clauses)

    def generateReq1(self):
        # Each node j must appear in the path.
        for i in range(1, self.keyNum + 1):
            clause = ""
            for j in range(1, self.keyNum + 1):
                clause += varToVarname(f"{j}{i}")
                clause += " "
            self.clauses.append(clause.strip())

    def generateReq2(self):
        # No node j appears twice in the path.
        for i in range(1, self.keyNum + 1):
            for k in range(i + 1, self.keyNum + 1):
                for j in range(1, self.keyNum + 1):
                    clause1 = varToVarname(f"{i}{j}")
                    clause2 = varToVarname(f"{k}{j}")
                    self.clauses.append(f"{NEGATE_SYMBOL}{clause1} {NEGATE_SYMBOL}{clause2}")

    def generateReq3(self):
        # Every position i on the path must be occupied.
        for i in range(1, self.keyNum + 1):
            clause = ""
            for j in range(1, self.keyNum + 1):
                clause += varToVarname(f"{i}{j}")
                clause += " "
            self.clauses.append(clause.strip())

    def generateReq4(self):
        # No two nodes j and k occupy the same position in the path.
        for j in range(1, self.keyNum + 1):
            for k in range(j + 1, self.keyNum + 1):
                for i in range(1, self.keyNum + 1):
                    clause1 = varToVarname(f"{i}{j}")
                    clause2 = varToVarname(f"{i}{k}")
                    self.clauses.append(f"{NEGATE_SYMBOL}{clause1} {NEGATE_SYMBOL}{clause2}")

    def generateReq5(self):
        # Nonadjacent nodes i and j cannot be adjacent in the path
        for k in range(1, self.keyNum):
            for i in range(1, self.keyNum + 1):
                for j in range(1, self.keyNum + 1):
                    if i not in self.graph[j] and i != j:
                        clause1 = varToVarname(f"{k}{i}")
                        clause2 = varToVarname(f"{k + 1}{j}")
                        self.clauses.append(f"{NEGATE_SYMBOL}{clause1} {NEGATE_SYMBOL}{clause2}")

    def printCNF(self):
        output = ""
        output += f"p cnf {len(self.graph.keys()) ** 2} {len(self.clauses)}\n"
        for clause in self.clauses:
            output += f"{clause} 0\n"
        
        out_file = open("output.txt", 'w')
        out_file.write(output)

if __name__=="__main__":
    # check for the number of arguments
    if len(sys.argv) == 1:
        print("Usage: {} [INPUT_FILE]".format(sys.argv[0]))
        exit(0)

    graph_to_cnf = Graph_to_CNF(sys.argv[1])

    graph_to_cnf.generatecnf()

    graph_to_cnf.printCNF()

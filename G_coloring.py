
import cplex
import math
import sys

if len(sys.argv) < 2:
	print ("Usage: python G_coloring.py datafile.dat")
	sys.exit(1)

def read_data(filename):
	with open(filename) as f:
		data = f.read().split()
		floats = []
		for elem in data:
			try:
	        		floats.append(float(elem))
			except ValueError:
				pass
	return(floats)
	

file_it = read_data(sys.argv[1])


n = int(file_it[0])   #Number of nodes
del file_it[0]

e = int(file_it[0])  #Number of edges
del file_it[0]

edge = []   
while len(file_it) > 0:
	edge.append([])
	edge[len(edge)-1].append(int(file_it[0])-1)
	del file_it[0]
	edge[len(edge)-1].append(int(file_it[0])-1)
	del file_it[0]

if len(edge) != e:
	print("number of edges is not as required")
	exit()


def define_problem(prob):
	prob.set_problem_name ("Graph_coloring")
	prob.objective.set_sense(prob.objective.sense.minimize)

	for i in range(n):
		prob.variables.add(lb = [0]*n,
				ub = [1]*n,
				types = ["B"]*n)

	prob.variables.add(obj=[1.0]*n,lb = [0]*n,
			ub = [1]*n,
			types = ["B"]*n)

	
	cons = [ [ [i*n + j for j in range(n)], [1 for j in range(n)] ] for i in range(n)]
	prob.linear_constraints.add(lin_expr=cons, senses = ["E"]*n, rhs = [1 for i in range(n)])
	
	cons = [ [ [i*n+j, (n*n)+j], [1,-1] ] for j in range(n) for i in range(n)]
	prob.linear_constraints.add(lin_expr=cons, senses = ["L"]*n*n, rhs = [0 for j in range(n) for i in range(n)])

	for i in range(e):
		for k in range(n):
			cons = [ [ [ edge[i][0]*n+k, edge[i][1]*n+k ] , [1 for j in range(2)] ] ]
			prob.linear_constraints.add(lin_expr=cons, senses = ["L"], rhs = [1])
			
def Graph_coloring():
	prob = cplex.Cplex()
	define_problem(prob)
	prob.solve()
	sol = prob.solution

	print(sol.status[sol.get_status()])
	print("Number of node in graph =",n)
	print("Number of edges in graph =",e)
	print("Number of colors used = ", int(sol.get_objective_value()))
	prob.write("Graph_coloring.lp")

Graph_coloring()	




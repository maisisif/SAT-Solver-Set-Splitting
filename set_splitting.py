import subprocess
from argparse import ArgumentParser


# Working principle of the code:
# 1) read the instance from file
# 2) translate it into SAT formula in DIMACS CNF format   
# 3) save CNF to formula.cnf
# 4) call glucose SAT solver on formula.cnf
# 5) based on the results, check which variables are pos or neg
#  and decide which will go to S1 and S2
# 6) print the output

def load_instance(input_file_name):
    #read the input instance
    #format of the file:
    #first line, first element is n = num of elements
    #first line, second element is m = num of sets (each set on a new line and space between the elements)

    #read nonempty and noncomment lines(optional step, can be ignored)
    with open(input_file_name, "r") as file:
        lines =  [ 
            line.strip()
            for line in file 
            if line.strip() and not  line.startswith("#")
        ]

    
    #take the n and m from first line
    first_line = lines[0].split()
    n = int(first_line[0])
    m = int(first_line[1])

    #read all sets(skip the first line)
    sets = []
    for line in lines[1:]:
        subset = list(map(int, line.split()))
        sets.append(subset)

    #check
    if len(sets) != m:
        print("number of sets does not match given m")
        exit(1)

    return n, sets


def encode(instance):
    #given instance, create a CNF formula
    #variables:  x_i is used when element is in S1 
    #           ¬x_i is used when element is in S2
    #for each input set Y the goal is to show that it is not fully in S1 or S2
    #for that it has to be: 
    #   forbid all in S1: 
    #       if every element of X is in S1, then x_i = true for all i in X 
    #       forbid it by adding the clause (¬x_1 v ¬x_2 v ... ¬x_i)
    #   forbid all in S2:
    #       if every element of X is in S2, then x_i = false for all i in X 
    #       forbid it by adding the clause (x_1 v x_2 v ... x_i)

    #obtained in the end: 
    # 2 clauses for each set 
    # total num of variables is equal to total num of elements
    #also return the total number of variables used   

    n, sets = instance
    cnf = []
    total_vars = n 
     

    #forbidding step
    for subset in sets:
        cnf.append([-var for var in subset])
        cnf.append([+var for var in subset])

    
    return cnf, total_vars


def call_solver(cnf, total_vars, output_name, solver_name, verbosity):
    # print the CNF into output_name in DIMACS format
    with open(output_name, "w") as file:
        file.write(f"p cnf {total_vars} {len(cnf)}\n")
        for clause in cnf:
            file.write(" ".join(str(l) for l in clause) + " 0\n")

    #call solver and return  result
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name], stdout=subprocess.PIPE)


def print_result(result):
    #print the output of SAT solver
    out_str = result.stdout.decode("utf-8")  
    for line in out_str.split('\n'): 
        print(line)  


    #check the result
    if result.returncode == 20: #UNSAT for 20
        return

    if result.returncode != 10: #SAT for 10
        return

    #parse the model from the solver output
    #model lines begin using 'v' and contain the literals until 0  
    model = []
    for line in out_str.split("\n"): 
        line =line.strip()
        if line.startswith("v"): 
            parts = line.split()
            #remove v
            parts.remove("v") 
            model.extend(int(v) for v in parts)

    #remove 0
    if 0 in model:
        model.remove(0)


    S1 = []
    S2 = []

    #if literal is positive then in S1 
    #if literal is negative then in S2
    max_var = max(abs(v) for v in model)
    assigned_values = set(model)
    for i in range(1, max_var + 1):  
        if i in assigned_values:
            S1.append(i) 
        else:
            S2.append(i) 

    print()
    print("##################################################################")
    print("###########[ Human readable result of Set Splitting ]#############")
    print("##################################################################")
    print()



    print("S1 =", S1)
    print("S2 =", S2)




if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="instances/small-sat.in",
        type=str,
        help=(
            "The instance file."
        ),
    )

    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format  (i.e. the CNF formula)."
        ),
    )

    parser.add_argument(
        "-s",
        "--solver",
        default="glucose",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )

    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )

    args = parser.parse_args()

    # get the input instance
    instance = load_instance(args.input)

    # encode the problem to create CNF formula
    cnf, total_vars = encode(instance)

    # call the SAT solver and get the result
    result = call_solver(cnf, total_vars, args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result)

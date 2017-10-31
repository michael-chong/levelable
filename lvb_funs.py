# Convenience functions for levelable project

def testing():
    print "it works!"

##########################################################################################
# g_read()
# If given a string, return the graph associated with that graph6 string
# Otherwise return the same object
def g_read(obj):
    if isinstance(obj, basestring):
        g = Graph()
        from_graph6(g, obj)
        return g

    elif isinstance(obj, sage.graphs.graph.Graph):
        return obj
    else:
        print "Not given a graph"
        return "NA"


##########################################################################################
# is_levelable()
# Check whether a graph is levelable. Takes either a graph6 string or graph object.
# If verbose = True, print the associated data with that graph
def is_levelable(obj, verbose = False):
    g = g_read(obj)
    indSets = IndependentSets(g, maximal = True)
    t = len(list(indSets))

    # Grab the number of vertices
    n = len(g.vertices())

    # Prepare matrices
    A = np.zeros((t-1, n))
    B = np.zeros((t-1, 1))

    # Iterate through all the facets of the independence complex
    for j in range(0,t-1):

        # Grab facet j
        Fj = list(indSets)[j]

        # Grab facet j + 1
        Fj1 = list(indSets)[j+1]


        # Iterate through every vertex of the facet j
        for k in range(0, len(Fj)):

            # Add 1 to these spots in the matrix
            A[j, Fj[k]] = A[j, Fj[k]] + 1

        # Iterate through every vertex of the facet j + 1
        for k in range(0, len(Fj1)):

            # Subtract 1 to these spots in the matrix
            A[j, Fj1[k]] = A[j, Fj1[k]] - 1

        # Other side of the equation - set the j-th entry
        B[j, 0] = len(Fj) - len(Fj1)

    p = MixedIntegerLinearProgram(maximization = False, solver = "GLPK")
    x = p.new_variable()

    for l in range(n):
        p.set_min(x[l], 2)

    for l in range(t-1):
        # Add a constraint according to the i^th equation
        p.add_constraint(sum(A[l,j]*x[j] for j in range(n)) == B[l])

    try:
        # Print data if verbose
        if (verbose):

            g.show()
            print g.graph6_string()
            print "Independent Sets"
            print list(indSets)

            print
            print "Matrix A"
            print A

            print
            print "B"
            print B

        # Try solving (tries to minimize by default)
        p.solve()

    except:

        if (verbose):
            print
            print "No solution found"
        return False
    else:

        # Get solution
        s = p.get_values([x[r] for r in range(n)])

        # Double check that the solution works
        if np.array_equal(np.matrix(np.dot(A,s)), transpose(B)):

            if (verbose):
                print
                print "Solution"
                print s

            return True

        else:

            # If the solution doesn't work, try to get a solution from maximzation instead
            try:
                p.solve(maximization = True)

            except:
                if (verbose):
                    print
                    print "No solution found (maximzation step necessary)"
                return False

            else:
                print
                print "Solution"
                print s
                return True

##################################################################################################
# g6_show()
# Show a graph from a graph6 string
def g6_show(string):
    g = Graph()
    from_graph6(g, string)
    g.show()

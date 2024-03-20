# fpt algorithms are ones which, when a certain input parameter is fixed, have a "tractable" runtime complexity
# (with respect to a more usual parameter e.g. graph node count).
# for example, due to Ramsey's Theorem, in a graph with n vertices one can always find a k-sized independent set
# or a k-sized clique in constant time, when n is bigger than 4^(k-1) (or, as remarkably discovered in 2023 O(3.998^k))

import Graphs


def ramsey_algorithm(k: int, g: Graphs.Graph):
    # executes the algorithm used in the standard upper-bound proof of the Ramsey Numbers
    # returns a k-list of vertices which is either an independent set or a clique
    # requires the graph to be of size at least 4^k

    vertices = g.vertices
    n = len(vertices)

    if n < 4 ** (k-1) and False:
        raise Exception('ramsey algorithm requires an input graph of size at least 4^k.'
                        'Given graph was size {}'.format(n))
    else:
        independent_set = []
        clique = []
        i = 0

        while not (len(independent_set) == k or len(clique) == k):
            i += 1
            pivot = vertices.pop()
            # check if pivot has enough neighbours to continue algorithm looking for a clique
            # in this sense, a clique is a greedily favoured outcome

            if g.degree(pivot) >= 4 ^ (k-i):
                # if pivot has sufficient degree, add pivot to clique and restrict vertex set to neighbourhood

                clique.append(pivot)
                vertices = vertices.intersection(g.neighbourhood(pivot))

            else:
                # otherwise, add pivot to independent set and remove neighbourhood from active vertices
                independent_set.append(pivot)
                vertices = vertices - g.neighbourhood(pivot)
        else:
            if len(independent_set) == k:
                return independent_set
            else:
                return clique

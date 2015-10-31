__author__ = 'FAMILY'
import itertools


def generate(type, length, max_movex, max_movey, max_offset, max_startx, max_starty):
    """
    generates all of the combinations of the parameters for graph.draw_layers within the limits of these parameters:
        type: "triangular" or "squared"
        length: length of the chains inputed as [length of chain1,length of chain2,length of chain3]
        max_movex: max movex that will be tested
        max_movey: max movey that will be tested
        max_offset: max delta_offset that will be tested
        max_startx: max startx that will be tested
        max_starty: max starty that will be tested
        graph_size:
    """
    if type == "squared":
        for combination in itertools.product(range(-1,2), repeat=length-1):
            str1=list(map(int, combination))
            for combination2 in itertools.product(range(-1,2), repeat=length-1):
                str2=list(map(int, combination2))
                for i in range(1,max_movex+1):
                    for j in range(1,max_movey+1):
                        for k in range(1,max_movex+1):
                            for l in range(1,max_movey+1):
                                for m in range(max_startx+1):
                                    for n in range(max_starty+1):
                                        for o in range(1,4):
                                            for p in range(max_offset+1):
                                                for r in range(max_offset+1):
                                                    if p>=i or r>=k:
                                                        pass
                                                    else:
                                                        yield(str1, i, j, p, 0, str2, k, l, r, o, m, n)
    elif type == "triangular":
        pass

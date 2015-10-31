__author__ = 'FAMILY'

from classes.shape import Shape
from classes.graph_draw import GraphDraw

class Graph(object):
    def __init__(self, graph_sizex, graph_sizey, chain_length, graph_type):

        self.graph_sizex = graph_sizex  # number of nodes in a row
        self.graph_sizey = graph_sizey  # number of rows
        self.chain_length = chain_length  # number of segments in each chain !!
        self.graph_type = graph_type  # geometry - "triangular" or "squared"
        self.graph_dict = self.make_square_graph(self.graph_sizex,
                                                 self.graph_sizey)  # dictionary from which the graph is built
        self.edge_list = self.generate_edges()  # list of graph edges
        self.node_list = self.generate_nodes()  # list of graph nodes
        self.shape_list = []  # list of all instances of Shape placed in the graph
        self.matrix = self.generate_matrix(self.chain_length[0], self.chain_length[1],
                                           self.chain_length[2])  # connection matrix
        self.alphabet = self.generate_alphabet(self.chain_length[0], self.chain_length[1],
                                               self.chain_length[2])  # alphabets of shapes in each layer
        self.stable = True
        self.graph_draw = GraphDraw(self, 1000, self.graph_sizex)  # GraphDraw used for drawing the graph

        self.matrix_list = []  # list of stable combinations
        self.found = 0  # number of found stable combinations

    def make_square_graph(self, sizex, sizey):
        # generates the connections of the graph
        # squared: each node except the outermost has 4 connections
        # triangular: each node except the outermost has 6 connections
        dicti = {i: [] for i in range(sizex * sizey)}
        for i in dicti:
            if self.graph_type == "triangular":
                if (i // 10) % 2 == 0:
                    row_switch = 1
                    arow_switch = 0
                else:
                    row_switch = 0
                    arow_switch = 1
                if not((int(i) % sizex) - 1 < 0):
                    dicti[i].append(int(i) - 1)
                if not (int(i) - sizex < 0):
                    dicti[i].append(int(i) - sizex - row_switch)
                if not(int(i) + 1 >= sizex * (i // sizex + 1)):
                    dicti[i].append(int(i) + 1)
                if not(int(i) + sizex >= sizey*sizex):
                    dicti[i].append(int(i) + sizex + arow_switch)
                if not i % sizex - 1 < 0 and not i + sizex > sizex * sizey:
                    dicti[i].append(int(i) + sizex - row_switch)
                if not i % sizex + 1 >= sizex and not i - sizex < 0:
                    dicti[i].append(int(i) - sizex + arow_switch)
            elif self.graph_type == "squared":
                if not ((int(i) % sizex) - 1 < 0):
                    dicti[i].append(int(i) - 1)
                if not (int(i) - sizex < 0):
                    dicti[i].append(int(i) - sizex)
                if not (int(i) + 1 >= sizex * (i // sizex + 1)):
                    dicti[i].append(int(i) + 1)
                if not (int(i) + sizex >= sizey * sizex):
                    dicti[i].append(int(i) + sizex)
        return dicti

    def generate_nodes(self):
        # each node is listed as [index of node. number of endings in each node]
        nodes = []
        for node in self.graph_dict:
            nodes.append([node, 0])
        return nodes

    def generate_edges(self):
        """
        each edge is listed as [index of first node,
                                index of second node,
                                number of segments placed on the edge,
                                position in shape_list of the last shape with a segment placed on the edge,
                                letter of last segment placed on the edge
                                orientation of last segment placed on the edge]
        """
        edges = []
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                if [neighbour, node, 0, 0, 0, 0] not in edges:
                    edges.append([node, neighbour, 0, 0, 0, 0])
        return edges

    def generate_matrix(self, length_f, length_s, length_t):
        # generates a list of matrixes of connections
        """
            example: we have chain 1 with segments abc and chain 2 with segments def. Their connection matrix will be:
              d e f D E F
            a 0 0 0 0 0 0
            b 0 0 0 0 0 0
            c 0 0 0 0 0 0
            with a 1 in the column with lowercase letters meaning a parallel connection and uppercase letters meaning an
            antiparallel connection. In our solution we regulated that there is to be only one 1 in each row and column,
            since more than one probably means an unstable lattice. The individual matrices for three different chains
            are the same, except that there is one for every pair combination
        """
        if length_t == 0:
            matrix = [[[0 for i in range(length_s * 2)] for j in range(length_f)]]
        else:
            matrix = [[[0 for i in range(length_s * 2)] for j in range(length_f)],
                      [[0 for i in range(length_t * 2)] for j in range(length_f)],
                      [[0 for i in range(length_t * 2)] for j in range(length_s)]]
        return matrix

    def generate_alphabet(self,length_f,length_s,length_t):
        # each of the chains gets their unique segment names
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        f_alphabet = alphabet[:length_f]
        s_alphabet = alphabet[length_f:length_s + length_f] + alphabet[length_f:length_s + length_f].upper()
        t_alphabet = (alphabet[length_f + length_s:length_f + length_s + length_t] +
                      alphabet[length_f + length_s:length_f + length_s + length_t].upper())
        return [f_alphabet,s_alphabet,t_alphabet]
    def shape_generator(self,shape,movex,movey,delta_offset,orientation,startx=0,starty=0,first=1):
        """
            generates a layer of shapes with the starting points being x+y*self.graph_sizex
            where x=xcount*movex + startx + offset and y=ycount*movey + starty with these parameters:
                movex - nodes between each start point in a row
                movey - nodes between each rows
                delta_offset - difference in offset for each row
                startx - x of the first starting point others are relative to
                starty - y of the first starting point others are relative to
                shape - defines the braking of the chain in each node
                first - specifies which layer do the shapes belong to
            does not generate the shapes that don't have all the segments on the connections of the graph
        """
        offset=0
        xcount = 0
        ycount = 0
        while ycount * movey + starty < self.graph_sizey:
            if not self.check_if_stable():
                return
            foo = Shape(self,
                        shape,
                        self.graph_sizex * (ycount * movey) + starty * self.graph_sizex + (xcount * movex) + startx + offset,
                        orientation,
                        first)
            size = foo.get_size()
            xcount=0
            if foo.start_point + (size[2] * self.graph_sizex) + size[0] + offset > self.graph_sizey * self.graph_sizex:
                break
            elif foo.start_point + (size[3] * self.graph_sizex) - size[1] < 0:
                pass
            else:
                while xcount * movex + startx + offset < self.graph_sizex:
                    foo = Shape(self,shape,self.graph_sizex * (ycount * movey + starty)+ xcount * movex + startx + offset,orientation,first)
                    size=foo.get_size()
                    if (foo.start_point + size[0]) // self.graph_sizex > foo.start_point // self.graph_sizex:
                        break
                    xcount+=1
                    yield foo
            ycount += 1
            if offset + delta_offset >= movex:
                offset += delta_offset - movex
            else:
                offset += delta_offset

    def draw_layer(self,shape,movex,movey,delta_offset,orientation,startx=0,starty=0,first=1):
        #draws every shape that the generator with the same parameters as the function yields
        for foo in self.shape_generator(shape,movex,movey,delta_offset,orientation,startx,starty,first):
            self.shape_list.append(foo)
            self.graph_draw.shape_queue.append(foo)
            self.draw_shape(foo)
        self.draw()

    def draw_layers(self, shape1, movex1, movey1,delta_offset1, orientation1,
                    shape2, movex2, movey2,delta_offset2, orientation2, startx2, starty2,
                    shape3=None, movex3=None, movey3=None,delta_offset3=None, orientation3=None, startx3=None, starty3=None):
        # draws up to three different layers of shapes, each with different parameters
        first_generator = self.shape_generator(shape1, movex1, movey1,delta_offset1, orientation1)
        second_generator = self.shape_generator(shape2, movex2, movey2, delta_offset2, orientation2, startx2, starty2, 2)
        if shape3:
            third_generator = self.shape_generator(shape3, movex3, movey3, delta_offset3, orientation3, startx3, starty3, 3)

        generators = [1,1,1]
        while generators != [0,0,0]:
            try:
                foo = next(first_generator)
                self.shape_list.append(foo)
                self.draw_shape(foo)
                if not self.stable:
                    self.stable = True
                    break
            except StopIteration:
                generators[0] = 0

            try:
                foo = next(second_generator)
                self.shape_list.append(foo)
                self.draw_shape(foo)
                if not self.stable:
                    self.stable = True
                    break
            except StopIteration:
                generators[1] = 0

            if shape3:
                try:
                    foo = next(third_generator)
                    self.shape_list.append(foo)
                    self.draw_shape(foo)
                    if not self.stable:
                        self.stable = True
                        break
                except StopIteration:
                    generators[2] = 0
            else:
                generators[2] = 0
        # if it finds the layers stable and the check function returns True, it adds the matrix and the parameters to matrix_list.
        if self.check(33, 66) and self.stable == True:
            self.matrix_list.append(
                [self.matrix, shape1, movex1, movey1, delta_offset1, orientation1, shape2, movex2, movey2,delta_offset2, orientation2, startx2,
                 starty2, shape3, movex3, movey3,delta_offset3, orientation3, startx3, starty3])
            self.found += 1

        # resets to the original graph state
        self.raise_not_stable()
        self.stable = True

    def make_connection(self, point1, point2, letter=None, orientation=None):
        # makes a connection between point1 and point2 by changing the properties of the edge in edge_list
        for i in self.edge_list:
            if (i[0] == point1 and i[1] == point2) or (i[0] == point2 and i[1] == point1):
                i[2] += 1
                i[3] = len(self.shape_list)
                if letter:
                    # if it is the first segment placed on the edge, the properties are saved
                    if i[4] == 0:
                        i[4] = letter
                        i[5] = orientation
                    # if it there are more than two segments on the edge, the graph combination is declared as unstable
                    elif i[4] == "checked":
                        self.raise_not_stable()
                        return
                    # if there is only one segement on the edge, it checks the connection and fills the proper spot in the matrix
                    else:
                        second_letter = i[4]
                        if self.alphabet[0].find(letter) != -1:
                            alphabet = 0
                        elif self.alphabet[1].find(letter) != -1:
                            alphabet = 1
                        elif self.alphabet[2].find(letter) != -1:
                            alphabet = 2

                        if self.alphabet[0].find(i[4]) != -1:
                            second_alphabet = 0
                        elif self.alphabet[1].find(i[4]) != -1:
                            second_alphabet = 1
                        elif self.alphabet[2].find(i[4]) != -1:
                            second_alphabet = 2
                        if alphabet > second_alphabet:
                            letter, second_letter = second_letter, letter
                            alphabet, second_alphabet = second_alphabet, alphabet
                        elif alphabet == second_alphabet:
                            self.raise_not_stable()
                            # print("not stable")
                            return
                        if 1 in self.matrix[alphabet + second_alphabet - 1][self.alphabet[alphabet].index(letter)]:
                            if i[5] != orientation:
                                if self.matrix[alphabet + second_alphabet - 1][self.alphabet[alphabet].index(letter)][
                                            self.alphabet[second_alphabet].index(second_letter) + len(
                                        self.alphabet[second_alphabet]) // 2] == 1:
                                    pass
                                else:
                                    self.raise_not_stable()
                                    # print("not stable")
                                    return
                            else:
                                if (self.matrix[alphabet + second_alphabet - 1][self.alphabet[alphabet].index(letter)]
                                    [self.alphabet[second_alphabet].index(second_letter)] == 1):
                                    pass
                                else:
                                    self.raise_not_stable()
                                    # print("not stable")
                                    return
                        else:
                            if i[5] != orientation:
                                self.matrix[alphabet + second_alphabet - 1][self.alphabet[alphabet].index(letter)][
                                    self.alphabet[second_alphabet].index(second_letter) + len(
                                        self.alphabet[second_alphabet]) // 2] = 1
                            else:
                                self.matrix[alphabet + second_alphabet - 1][self.alphabet[alphabet].index(letter)][
                                    self.alphabet[second_alphabet].index(second_letter)] = 1
                        i[4] = "checked"

    def raise_not_stable(self):
        # resets the graph to the default and changes self.stable to false
        self.edge_list = []
        self.shape_list = []
        self.node_list = self.generate_nodes()
        self.edge_list = self.generate_edges()
        self.matrix = self.generate_matrix(self.chain_length[0], self.chain_length[1], self.chain_length[2])
        self.graph_draw = GraphDraw(self, 750, self.graph_sizex)

        self.stable = False

    def check(self, first_point, second_point):
        # checks a square within the graph with opposite corners being first_point and second_point.
        # if all the edges within the square are filled with exactly two segments. If they are, it returns true, meaning that the lattice is stable
        for i in self.edge_list:
            if (i[0] % self.graph_sizex >= first_point % self.graph_sizex and
                            i[0] % self.graph_sizex <= second_point % self.graph_sizex and
                            i[1] % self.graph_sizex >= first_point % self.graph_sizex and
                            i[1] % self.graph_sizex <= second_point % self.graph_sizex and
                        i[0] >= first_point and i[1] >= first_point and
                        i[0] <= second_point and i[1] <= second_point):
                if i[2] == 2:
                    pass
                else:
                    return False
        return True

    def check_if_stable(self):
        if not self.stable:
            return False
        else:
            return True

    def draw_shape(self,shape):
        # places all of the segments in an instance of Shape on the connections of the graph using make_connection.
        _start_point = shape.start_point
        _orientation = shape.orientation
        count = 0

        if shape.first == 1:
            alphabet = 0
        elif shape.first == 2:
            alphabet = 1
        else:
            alphabet = 2

        # checks the number of endings in each node, if it exceeds 2, it declares the lattice as unstable
        self.node_list[_start_point][1] += 1
        if self.node_list[_start_point][1] > 2:
            self.raise_not_stable()
            # print("not stable")
            return
        if self.graph_type == 'triangular':
            if _start_point // 10 % 2 == 0:
                row_switch = 1
                arow_switch = 0
            else:
                row_switch = 0
                arow_switch = 1

            if _orientation == 0:
                self.make_connection(_start_point,_start_point + 1,self.alphabet[alphabet][count],_orientation)
                _start_point += 1
            elif _orientation == 1:
                self.make_connection(_start_point,_start_point + self.graph_sizex + arow_switch,self.alphabet[alphabet][count], _orientation)
                _start_point = _start_point + self.graph_sizex + arow_switch
            elif _orientation == 2:
                self.make_connection(_start_point,_start_point + self.graph_sizex - row_switch,self.alphabet[alphabet][count], _orientation)
                _start_point += self.graph_sizex - row_switch
            elif _orientation == 3:
                self.make_connection(_start_point,_start_point - 1,self.alphabet[alphabet][count], _orientation)
                _start_point -= 1
            elif _orientation == 4:
                self.make_connection(_start_point,_start_point - self.graph_sizex - row_switch,self.alphabet[alphabet][count], _orientation)
                _start_point = _start_point - self.graph_sizex - row_switch
            elif _orientation == 5:
                self.make_connection(_start_point,_start_point - self.graph_sizex + arow_switch,self.alphabet[alphabet][count], _orientation)
                _start_point += -self.graph_sizex + arow_switch
            count += 1


            if not self.check_if_stable():
                return

            for i in shape.shape:
                _orientation += i
                if _orientation < 0:
                    _orientation += 6
                if _orientation >= 6:
                    _orientation -= 6
                if (_start_point // 10) % 2 == 0:
                    row_switch = 1
                    arow_switch = 0
                else:
                    row_switch = 0
                    arow_switch = 1
                if _orientation == 0:
                    self.make_connection(_start_point,_start_point + 1,self.alphabet[alphabet][count],_orientation)
                    _start_point += 1
                elif _orientation == 1:
                    self.make_connection(_start_point,_start_point + self.graph_sizex + arow_switch,self.alphabet[alphabet][count],_orientation)
                    _start_point = _start_point + self.graph_sizex + arow_switch
                elif _orientation == 2:
                    self.make_connection(_start_point,_start_point + self.graph_sizex - row_switch,self.alphabet[alphabet][count],_orientation)
                    _start_point += self.graph_sizex - row_switch
                elif _orientation == 3:
                    self.make_connection(_start_point,_start_point - 1,self.alphabet[alphabet][count],_orientation)
                    _start_point -= 1
                elif _orientation == 4:
                    self.make_connection(_start_point,_start_point-self.graph_sizex - row_switch,self.alphabet[alphabet][count],_orientation)
                    _start_point = _start_point - self.graph_sizex - row_switch
                elif _orientation == 5:
                    self.make_connection(_start_point,_start_point - self.graph_sizex + arow_switch,self.alphabet[alphabet][count],_orientation)
                    _start_point += -self.graph_sizex + arow_switch

                count += 1
                if not self.check_if_stable():
                    return
        elif self.graph_type == 'squared':
            if _orientation == 0:
                self.make_connection(_start_point, _start_point + 1, self.alphabet[alphabet][count], _orientation)
                _start_point += 1
            elif _orientation == 1:
                self.make_connection(_start_point, _start_point + self.graph_sizex, self.alphabet[alphabet][count],
                                     _orientation)
                _start_point = _start_point + self.graph_sizex
            elif _orientation == 2:
                self.make_connection(_start_point, _start_point - 1, self.alphabet[alphabet][count], _orientation)
                _start_point -= 1
            elif _orientation == 3:
                self.make_connection(_start_point, _start_point - self.graph_sizex, self.alphabet[alphabet][count],
                                     _orientation)
                _start_point = _start_point - self.graph_sizex
            count += 1

            if not self.check_if_stable():
                return

            for i in shape.shape:
                if i == -1:
                    _orientation -= 1
                    if _orientation < 0:
                        _orientation += 4
                elif i == 1:
                    _orientation += 1
                    if _orientation >= 4:
                        _orientation -= 4

                if _orientation == 0:
                    self.make_connection(_start_point, _start_point + 1, self.alphabet[alphabet][count], _orientation)
                    _start_point += 1
                elif _orientation == 1:
                    self.make_connection(_start_point, _start_point + self.graph_sizex, self.alphabet[alphabet][count],
                                         _orientation)
                    _start_point = _start_point + self.graph_sizex
                elif _orientation == 2:
                    self.make_connection(_start_point, _start_point - 1, self.alphabet[alphabet][count], _orientation)
                    _start_point -= 1
                elif _orientation == 3:
                    self.make_connection(_start_point, _start_point - self.graph_sizex, self.alphabet[alphabet][count],
                                         _orientation)
                    _start_point = _start_point - self.graph_sizex
                count += 1
                if not self.check_if_stable():
                    return

        self.node_list[_start_point][1] += 1
        if self.node_list[_start_point][1] > 2:
            self.raise_not_stable()
            return
        self.shape_list.append(shape)
        self.graph_draw.shape_queue.append(shape)

    def draw(self):
        # draws the current graph situation using the Graph_draw class.
        self.graph_draw.draw()


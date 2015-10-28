__author__ = 'FAMILY'
import time

from classes.shape import Shape
from classes.graph_draw import GraphDraw

class Graph(object):
    def __init__(self, graph_sizex, graph_sizey, chain_length, type, *args, **kwargs):

        self.graph_sizex = graph_sizex
        self.graph_sizey = graph_sizey
        self.chain_length = chain_length
        self.type = type
        self.graph_dict = self.make_square_graph(self.graph_sizex, self.graph_sizey)
        self.edge_list = []
        self.node_list = []

        self.__generate_edges()

        self.shape_list = []

        self.matrix = self.generate_matrix(self.chain_length,self.chain_length,self.chain_length)
        self.alphabet = self.generate_alphabet(self.chain_length,self.chain_length,self.chain_length)

        self.matrix_list = []
        self.stable = True
        self.graph_draw = GraphDraw(self,1000,self.graph_sizex)

        # jut for testing
        self.found=0
    def make_square_graph(self, sizex, sizey):
        dicti = {i: [] for i in range(sizex * sizey)}
        for i in dicti:
            if self.type == "triangular":
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
            elif self.type == "squared":
                if not ((int(i) % sizex) - 1 < 0):
                    dicti[i].append(int(i) - 1)
                if not (int(i) - sizex < 0):
                    dicti[i].append(int(i) - sizex)
                if not (int(i) + 1 >= sizex * (i // sizex + 1)):
                    dicti[i].append(int(i) + 1)
                if not (int(i) + sizex >= sizey * sizex):
                    dicti[i].append(int(i) + sizex)
        return dicti
    def generate_matrix(self,length_f,length_s, length_t):
        matrix = [[[0 for i in range(length_s*2)] for j in range(length_f)],
                  [[0 for i in range(length_t*2)] for j in range(length_f)],
                  [[0 for i in range(length_t*2)] for j in range(length_s)]]
        return matrix
    def generate_alphabet(self,length_f,length_s,length_t):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        f_alphabet = alphabet[:length_f]
        s_alphabet = alphabet[length_f:length_s + length_f] + alphabet[length_f:length_s + length_f].upper()
        t_alphabet = (alphabet[length_f + length_s:length_f + length_s + length_t] +
                      alphabet[length_f + length_s:length_f + length_s + length_t].upper())
        return [f_alphabet,s_alphabet,t_alphabet]
    def shape_generator(self,shape,movex,movey,delta_offset,orientation,startx=0,starty=0,first=1):
        offset=0
        xcount = 0
        ycount = 0
        foo = Shape(self,
                    shape,
                    self.graph_sizex * (ycount * movey) + starty * self.graph_sizex + (xcount * movex) + startx,
                    orientation,
                    first)
        size = foo.get_size()
        while ycount * movey + starty < self.graph_sizey:
            if not self.check_if_stable():
                return
            foo = Shape(self,
                        shape,
                        self.graph_sizex * (ycount * movey) + starty * self.graph_sizex + (xcount * movex) + startx + offset,
                        orientation,
                        first)
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
        for foo in self.shape_generator(shape,movex,movey,delta_offset,orientation,startx,starty,first):
            self.shape_list.append(foo)
            self.graph_draw.shape_queue.append(foo)
            self.draw_shape(foo)
        self.draw()

    def draw_layers(self, shape1, movex1, movey1,delta_offset1, orientation1,
                    shape2, movex2, movey2,delta_offset2, orientation2, startx2, starty2,
                    shape3=None, movex3=None, movey3=None,delta_offset3=None, orientation3=None, startx3=None, starty3=None):
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

        if self.check(33, 66) and self.stable == True:
            self.matrix_list.append(
                [self.matrix, shape1, movex1, movey1, delta_offset1, orientation1, shape2, movex2, movey2,delta_offset2, orientation2, startx2,
                 starty2, shape3, movex3, movey3,delta_offset3, orientation3, startx3, starty3])
            self.found += 1

        self.raise_not_stable()
        self.stable = True

    def make_connection(self, point1, point2, letter=None, orientation=None):
        for i in self.edge_list:
            if (i[0] == point1 and i[1] == point2) or (i[0] == point2 and i[1] == point1):
                i[2] += 1
                i[3] = len(self.shape_list)
                if letter:
                    if i[4] == 0:
                        i[4] = letter
                        i[5] = orientation
                    elif i[4] == "checked":
                        self.raise_not_stable()
                        return
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
        self.edge_list = []
        self.shape_list = []
        self.node_list = []
        self.__generate_edges()
        self.matrix = self.generate_matrix(self.chain_length,self.chain_length,self.chain_length)
        self.graph_draw = GraphDraw(self,750,self.graph_sizex)

        self.stable = False

    def check(self, first_point, second_point):
        for i in self.edge_list:
            if (i[0] % self.graph_sizex >= first_point % self.graph_sizex and
                            i[0] % self.graph_sizex <= second_point % self.graph_sizex and
                            i[1] % self.graph_sizex >= first_point % self.graph_sizex and
                            i[1] % self.graph_sizex <= second_point % self.graph_sizex and
                        i[0] >= first_point and i[1] >= first_point and
                        i[0] <= second_point and i[1] <= second_point):
                if (i[2] == 2):
                    pass
                else:
                    return (False)
        return (True)

    def check_if_stable(self):
        if not self.stable:
            return False
        else:
            return True

    def draw_shape(self,shape):
        _start_point = shape.start_point
        _orientation = shape.orientation
        count = 0

        if shape.first == 1:
            alphabet = 0
        elif shape.first == 2:
            alphabet = 1
        else:
            alphabet = 2

        # preveri st. koncev v ogliscu
        self.node_list[_start_point][1] += 1
        if self.node_list[_start_point][1] > 2:
            self.raise_not_stable()
            # print("not stable")
            return
        if self.type == 'triangular':
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
        elif self.type=='squared':
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

    def __generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            self.node_list.append([vertex, 0])
            for neighbour in self.graph_dict[vertex]:
                if [neighbour, vertex, 0, 0, 0, 0] not in edges:
                    edges.append([vertex, neighbour, 0, 0, 0, 0])
        self.edge_list = edges
        return edges
    def draw(self):
        self.graph_draw.draw()


__author__ = 'FAMILY'


class Shape(object):
    def __init__(self, graph, shape, start_point, orientation, first=1):

        self.graph = graph  # graph that the shape will be drawn into
        self.shape = shape  # change of the direction of the chain at each node
        self.start_point = start_point  # node index that the chain will start in the graph
        self.orientation = orientation  # orientation of the first segment of the chain
        self.sizex = graph.graph_sizex  # number of nodes in a row in the graph
        self.first = first  # layer that the shape belongs to
        if first == 1:
            self.alphabet = graph.alphabet[0]
        elif first == 2:
            self.alphabet = graph.alphabet[1]
        else:
            self.alphabet = graph.alphabet[2]

        self.segment_list = self.init_edges()

    def init_edges(self):
        # generates the segments listed as [start node, end node, segment orientation, segment letter]
        _start_point = self.start_point
        _orientation = self.orientation
        temp = []
        count = 0
        if self.graph.graph_type == "triangular":
            """
                there are 6 possible orientations:
                    0 - horizontal, facing right
                    1 - diagonal, facing down and right
                    2 - diagonal, facing down and left
                    3 - horizontal, facing left
                    4 - diagonal, facing up and left
                    5 - diagonal, facing up and right
            """
            if (_start_point // 10) % 2 == 0:
                row_switch = 1
                arow_switch = 0
            else:
                row_switch = 0
                arow_switch = 1
            if _orientation == 0:
                temp.append([_start_point,_start_point + 1,_orientation, self.alphabet[count]])
                _start_point += 1
            if _orientation == 1:
                temp.append([_start_point,_start_point + self.sizex + arow_switch,_orientation, self.alphabet[count]])
                _start_point = _start_point + self.sizex + arow_switch
            if _orientation == 2:
                temp.append([_start_point,_start_point + self.sizex - row_switch,_orientation, self.alphabet[count]])
                _start_point += self.sizex - row_switch
            if _orientation == 3:
                temp.append([_start_point,_start_point - 1,_orientation, self.alphabet[count]])
                _start_point -= 1
            if _orientation == 4:
                temp.append([_start_point,_start_point - self.sizex - arow_switch,_orientation, self.alphabet[count]])
                _start_point = _start_point - self.sizex - arow_switch
            if _orientation == 5:
                temp.append([_start_point,_start_point - self.sizex + row_switch,_orientation, self.alphabet[count]])
                _start_point += -self.sizex + row_switch

            for i in self.shape:

                count += 1

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
                    temp.append([_start_point,_start_point + 1,_orientation, self.alphabet[count]])
                    _start_point += 1
                if _orientation == 1:
                    temp.append([_start_point,_start_point + self.sizex + arow_switch,_orientation, self.alphabet[count]])
                    _start_point = _start_point + self.sizex + arow_switch
                if _orientation == 2:
                    temp.append([_start_point,_start_point + self.sizex - row_switch,_orientation, self.alphabet[count]])
                    _start_point += self.sizex - row_switch
                if _orientation == 3:
                    temp.append([_start_point,_start_point - 1,_orientation, self.alphabet[count]])
                    _start_point -= 1
                if _orientation == 4:
                    temp.append([_start_point,_start_point - self.sizex - row_switch,_orientation, self.alphabet[count]])
                    _start_point = _start_point - self.sizex - row_switch
                if _orientation == 5:
                    temp.append([_start_point,_start_point - self.sizex + arow_switch,_orientation, self.alphabet[count]])
                    _start_point += -self.sizex + arow_switch
        elif self.graph.graph_type == "squared":
            """
            there are 4 possible orientations:
                    0 - horizontal, facing right
                    1 - vertical, facing down
                    2 - horizontal, facing left
                    3 - vertical, facing up
            """
            if _orientation == 0:
                temp.append([_start_point, _start_point + 1, _orientation, self.alphabet[count]])
                _start_point += 1
            if _orientation == 1:
                temp.append([_start_point, _start_point + self.sizex, _orientation, self.alphabet[count]])
                _start_point = _start_point + self.sizex
            if _orientation == 2:
                temp.append([_start_point, _start_point - 1, _orientation, self.alphabet[count]])
                _start_point -= 1
            if _orientation == 3:
                temp.append([_start_point, _start_point - self.sizex, _orientation, self.alphabet[count]])
                _start_point = _start_point - self.sizex
            for i in self.shape:
                count += 1
                if i == -1:
                    _orientation -= 1
                    if _orientation < 0:
                        _orientation += 4
                elif i == 1:
                    _orientation += 1
                    if _orientation >= 4:
                        _orientation -= 4
                if _orientation == 0:
                    temp.append([_start_point, _start_point + 1, _orientation, self.alphabet[count]])
                    _start_point += 1
                if _orientation == 1:
                    temp.append([_start_point, _start_point + self.sizex, _orientation, self.alphabet[count]])
                    _start_point = _start_point + self.sizex
                if _orientation == 2:
                    temp.append([_start_point, _start_point - 1, _orientation, self.alphabet[count]])
                    _start_point -= 1
                if _orientation == 3:
                    temp.append([_start_point, _start_point - self.sizex, _orientation, self.alphabet[count]])
                    _start_point = _start_point - self.sizex
        return temp
    def get_size(self):
        # returns the span of the shape in each direction
        _orientation = self.orientation
        x = 0
        y = 0
        minx = x
        maxx = x
        miny = y
        maxy = y
        if self.graph.graph_type == "triangular":
            # in triangular graps, the span changes with each row because of the nature of the connections
            if (self.start_point // 10) % 2 == 0:
                row_switch = 1
                arow_switch = 0
            else:
                row_switch = 0
                arow_switch = 1

            if _orientation == 0:
                x += 1
            elif _orientation == 1:
                y += 1
                x += arow_switch
                row_switch, arow_switch = arow_switch, row_switch
            elif _orientation == 2:
                y += 1
                x -= row_switch
                row_switch, arow_switch = arow_switch, row_switch
            elif _orientation == 3:
                x -= 1
            elif _orientation == 4:
                y -= 1
                x -= row_switch
                row_switch, arow_switch = arow_switch, row_switch
            elif _orientation == 5:
                y -= 1
                x += arow_switch
                row_switch, arow_switch = arow_switch, row_switch
            if x < minx:
                minx = x
            elif y < miny:
                miny = y
            elif x > maxx:
                maxx = x
            elif y > maxy:
                maxy = y
            for i in self.shape:
                _orientation += i
                if _orientation < 0:
                    _orientation += 6
                if _orientation >= 6:
                    _orientation -= 6
                if _orientation == 0:
                    x += 1
                elif _orientation == 1:
                    y += 1
                    x += arow_switch
                    row_switch, arow_switch = arow_switch, row_switch
                elif _orientation == 2:
                    y += 1
                    x -= row_switch
                    row_switch, arow_switch = arow_switch, row_switch
                elif _orientation == 3:
                    x -= 1
                elif _orientation == 4:
                    y -= 1
                    x -= row_switch
                    row_switch, arow_switch = arow_switch, row_switch
                elif _orientation == 5:
                    y -= 1
                    x += arow_switch
                    row_switch, arow_switch = arow_switch, row_switch

                if x < minx:
                    minx = x
                if y < miny:
                    miny = y
                if x > maxx:
                    maxx = x
                if y > maxy:
                    maxy = y
        elif self.graph.graph_type == "squared":
            if _orientation == 0:
                x += 1
            elif _orientation == 1:
                y += 1
            elif _orientation == 2:
                x -= 1
            elif _orientation == 3:
                y -= 1
            if x < minx:
                minx = x
            elif y < miny:
                miny = y
            elif x > maxx:
                maxx = x
            elif y > maxy:
                maxy = y
            for i in self.shape:
                if i == 1:
                    _orientation += 1
                    if _orientation == 4:
                        _orientation = 0
                elif i == -1:
                    _orientation -= 1
                    if _orientation == -1:
                        _orientation = 3
                if _orientation == 0:
                    x += 1
                elif _orientation == 1:
                    y += 1
                elif _orientation == 2:
                    x -= 1
                elif _orientation == 3:
                    y -= 1
                if x < minx:
                    minx = x
                elif y < miny:
                    miny = y
                elif x > maxx:
                    maxx = x
                elif y > maxy:
                    maxy = y
        return [maxx, minx, maxy, miny]

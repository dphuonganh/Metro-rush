import pyglet
from pyglet.window import mouse
from pyglet.window import key


def find_index(Metro, line, position):
    """
    find index of station connect with another line in Metro
    @param Metro : a dictionary contain lines and stations in file data
                   with lines is key and value is list contain objects station
    @param line : current line contain objects station what need find index
    @param position : position of station in currnt line
    @return index of station
    """
    for index, station_obj in enumerate(Metro[line]):
        if station_obj.name == Metro[position[0]][position[1]].name:
            return index


def take_connect(Metro, output):
    """
    take coordiate of all station connected to draw line connect
    @param Metro : a dictionary contain lines and stations in file data
                   with lines is key and value is list contain objects station
    @param output : a dictionary contain all object
                    each object  have coordiate and the name of station
    @return a list contain all point connected
    """
    connect = []
    for key, value in Metro.items():
        for index, ele in enumerate(value):
            if not ele.lines:
                continue
            try:
                for line in ele.lines:
                    obj1 = output[key.split()[0]][index]
                    obj2 = output[line.split()[0]][
                        find_index(Metro, line, [key, index])]
                    connect.append(
                        [obj1.posx, obj1.posy, obj2.posx, obj2.posy])
            except (TypeError, KeyError, AttributeError, IndexError):
                pass
    return connect


def Init(Metro):
    """
    create a dictionary to draw station image, line
    create a list contain point connected
    @param Metro : a dictionary contain lines and stations in file data
                   with lines is key and value is list contain objects station
    @return a dictionary contain all object
            each object  have coordiate and the name of station
    @return a list contain all point connected
    """
    output = {}
    point = 1
    for key, list_station in Metro.items():
        temp = []
        for index, station in enumerate(list_station, 1):
            if len(station.lines) > 1:
                temp.append(Object(index * 40, point * 100, 'swi.png'))
            else:
                temp.append(Object(index * 40, point * 100, 'sta.jpg'))
            temp[-1].name = station.name
        point += 1
        output[key.split()[0]] = temp

    return output, take_connect(Metro, output)


def hit(take, list_station):
    """
    return a station name if click hit a station on display
    """
    for obj in list_station:
        posx = obj.posx - obj.width // 2
        posy = obj.posy - obj.height // 2
        if posx < take[0] and posx + obj.width > take[0] \
                and obj.height + posy > take[1] and obj.height < take[1]:
            return obj.name
    return False


class Object:
    """
    class contain image and position of its
    """
    def __init__(self, posx, posy, img):
        self.posx = posx
        self.posy = posy
        self.sprite = self.Sprite(img)
        self.sprite.x = self.posx
        self.sprite.y = self.posy
        self.width = self.sprite.width
        self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def Sprite(self, img):
        """
        Sprite image
        """
        image = pyglet.image.load(img)
        image.anchor_x = image.width // 2
        image.anchor_y = image.width // 2
        return pyglet.sprite.Sprite(image)


class Window(pyglet.window.Window):
    def __init__(self, graph=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # declare data stucture to draw station and point connect
        self.graph, self.connect = Init(graph.lines)
        self.color = {
            'Pink': [255, 20, 147],
            'Red': [255, 0, 0],
            'Airport': [255, 69, 0],
            'Violet': [238, 130, 238],
            'Green': [84, 255, 159],
            'Yellow': [255, 255, 0],
            'Blue': [0, 0, 255],
            'Magenta': [255, 0, 255]
        }
        # list contain all step move of all train
        self.list_move = graph.output
        self.current_turn = 0
        # create 2 circle in point end and point start
        start = self.graph[graph.start[0].split()[0]][graph.start[1] - 1]
        end = self.graph[graph.end[0].split()[0]][graph.end[1] - 1]
        self.start = Object(start.posx, start.posy, 'cir.png')
        self.end = Object(end.posx, end.posy, 'cir.png')
        # declare text
        self.name_station = pyglet.text.Label(start.name, font_size=30,
                                              x=1300, y=750)
        self.turn = pyglet.text.Label('0', font_size=30, x=25, y=750)
        self.total_turn = pyglet.text.Label('/' + str(len(self.list_move)-1),
                                            font_size=30, x=70, y=750)

    def on_draw(self):
        self.clear()
        # draw lines connect points connected
        for x in self.connect:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2i', (x[0], x[1], x[2], x[3])),
                                 ('c3B', (54, 54, 54, 54, 54, 54)))
        # draw stations and lines
        for key, list_station in self.graph.items():
            x0 = list_station[0].posx
            y0 = list_station[0].posy
            x1 = list_station[-1].posx
            y1 = list_station[-1].posy
            # draw line
            if key in self.color:
                temp = self.color[key]
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v2i', (x0, y0, x1, y1)),
                                     ('c3B', (temp[0], temp[1],
                                              temp[2], temp[0],
                                              temp[1], temp[2])))
            else:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v2i', (x0, y0, x1, y1)),
                                     ('c3B', (255, 255, 255, 255, 255, 255)))
            # draw station
            for station in list_station:
                station.draw()
        # draw all station contain at least train
        for list_coor in self.list_move[self.current_turn]:
            temp_obj = self.graph[list_coor[0].split()[0]][list_coor[1] - 1]
            Object(temp_obj.posx, temp_obj.posy, 'train.png').draw()

        self.start.draw()
        self.end.draw()

        self.name_station.draw()
        self.turn.draw()
        self.total_turn.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT and self.current_turn > 0:
            self.current_turn -= 1
        if symbol == key.RIGHT and self.current_turn < len(self.list_move) - 1:
            self.current_turn += 1
        self.turn.text = str(self.current_turn)

    def on_mouse_press(self, x, y, button, modifier):
        if button == mouse.LEFT:
            for line in self.graph.values():
                temporary = hit([x, y], line)
                if temporary:
                    self.name_station.text = temporary
                    return


def GUI(Graph):
    Window(Graph, 1920, 800, 'Visualzation')
    pyglet.app.run()

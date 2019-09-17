from graph import Graph
from node import Node


def get_path(node):
    """
    return the path from the start station to the end station
    take a node and that node will return node parent
    @param node : node last in linked list
    """
    path = []
    while node.parent_node:
        path.append(node)
        node = node.parent_node
    path.append(node)
    return path[::-1]


class BreadthFirstSearch(Graph):
    """
    class find all path from start station to end station
    """
    def __init__(self, input_data):
        super().__init__()
        self.create_graph(input_data)
        self.paths = []

    def get_station_id(self, line_name, station_name):
        """
        find index of station connect with another line in Metro
        @param line_name : current line contain objects station
                           what need find index
        @param station_name : position of station in currnt line
        @return index of station
        """
        for index, station in enumerate(self.lines[line_name], 1):
            if station.name == station_name:
                return index

    def check_another_lines(self, current_node, open_list):
        """
        append other stations in other lines if current station connect
        to other lines
        @param current_node : current node
        @param open_list : list contain all node need check
        @return None
        """
        try:
            station = self.get_station(current_node.line_name,
                                       current_node.station_id)
            lines = station.lines.copy()
            lines.remove(current_node.line_name)
            while lines:
                another_line = lines.pop()
                if another_line not in self.lines:
                    continue
                station_id = self.get_station_id(another_line, station.name)
                open_list.append(Node(another_line, station_id,
                                      current_node, 0, 'switch'))
        except TypeError:
            pass

    def check_left_node(self, current_node, open_list, line_len):
        """
        append left stations if that station not in open list
        @param current_node : current node
        @param open_list : list contain all node need check
        @param line_len : length of line
        @return None
        """
        try:
            if current_node.station_id > 1 and current_node.status != 1:
                open_list.append(Node(current_node.line_name,
                                      current_node.station_id - 1,
                                      current_node, -1, 'move'))
            elif current_node.line_name in self.circular_lines \
                    and current_node.station_id == 1:
                open_list.append(Node(current_node.line_name,
                                      line_len - 1,
                                      current_node, -1, 'move'))
        except TypeError:
            pass

    def check_right_node(self, current_node, open_list, line_len):
        """
        append right stations if that station not in open list
        @param current_node : current node
        @param open_list : list contain all node need check
        @param line_len : length of line
        @return None
        """
        try:
            if current_node.station_id < line_len \
                    and current_node.status != -1:
                open_list.append(Node(current_node.line_name,
                                      current_node.station_id + 1,
                                      current_node, 1, 'move'))
            elif current_node.line_name in self.circular_lines \
                    and current_node.station_id == line_len:
                open_list.append(Node(current_node.line_name, 2,
                                      current_node, 1, 'move'))
        except TypeError:
            pass

    def check_neighbor_node(self, current_node, open_list):
        """
        check and append (if possible) left, right and
        node in other line of current node
        @param open_list : list contain all node need check
        @param line_len : length of line
        @return None
        """
        line_len = len(self.lines[current_node.line_name])
        self.check_another_lines(current_node, open_list)
        self.check_left_node(current_node, open_list, line_len)
        self.check_right_node(current_node, open_list, line_len)

    def find_paths(self):
        """
        use algorithm Breadth First Search to find all path possible
        """
        open_list = [Node(*self.start, None)]
        close_list = []
        while open_list:
            current_node = open_list.pop(0)
            position = [current_node.line_name, current_node.station_id]
            # if current node have been check
            if position in close_list:
                continue
            # if current node is point end
            if position == self.end:
                self.paths.append(get_path(current_node))
                continue
            close_list.append(position)
            self.check_neighbor_node(current_node, open_list)

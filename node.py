class Node:
    """
    Represent a node in path.
    Attributes:
        - line_name: line name
        - station_id: station ID
        - parent_node: parent node
        - status: valid direction of node to find path, with 3 modes:
                        -1 (left)
                        0 (left, right) -> default mode
                        1 (right)
        - action: valid action of node to run train, with 3 modes:
                        - None (nothing) -> default mode
                        - 'move' (move to next station)
                        - 'switch' (switch to another line)
        - switched: check train transferred to another line, with 2 modes:
                        - True: transferred
                        - False: not yet -> default mode
    """
    def __init__(self, line_name, station_id, parent_node,
                 status=0, action=None, switched=False):
        """
        Initialize attributes of Node class.
        @param line_name: line name
        @param station_id: station ID
        @param parent_node: parent node
        @param status: node direction
        @param action: node action
        @param switched: mode of transfer
        """
        self.line_name = line_name
        self.station_id = station_id
        self.parent_node = parent_node
        self.status = status
        self.action = action
        self.switched = switched

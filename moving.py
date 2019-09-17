from finding import BreadthFirstSearch


def move_station(current_station, parent_station):
    """
    Move train from parent station to current station.
    @param current_station: current station object
    @param parent_station: parent station object
    @return: boolean - True: success moving
                     - False: failed moving
    """
    if parent_station.trains:
        if current_station.push_train(parent_station.trains[-1]):
            parent_station.pop_train()
            return True
    return False


def get_output(result, temp, index, station, node):
    """
    Get output after each turn.
    @param result: list contains all station string
    @param temp: temporary list
    @param index: path index
    @param station: current station object
    @param node: current node object
    @return: list contains result and temp list
    """
    result[index].append('{}({}:{})-{}'.format(
        station.name, node.line_name, node.station_id,
        ','.join(station.trains)))
    temp.append([node.line_name, node.station_id])
    return [result, temp]


def display_output(result, index):
    print('\t* Path {}:'.format(index + 1))
    print('|'.join(result[index]))


class MovingTrains(BreadthFirstSearch):
    def __init__(self, input_data, algo):
        """
        Initialize attributes of MovingTrains class.
        @param input_data: list of each line in metro stations file
        @param algo: algorithm type
        """
        super().__init__(input_data)
        self.find_paths()
        self.algo = algo
        self.depart_rate = [0, 0]
        self.num_turns = 0
        self.output = []
        self.calculate_depart_rate()
        self.move_trains()

    def get_constant(self):
        """
        Calculate constant of each path.
        @return: list of constants of each path
        """
        const = [1, 1]
        for index in range(2):
            for node in self.paths[index]:
                if node.action == 'switch':
                    const[index] = 2
                    break
        return const

    def get_cost(self):
        """
        Get cost of each path.
        @return: list of costs of each path
        """
        return [len(self.paths[0]) - 1, len(self.paths[1]) - 1]

    def add_depart_rate(self, path_index, c, cost):
        """
        Plus depart rate with constant of path.
        @param path_index: index of path
        @param c: constant of path
        @param cost: cost of path
        @return: new cost of path
        """
        self.depart_rate[path_index] += 1
        return cost + c

    def calculate_depart_rate(self):
        """Calculate the rate of trains departing each path."""
        # Run only one path.
        if len(self.paths) == 1 or self.algo == 0:
            self.depart_rate[0] = self.num_trains
        # Run two path.
        elif len(self.paths) > 1:
            # Get constant and cost of each path.
            c1, c2 = self.get_constant()
            cost1, cost2 = self.get_cost()
            # Update the rate of trains depart from each path.
            for index in range(1, self.num_trains + 1):
                if cost1 <= cost2:
                    cost1 = self.add_depart_rate(0, c1, cost1)
                    continue
                cost2 = self.add_depart_rate(1, c2, cost2)

    def print_each_path(self):
        """Display trains and save movement history after each turn."""
        # Initialize list containing each station string.
        result = [[] for _ in range(self.algo + 1)]
        station_string = []
        for index, path in enumerate(self.paths[:self.algo + 1]):
            temp = []
            for node in path:
                station = self.get_station(node.line_name, node.station_id)
                # Skip when trains of station is empty.
                if not len(station.trains):
                    continue
                # Check action of node is 'switch'.
                if node.action == 'switch':
                    # Skip when not switched.
                    if not node.switched:
                        continue
                    # Remove last element of result and temp list.
                    result[index].pop()
                    temp.pop()
                # Update result and temp list.
                result, temp = get_output(result, temp, index, station, node)
                # Check and add element of temp to station string.
                for item in temp:
                    if item not in station_string:
                        station_string.append(item)
            display_output(result, index)
        # Save station string to output attribute.
        self.output.append(station_string)

    def print_trains(self):
        """Display trains containing trains after each turn."""
        print('___Turn {}___'.format(self.num_turns))
        try:
            self.print_each_path()
        except IndexError:
            pass

    def check_train_depart(self, path_index):
        """
        Check train can depart from path.
        @param path_index: index of path
        @return: boolean - True: valid depart
                         - False: invalid depart
        """
        if self.depart_rate[path_index] > 0:
            return True
        return False

    def update_each_path(self, path_index):
        """
        Update all trains of each path after each turn.
        @param path_index: index of path
        """
        # Update each path.
        for node in self.paths[path_index][:0:-1]:
            # Get current and parent station object.
            current_station = self.get_station(node.line_name, node.station_id)
            parent_station = self.get_station(node.parent_node.line_name,
                                              node.parent_node.station_id)
            # Skip when:
            if node.action != 'move' or not parent_station.trains:
                continue
            # Action of parent node is 'move'.
            if node.parent_node.action == 'move':
                move_station(current_station, parent_station)
            # Action of parent node is None.
            elif not node.parent_node.action:
                if self.check_train_depart(path_index):
                    if move_station(current_station, parent_station):
                        self.depart_rate[path_index] -= 1
            # Action of parent node is 'switch'.
            else:
                if node.parent_node.switched:
                    move_station(current_station, parent_station)
                # Change mode of switched node.
                node.parent_node.switched = not node.parent_node.switched

    def update_trains(self):
        """Update all trains after each turn."""
        try:
            for path_index in range(self.algo + 1):
                self.update_each_path(path_index)
        except IndexError:
            pass

    def move_trains(self):
        """Run all trains."""
        self.print_trains()
        while len(self.get_station(*self.end).trains) < self.num_trains:
            self.update_trains()
            self.num_turns += 1
            self.print_trains()

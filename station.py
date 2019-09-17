class Station:
    """
    Represent a station in the metro network.
    Attributes:
        - name: station name
        - lines: set of lines containing station
        - capacity: capacity of station
        - trains: list of trains in station
    """
    def __init__(self, station_name, line_name, capacity=1):
        """
        Initialize attributes of Station class.
        @param station_name: station name
        @param line_name: line name containing station
        @param capacity: capacity of station
        """
        self.name = station_name
        self.lines = {line_name}
        self.capacity = capacity
        self.trains = []

    def add_line(self, line_name):
        """
        Add a new line to the set of lines containing station.
        @param line_name: line name containing station
        """
        self.lines.add(line_name)

    def push_train(self, train_label):
        """
        Add train to station.
        @param train_label: train label
        @return: boolean - True: success adding
                         - False: failed adding
        """
        if len(self.trains) < self.capacity:
            self.trains.insert(0, train_label)
            return True
        return False

    def pop_train(self):
        """Remove last train from station."""
        try:
            self.trains.pop(-1)
        except IndexError:
            pass

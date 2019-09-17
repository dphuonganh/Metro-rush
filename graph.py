from sys import stderr
from math import inf
from station import Station


def parse_station_info(args):
    """
    Get station name and other line name form station info.
    @param args: station info
    @return: list contains info of station
    """
    station_name, another_line_name = None, None
    if len(args) == 2:
        _, station_name = args
    elif len(args) == 4:
        _, station_name, _, another_line_name = args
    return [station_name, another_line_name]


class Graph:
    """
    Represent a metro network.
    Attributes:
        - stations: dictionary of stations in metro network
        - lines: dictionary of lines in metro network
        - circular_lines: set of circular lines in metro network
        - start: list contains information of start station
        - end: list contains information of end station
        - num_trains: number of trains in metro network
    """
    def __init__(self):
        """Initialize attributes of Graph class."""
        self.stations = {}
        self.lines = {}
        self.circular_lines = set()
        self.start, self.end = [None, None], [None, None]
        self.num_trains = 0

    def get_station(self, line_name, station_id):
        """
        Get station object from dictionary of lines  in metro network.
        @param line_name: line name containing station
        @param station_id: station ID
        @return: - station object: station exists
                 - None: station does not exist
        """
        try:
            return self.lines[line_name][station_id - 1]
        except KeyError:
            return None

    def create_line(self, line_name):
        """
        Create new line in dictionary of lines in metro network.
        @param line_name: line name
        @return: line name
        """
        if line_name not in self.lines:
            self.lines[line_name] = []
        return line_name

    def check_circular_line(self, line_name, station_name):
        """
        Check current line is a circular line.
        @param line_name: current line name
        @param station_name: current station name
        @return: boolean - True: circular line
                         - False: straight line
        """
        try:
            # Check current station is the same as first station of line.
            if station_name == self.lines[line_name][0].name:
                self.circular_lines.add(line_name)
        except IndexError:
            pass

    def setup_station(self, line_name, station_name, another_line_name):
        """
        Setup attribute values of station object.
        @param line_name: line name
        @param station_name: station name
        @param another_line_name: another line name
        @return: station object
        """
        # Check dictionary of stations contains current station.
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name, line_name)
        else:
            self.stations[station_name].add_line(line_name)
            self.stations[station_name].add_line(another_line_name)
        # Check another line name is None.
        if another_line_name:
            self.stations[station_name].add_line(another_line_name)
        return self.stations[station_name]

    def create_station(self, line_name, args):
        """
        Create new station in dictionary of stations in metro network.
        @param line_name: line name
        @param args: list contains info of station
        """
        # Get station info.
        station_name, another_line_name = parse_station_info(args)
        # Check current line is circular line.
        self.check_circular_line(line_name, station_name)
        # Add station to line.
        self.lines[line_name].append(
            self.setup_station(line_name, station_name, another_line_name))

    def setup_start_end_point(self, line_name, station_id):
        """
        Setup start/end station info in metro network.
        @param line_name: line name of start/end point
        @param station_id: station ID of start/end point
        @return: list contains information of start/end station
        """
        self.get_station(line_name, station_id).capacity = inf
        return [line_name, station_id]

    def setup_trains(self, number):
        """
        Setup departure station for all trains in metro network.
        @param number: number of trains in metro network
        """
        self.num_trains = number
        # Initialize a list of all train labels.
        trains = []
        for index in range(number, 0, -1):
            trains.append('T{}'.format(index))
        # Assign above list to start station attribute.
        self.get_station(*self.start).trains = trains

    def analyze_and_store_data(self, input_data):
        """
        Setup attribute values from input data.
        @param input_data: list of each line in metro stations file
        """
        line_name = None
        # Read each line in input data.
        for row in input_data:
            row = row.strip()
            # Take division position of row containing start/end station info.
            div_pos = row.find(':')
            # Row contains line name.
            if row.startswith('#'):
                line_name = self.create_line(row[1:])
            # Row contains start station info.
            elif row.startswith('START'):
                self.start = self.setup_start_end_point(
                    row[6:div_pos], int(row[div_pos + 1:]))
            # Row contains end station info.
            elif row.startswith('END'):
                self.end = self.setup_start_end_point(
                    row[4:div_pos], int(row[div_pos + 1:]))
            # Row contains number of trains in metro network.
            elif row.startswith('TRAINS'):
                self.setup_trains(int(row[7:]))
            # Row contains station info.
            elif row:
                self.create_station(
                    line_name, [arg.strip() for arg in row.split(':')])

    def create_graph(self, input_data):
        """
        Create a metro graph.
        If data is invalid, raise error.
        @param input_data: list of each line in metro stations file
        """
        try:
            self.analyze_and_store_data(input_data)
        except (NameError, ValueError):
            stderr.write('Invalid file\n')
            exit(1)

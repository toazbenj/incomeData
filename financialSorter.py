"""
Income Data Sorter By State and County

    Open_file():
        Open file for reading, prompt until successful
    Get_County_State():
        Extract county and state from string
    Read_File():
        Loop through file, make tuple list (state, county, median_income)

    State_Average_Income():
        Find income average for counties in state
    Top_Counties_By_Income():
        Find top ten income counties in decreasing order
    Bottom_Counties_By_Income():
        Find the bottom ten income counties in decreasing order
    Top_States_By_Income():
        Find top ten income states in decreasing order
    Bottom_States_By_Income():
        Find bottom ten income counties decreasing order
    Counties_In_State():
        Find tuple list with counties, incomes sorted alphabetically

    Display_Options():
        Display menu of options for program, take option input

    Main():
        Open_file()
        Read_File()
        User Input Loop
            Display_Options()
            Option Decision Tree
                1- State_Average_Income()
                2- Top_Counties_By_Income()
                3- Bottom_Counties_By_Income()
                4- Top_States_By_Income()
                5- Bottom_States_By_Income()
                6- Counties_In_State()

"""

# Import Library
import csv
from operator import itemgetter

# Constants
STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


def open_file(ch):
    """File name hardcoded here for demo purposes"""
    """Opens file for reading, prompts until successful"""

    # User Input Loop
    # while True:
    #     # Reading file
    #     if ch == "r":
    #         try:
    #             file_str = input('Input a file: ')
    #             file_pointer = open(file_str, 'r')
    #             break
    #         except IOError:
    #             print('Invalid filename, please try again.')
    file_pointer = open("data.csv", 'r')
    return file_pointer


def get_county_state(s):
    """Extract county and state from string"""

    # Split the line, extract state and county
    format_list = s.split(",")
    state = format_list[1]
    county = format_list[0]

    # Remove leading and trailing spaces
    state = state.strip()
    county = county.strip()

    return county, state


def read_file(fp):
    """ Loop through file, make tuple list (state, county, median_income)"""

    # Skip Header
    fp.readline()

    # Read file, extract columns 1 and 10, put into place name and income lists
    name_list = []
    income_list = []
    reader = csv.reader(fp)

    for line_list in reader:
        name_list.append(line_list[1])

        # Remove Commas from income
        if line_list[10] != "":
            format_list = line_list[10].split(",")
            format_str = "".join(format_list)
            income_list.append(int(format_str))
        else:
            income_list.append(line_list[10])

    # Separate state and county, match up place with income
    stats_list = []
    income_count = 0

    for name in name_list:
        # Call the get_county_state to separate the county and state
        county, state = get_county_state(name)
        stats_tuple = state, county, income_list[income_count]

        # If there is no value for income, ignore that county
        if stats_tuple[2] != "":
            stats_list.append(stats_tuple)

        income_count += 1

    # Return a list of tuples (state, county, median_income)
    # in decreasing order of median_income
    return sorted(stats_list, key=itemgetter(2), reverse=True)


def state_average_income(state, master_list):
    """Find median income average for counties in state"""

    # Check for incorrect spelling
    if state not in STATES:
        return None

    # Add up incomes
    total = 0
    count = 0
    for county_tuple in master_list:
        if county_tuple[0] == state:
            total += county_tuple[2]
            count += 1

    # Check for wrong state
    if count == 0:
        return None

    avg = total/count

    return round(avg, 2)


def top_counties_by_income(master_list):
    """Find top ten counties by median income in decreasing order"""

    income_order_list = sorted(master_list, key=itemgetter(2), reverse=True)
    top_ten_list = income_order_list[0:10]

    return top_ten_list


def bottom_counties_by_income(master_list):
    """Find the bottom ten counties by median incomes in decreasing order"""

    income_order_list = sorted(master_list, key=itemgetter(2), reverse=True)
    bottom_ten_list = income_order_list[-10:]

    return bottom_ten_list


def top_states_by_income(master_list):
    """Find top ten states by average median incomes in decreasing order"""

    # Call state_average_income for each state, sort
    avg_list = []
    for state in STATES:
        # Make list of each state and average income in tuples
        stats_list = [state, state_average_income(state, master_list)]

        # Check if income value is empty
        try:
            float(stats_list[1])
            avg_list.append(stats_list)
        except TypeError:
            continue

    # Return tuple list where each tuple is (state, average_median_income)
    avg_list = sorted(avg_list, key=itemgetter(1), reverse=True)
    return avg_list[0:10]


def bottom_states_by_income(master_list):
    """Find bottom ten counties by median incomes in decreasing order"""

    # Call state_average_income for each state, sort
    avg_list = []
    for state in STATES:
        # Make list of each state and average income in tuples
        stats_list = [state, state_average_income(state, master_list)]

        # Check if income value is empty
        try:
            float(stats_list[1])
            avg_list.append(stats_list)
        except TypeError:
            continue

    # Return tuple list where each tuple is (state, average_median_income)
    avg_list = sorted(avg_list, key=itemgetter(1))
    return avg_list[:10]


def counties_in_state(state, master_list):
    """Find tuple list with counties, median incomes sorted alphabetically"""

    # Find counties in state, extract name and income
    county_list = []
    for in_tuple in master_list:
        # Check if county is in state
        if in_tuple[0] == state:
            stats_list = tuple([in_tuple[1], in_tuple[2]])
            county_list.append(stats_list)

    # Return a list of tuples (county, median_income)
    county_tuple = sorted(county_list, key=itemgetter(0))
    return county_tuple


def display_options():
    """Display menu of options for program, take option input"""

    OPTIONS = """\nMenu
    1: Average median household income in a state
    2: Highest median household income counties
    3: Lowest median household income counties
    4: Highest average median household income states
    5: Lowest average median household income states
    6: List counties' median household income in a state\n"""

    print(OPTIONS)

    option = input('Choose an option, q to quit: ')

    return option


def main():
    print("\nMedian Income Data")

    # Call open_file to open an input file for reading
    fp = open_file("r")

    # Call read_file to read the desired data into a “master” list of tuples.
    master_list = read_file(fp)

    # Display menu of options, prompt for input, execute options
    # Loop until the input is "q"
    option = ""
    while option != "q":
        option = display_options()

        # Check if quitting or numerical input
        if option.isalpha():
            pass
        else:
            option = int(option)

        # Option Decision Tree
        if option == 1:

            # Prompt user for 2-letter code until valid
            while True:
                state = input('Please enter a 2-letter state code: ').upper()

                # Checks for spelling, calls state_average_income
                if state in STATES:
                    income = state_average_income(state, master_list)
                    break
                else:
                    print('Please input a valid state')

            # Display income
            print('\nAverage median income in {:2s}: ${:<10,.2f}'
                  .format(state, income))

        elif option == 2:

            # Call top_counties_by_income to determine the top 10
            display_list = top_counties_by_income(master_list)

            # Display Header Lines
            print('\nTop 10 Counties by Median Household Income (2018)')
            print('{:<10}{:<30s}{:10s}'
                  .format('State', 'County', 'Median Household Income'))

            # Display Data
            for e in display_list:
                print('{:<10}{:<30s}${:<10,d}'.format(e[0], e[1], e[2]))

        elif option == 3:

            # Call bottom_counties_by_income
            display_list = bottom_counties_by_income(master_list)

            # Display Header Lines
            print('\nBottom 10 Counties by Median Household Income (2018)')
            print('{:<10}{:<30s}{:10s}'
                  .format('State', 'County', 'Median Household Income'))

            # Display Data
            for e in display_list:
                print('{:<10}{:<30s}${:<10,d}'.format(e[0], e[1], e[2]))

        elif option == 4:

            # Call top_states_by_income
            display_list = top_states_by_income(master_list)

            # Display Header Lines
            print('\nTop 10 States by Average Median Household Income (2018)')
            print('{:<10}{:<10s}'.format('State', 'Median Household Income'))

            # Display Data
            for e in display_list:
                print('{:<10}${:<10,.2f}'.format(e[0], e[1]))

        elif option == 5:

            # Call bottom_states_by_income
            display_list = bottom_states_by_income(master_list)

            # Display Header Lines
            print('\nBottom 10 States by\
                  Average Median Household Income (2018)')
            print('{:<10}{:<10s}'.format('State', 'Median Household Income'))

            # Display Data
            for e in display_list:
                print('{:<10}${:<10,.2f}'.format(e[0], e[1]))

        elif option == 6:

            # Prompt user for 2-letter code until valid
            while True:
                state = input('Please enter a 2-letter state code: ').upper()

                if state in STATES:
                    income = state_average_income(state, master_list)
                    break
                else:
                    print('Please input a valid state')

            # Find counties in state
            display_list = counties_in_state(state, master_list)

            # Display Data
            if len(display_list) > 0:
                print('\nThere are {} counties in {}:'
                      .format(len(display_list), state))
                print('{:<30s}{:<10}'
                      .format('County', 'Median Household Income'))
            else:
                print('\nThere are 0 counties in {}'.format(state))

            for e in display_list:
                print('{:<30s}${:<10,d}'.format(e[0], e[1]))

        elif option == "q":
            # Pause before break
            pass

        else:
            # Error for wrong input
            print('Invalid choice, please try again')


if __name__ == '__main__':
    main()

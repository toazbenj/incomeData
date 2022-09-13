"""
Region Economic Analysis

    Open_file()
        Take a file type string and prompt until name is correct, open file
    Read_income_file()
        Build a dictionary from income file
    Read_gdp_file()
        Find and append GDP data onto state lists within dictionary
    Read_pop_file()
        Find and append population data onto state lists within dictionary

    Get_min_max()
        Extract data for specified region (str) from the dictionary D
    Get_region_states()
        Build list of tuples for state data in the specified region

    Display_region()
        Display min & max income and GDP; regions’ state data
    Plot_regression()
        Plots the regression line between 2 variables
    Plot()
        Plots selected data for region, calls plot_regression()

    Main()
        Opens income, GPD, population files
        Extracts data from each in a dictionary
        Prompts user for region
        Displays region data
        Prompts user for plotting
        Plots selected data

"""


import csv
import pylab
from operator import itemgetter

REGION_LIST = ['Far West', 'Great Lakes', 'Mideast', 'New England', 'Plains',
               'Rocky Mountain', 'Southeast', 'Southwest', 'all']

STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
          'Connecticut', 'Delaware', 'District of Columbia', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
          'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
          'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
          'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
          'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
          'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
          'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
          'Wyoming']

PROMPT1 = "\nSpecify a region from this list or 'q' to quit -- \nFar West,\
Great Lakes, Mideast, New England, Plains,\
Rocky Mountain, Southeast, Southwest, all: "


def open_file(s="income"):
    '''Take a file type string and prompt until name is correct, open file'''

    # User Input Loop
    while True:
        # Reading file
        try:
            file_str = input('Input a {} file: '.format(s))
            file_pointer = open(file_str, 'r')
            break
        except IOError:
            print('Invalid filename, please try again.')

    return file_pointer


def read_income_file(fp):
    '''Read the income file and build a dictionary'''

    # Skip first 5 lines
    for i in range(6):
        fp.readline()

    # Loop variables
    reader = csv.reader(fp)
    master_dict = {}
    region = ""
    state = ""
    income = 0

    # Extract region name, state name, and income for the state
    for line_list in reader:
        # Region, state names, index 0, either a region or state
        if line_list[0].strip() in REGION_LIST:
            region = line_list[0].strip()
            continue
        else:
            state = line_list[0].strip()

        # Income is at index 6, remove the comma, convert to an int
        format_list = line_list[6].split(",")
        income = int("".join(format_list))

        # Use state as a dictionary key, put region and income into list
        state_list = [region, income]
        master_dict[state] = state_list

    # Return dictionary with key=state and value=[region,income]
    return master_dict


def read_gdp_file(fp, master_dict):
    '''Find and append GDP data onto state lists within dictionary'''

    # Skip first 6 lines
    for i in range(7):
        fp.readline()

    # Loop variables
    reader = csv.reader(fp)
    state = ""
    GDP = 0

    # Extract state name (index 0) and GDP for the state (index 7)
    for line_list in reader:
        # Region, state names, index 0, either a region or state
        if line_list[0].strip() in STATES:
            state = line_list[0].strip()
        else:
            continue

        # GDP is at index 7, remove the comma, convert to an int
        format_list = line_list[7].split(",")
        GDP = int("".join(format_list))

        # Use state as a dictionary key, put GDP into list
        state_list = master_dict[state]
        state_list.append(GDP)
        master_dict[state] = state_list

    # Return dictionary with key=state and value=[region,income,GDP]
    return master_dict


def read_pop_file(fp, master_dict):
    '''Find and append population data onto state lists within dictionary'''

    # Skip 1 header line
    fp.readline()

    # Loop variables
    reader = csv.reader(fp)
    state = ""
    population = 0

    # Extract state population from file, attach to each state tuple
    for line_list in reader:
        # Extract state name (index 1), no regions to skip
        state = line_list[1].strip()

        # Extract population for the state (index 2)
        population = int(line_list[2])
        # Convert population to millions, round to 2 decimal points
        population = round(population/10**6, 2)

        # Use state as key to dictionary, append population value list
        try:
            state_list = master_dict[state]
            state_list.append(population)
            master_dict[state] = state_list
        except KeyError:
            # If state isn't in master_list => it's a region, ignore it
            continue

    # Return dictionary with key=state and value=[region,income,GDP,population]
    return master_dict


def get_min_max(master_dict, region):
    '''Extract data for the specified region (str) from the dictionary D'''

    # Call to get_region_states to get narrow down states
    region_list = get_region_states(master_dict, region)
    # If it returns none the region was invalid
    if region_list == None:
        return None

    # Sort list by income, select first and last values with itemgetter
    income_list = sorted(region_list, key=itemgetter(-1), reverse=True)

    # Select the first and last states to get the min and max income and gdp
    if income_list[0][0] == "DC":
        # Switches DC to full name for beginning max state display
        max_income_state = "District of Columbia", income_list[0][-1],\
            income_list[0][-2]
    else:
        max_income_state = income_list[0][0], income_list[0][-1],\
            income_list[0][-2]

    min_income_state = income_list[-1][0], income_list[-1][-1],\
        income_list[-1][-2]

    # Sort list by GDP, select first and last values with itemgetter
    gdp_list = sorted(region_list, key=itemgetter(-2), reverse=True)
    if gdp_list[0][0] == "DC":
        max_gdp_state = "District of Columbia", income_list[0][-1],\
            income_list[0][-2]
    else:
        max_gdp_state = gdp_list[0][0], gdp_list[0][-1], gdp_list[0][-2]

    min_gdp_state = gdp_list[-1][0], gdp_list[-1][-1], gdp_list[-1][-2]

    # Return min and max for income per capita, GDP per capita,
    # States are tuples: (state, income per capita, GDP per capita)
    return min_income_state, max_income_state, min_gdp_state, max_gdp_state


def get_region_states(master_dict, region):
    '''Build list of tuples for state data in the specified region'''

    # Check if valid region
    if region not in REGION_LIST:
        return None

    # Loop variables
    region_list = []
    # List of names to apply to state tuple using count variable for order
    state_name_list = list(master_dict.keys())
    count = -1

    # Make list of states in region, add per capita income and GDP
    for state in master_dict.values():
        count += 1
        # Check if state is in region
        if state[0] != region and region != "all":
            continue

        # Per capita values rounded to nearest dollar
        income_per_capita = round(state[1]/state[3])
        GDP_per_capita = round(state[2]/state[3])

        # Tuples: (state, population, GDP, income,
        # GDP per capita, income per capita)
        state_tup = state_name_list[count], state[3], state[2], state[1],\
            GDP_per_capita, income_per_capita

        # Replace ‘District of Columbia’ with ‘DC’ state name for large display
        if state_name_list[count] == "District of Columbia":
            state_tup = "DC", state[3], state[2], state[1], \
                GDP_per_capita, income_per_capita

        region_list.append(state_tup)

    # Alphabetize by state
    region_list = sorted(region_list)
    # Return sorted list of tuples
    return region_list


def display_region(master_dict, region):
    '''Display min & max income and GDP; regions’ state data'''

    # If region not in region list, return None, display nothing
    if region not in REGION_LIST:
        return None

    # Header for all states
    elif region == "all":
        print("\nData for the all regions:")

    # Region Header
    else:
        print("\nData for the {:s} region:".format(region))

    # Call get_min_max, get min & max of income and GDP in region
    min_income_state, max_income_state, min_gdp_state, max_gdp_state = \
        get_min_max(master_dict, region)

    # Display that data
    print("\n{:s} has the highest GDP per capita at ${:,d} ".format(
        max_gdp_state[0], max_gdp_state[2]))
    print("{:s} has the lowest GDP per capita at ${:,d} ".format
          (min_gdp_state[0], min_gdp_state[2]))
    print("\n{:s} has the highest Income per capita at ${:,d} ".format(
        max_income_state[0], max_income_state[1]))
    print("{:s} has the lowest Income per capita at ${:,d} ".format(
        min_income_state[0], min_income_state[1]))

    # Call get_region_states to get a list of state data
    state_list = get_region_states(master_dict, region)

    # Header for printing states
    print("\nData for all states in the {:s} region:".format(region))
    print("\n{:15s}{:>13s}{:>10s}{:>12s}{:>18s}{:>20s}".format('State',
        'Population(m)', 'GDP(m)', 'Income(m)',
        'GDP per capita', 'Income per capita'))

    # Loop through list to display
    for state in state_list:
        print("{:15s}{:>13,.2f}{:10,d}{:12,d}{:18,d}{:20,d}".format(state[0],
            state[1], state[2], state[3], state[4], state[5]))


def plot_regression(x, y):
    '''
    This function plots the regression line between 2 variables.
    This function is provided in the skeleton code.
    Parameters:
        x: a list that includes the values for the first variable
        y: a list that includes the values for the second variable
    Returns: None
    '''

    # set the size of the plot
    pylab.rcParams['figure.figsize'] = 6.4, 4.8
    xarr = pylab.array(x)
    yarr = pylab.array(y)
    # fit a line, only takes numpy arrays
    m, b = pylab.polyfit(xarr, yarr, deg=1)
    # plotting the regression line
    pylab.plot(xarr, m*xarr+b, '-')


def plot(region_states):
    '''
    This function plots the data (GDP, population, Income, GDP per capita, and
    Income per capita) for the selected region. It also plots the regression
    line between 2 of the data. This function is provided in the skeleton code.
    Parameters:
        region_states (list of tuples): list of tuples of data for states
        in the specified region (state, population, GDP,income, GDP per capita,
        and income per capita)
    Returns: None
    '''

    VALUES_LIST = ['Pop', 'GDP', 'PI', 'GDPp', 'PIp']
    VALUES_NAMES = ['Population(m)', 'GDP(m)', 'Income(m)', 'GDP per capita',
                    'Income per capita']
    PROMPT2 = "Specify x and y values, space separated from Pop, GDP, PI,\
        GDPp, PIp: "

    # prompt for which values to plot
    while True:
        x_name, y_name = input(PROMPT2).strip().split()
        if x_name.lower() in [s.lower() for s in VALUES_LIST] \
                and y_name.lower() in [s.lower() for s in VALUES_LIST]:
            break
        else:
            print("Error in selection. Please try again.")

    x_index = VALUES_LIST.index(x_name)
    y_index = VALUES_LIST.index(y_name)
    # print("indices:",x_name,":",x_index," ; ", y_name, ":",y_index)

    # +1 accounts for skipping state name in list
    x = [state[x_index+1] for state in region_states]
    y = [state[y_index+1] for state in region_states]
    state_names = [state[0] for state in region_states]

    # get full names
    x_name = VALUES_NAMES[x_index]
    y_name = VALUES_NAMES[y_index]

    # Set the labels and titles of the plot
    pylab.title(x_name+" vs. "+y_name)

    pylab.xlabel(x_name)
    pylab.ylabel(y_name)

    # plot the scatter plot
    pylab.scatter(x, y)
    for i, txt in enumerate(state_names):
        pylab.annotate(txt, (x[i], y[i]))

    # plot the regression line between x and y
    plot_regression(x, y)

    # save and show the graph
    pylab.savefig("plot.png", dpi=100)
    pylab.show()


def main():

    # Call the open_file() with the appropriate string
    # fp = open_file()
    # Read to create dictionary, key is state, value is list of region, income
    master_dict = read_income_file(open("income.csv", "r"))

    # fp = open_file("GDP")
    # Read file to add GDP to dictionary
    master_dict = read_gdp_file(open("gdp.csv", "r"), master_dict)

    # fp = open_file("population")
    # Read file to add population to dictionary
    master_dict = read_pop_file(open("pop.csv", "r"), master_dict)

    # Loop prompting for a region to display data with an option to plot data
    while True:

        region = input(PROMPT1)

        # ‘q’ or ‘Q’ to quit looping, string is PROMPT1
        if region.lower() == 'q':
            break
        elif region not in REGION_LIST:
            continue

        display_region(master_dict, region)

        # Prompt to plot, plot only if 'yes' is entered
        plot_answer_str = input("\nDo you want to create a plot? ")

        # If plotting, call get_region_states to get x and y values to plot
        if plot_answer_str.lower() == "yes":
            state_list = get_region_states(master_dict, region)
            plot(state_list)


if __name__ == '__main__':
    main()

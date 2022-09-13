"""
Income Data Analysis

    Do_plot():
        Plot income range vs. percent of population
    Open_file():
        Opens file for reading, prompts until successful
    Handle_commas():
        Converts strings to ints/floats, removes commas, ignores strings
    Read_file():
        Read each line, extract columns 1-7, return master list

    Find_average():
        Calculates the average salary
    Find_median():
        Find average income of range closest to 50% of total population

    Get_range():
        Finds income bracket closest to given percent of population
    Get_percent():
        Finds income bracket containing given salary

    Main():
        Basic prompts and data displays
        Input loop prompting r for range, p for percent, "" for quit
            Find income range from given percent of population
                Check for correct input
                Get income range, percentage, average income
            Find percentage of population lower than given income
                Check for correct input
                Get cumulative percentage, income range
"""

import pylab


def do_plot(x_vals, y_vals, year):
    '''Plot x_vals vs. y_vals, each is list of numbers of same length.'''

    # Titles/labels
    pylab.xlabel('Income')
    pylab.ylabel('Cumulative Percent')
    pylab.title("Cumulative Percent for Income in "+str(year))

    # Make plot
    pylab.plot(x_vals, y_vals)
    pylab.rcParams['figure.figsize'] = 6.4, 4.8

    # Save and display
    pylab.savefig("plot.png", dpi=100)
    pylab.show()


def open_file():
    """Opens file for reading, prompts until successful"""

    LOWER_YEAR_LIMIT = 1990
    UPPER_YEAR_LIMIT = 2019

    # User Input Loop
    while True:

        try:
            # User input
            year_int = int(input("Choose year: 2000, 2014, or 2019:"))

            # Check if between 1990 and 2019
            if year_int <= UPPER_YEAR_LIMIT and year_int >= LOWER_YEAR_LIMIT:

                file_str = 'year' + str(year_int) + ".txt"

                # Open data file ‘yearXXXX.txt’
                file_pointer = open(file_str, 'r', encoding="utf8")

            else:
                print("Error in year. Please try again.")
                continue

            break

        # File doesn't exist
        except IOError:

            print("Error in file name:", file_str, " Please try again.")

        # Incorrect input type
        except ValueError:
            print("Error in year. Please try again.")
            continue

    return file_pointer, year_int


def handle_commas(s, T):
    '''Converts strings to ints/floats, removes commas, ignores strings'''

    # Remove Commas
    format_list = s.split(",")
    format_str = "".join(format_list)

    # Convert string to int
    if T == "int":
        try:
            out_int = int(format_str)
            return out_int
        except ValueError:
            return None

    # Convert string to float
    if T == "float":
        try:
            out_float = float(format_str)
            return out_float
        except ValueError:
            return None


def read_file(fp):
    '''Read each line, extract columns 1-7, return master list'''

    # Skip Headers
    fp.readline()
    fp.readline()

    # Read each line, format and extract data
    master_list = []
    for line in fp:
        line_list = line.split()

        # Handle commas, convert to ints and floats for elements in line_list
        count = 0
        for num in line_list:

            if count == 3 or count == 4:
                line_list[count] = handle_commas(num, "int")
            else:
                line_list[count] = handle_commas(num, "float")

            count += 1

        # Extract Coumns 1 through 7
        interval_tuple = line_list[0], line_list[2]

        # Make space for and append interval_tuple to line_list
        line_list.pop(2)
        line_list[0] = interval_tuple

        # Get Rid of weird character (now a NoneType)
        line_list.pop(1)

        line_tup = tuple(line_list)
        master_list.append(line_tup)

    # Return list of tuples: ((float, float), int, int, float, float, float)
    # ((column 0, column 2), column 3, column 4, column 5, column 6, column 7)
    return master_list


def find_average(data_lst):
    '''Calculates the average salary'''

    # Last line column 3 (index 2) is cumulative people surveyed
    total_people = data_lst[-1][2]

    total_money = 0
    for line in data_lst:
        total_money += line[-2]

    avg = total_money/total_people

    # Round to 2 decimals (cents) before returning
    return round(avg, 2)


def find_median(data_lst):
    '''Find average income of range closest to 50% of total population'''

    for line in data_lst:
        # Returns average income of first range to exceed 50% of the population
        if line[3] >= 50:
            # Line 5 = column 7, average income
            return line[5]


def get_range(data_lst, percent):
    '''Finds income bracket closest to given percent of population'''

    for line in data_lst:
        # Selects first percentage close to percent
        if line[3] >= percent:
            # Range, percent, average income
            return line[0], line[3], line[5]


def get_percent(data_lst, salary):
    '''Finds income bracket containing given salary'''

    for line in data_lst:
        # Checks if salary is within range boundaries
        if line[0][0] <= salary and line[0][1] >= salary:
            # Range, percent
            return line[0], line[3]


def main():

    # Basic prompts and data displays
    fp, year_int = open_file()

    print("For the year {:4d}:".format(year_int))

    master_list = read_file(fp)

    print("The average income was ${:<13,.2f}".format(
        find_average(master_list)))
    print("The median income was ${:<13,.2f}".format(find_median(master_list)))

    check_str = input("Do you want to plot the data (yes/no): ")
    if check_str.lower() == "yes":

        range_list = []
        percentage_list = []
        count = 0

        # Gather x and y values from master_list
        for line in master_list:
            range_list.append(line[0][0])
            percentage_list.append(line[3])

            # Only do first 40 income brackets
            if count == 39:
                break
            count += 1

        do_plot(range_list, percentage_list, year_int)

    # Input loop prompting for either r for range, p for percent, "" for quit
    while True:

        choice_str = input(
            "Enter a choice to get (r)ange, (p)ercent, or nothing to stop: ")

        # Carriage-return is entered, halt the program
        if choice_str == "":
            break

        # Invalid input
        elif choice_str.lower() != "r" and choice_str.lower() != 'p':
            print("Error in selection.")
            continue

        # Finds income range from given percent of population
        elif choice_str.lower() == "r":
            while True:

                percent_str = input("Enter a percent: ")

                # Make sure percent is a number
                percent_check = False
                try:
                    percent = float(percent_str)
                    percent_check = True
                except ValueError:
                    print("Error in percent. Please try again")

                # Make sure percent has correct range
                if percent_check and percent < 100 and percent > 0:

                    # Get range, percentage, average income
                    income_range, percent_out, average_income = get_range(
                        master_list, percent)

                    print("{:4.2f}% of incomes are below ${:<13,.2f}.".format(
                        percent, income_range[0]))

                    # Prompt again at top
                    break

                # Prompt again if wrong percent range but still a number
                elif percent_check:
                    print("Error in percent. Please try again")

        # Find percentage of population lower than given income
        elif choice_str.lower() == "p":
            while True:

                income_str = input("Enter an income: ")

                # Make sure income is a number
                income_check = False
                try:
                    income_int = int(income_str)
                    income_check = True
                except ValueError:
                    print("Error in income. Please try again")

                # Make sure income is positive
                if income_check and income_int > 0:

                    # Call the get_percent(), get cumulative percentage
                    income_range, percent = get_percent(
                        master_list, income_int)
                    print("An income of ${:<13,.2f} is in the top {:4.2f}% \
                          of incomes.".format(income_int, percent))

                    # Prompt again at the top
                    break

                # Prompt again if wrong income but still a number
                elif income_check:
                    print("Error: income must be positive")


if __name__ == '__main__':
    main()

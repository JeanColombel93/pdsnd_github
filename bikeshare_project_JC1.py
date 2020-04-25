import time
import pandas as pd
import numpy as np
import calendar

# Given datasets by Udacity, feel free to add more city files if
# they have the same format.
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

# Get the user Inputs
# Outputs are city, month and day.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    bad_input = True
    while bad_input:
        city = input("Would you like to see the data for Chicago, New York, or Washington?\n").title()
        if city in ["Chicago","New York", "Washington"]:
            bad_input = False
        else:
            print("\nIt seems that you entered a wrong city name...")

    print("")
    # get user inputer for filter (month, day, both or none)
    bad_input = True
    while bad_input:
        filter = input("Would you like to filter the data by month, day, both or not at all?\
 Type \"none\" for no time filter.\n").lower()
        if filter in ["month","day","both","none"]:
            bad_input = False
        else:
            print("\nIt seems that you entered an invalid filter variable name...")

    print("")
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter == 'month':
        day = "all"
        bad_input = True
        while bad_input:
            month = input("Which month? January, February, March, April, May or June?\n").title()
            if month in list(calendar.month_name)[1:7]:
                bad_input = False
            else:
                print("\nPlease enter a valid month")

    elif filter == 'day':
        month = "all"
        bad_input = True
        while bad_input:
            day = input("Which day? Please type the response as an integer (e.g., 0-Monday)\n")
            if len(day.strip()) !=0 and day in str(list(range(0,8))):
                bad_input = False
            else:
                print("\nPlease enter a valid numerical value for the day")

    elif filter == 'both':
        bad_input = True
        while bad_input:
            month = input("Which month? January, February, March, April, May or June?\n").title()
            if month in list(calendar.month_name)[1:7]:
                bad_input = False
            else:
                print("\nPlease enter a valid month")

        print("")

        bad_input = True
        while bad_input:
            day = input("Which day? Please type the response as an integer (e.g., 0-Monday)\n")
            if len(day.strip()) !=0 and day in str(list(range(0,8))):
                bad_input = False
            else:
                print("\nPlease enter a valid numerical value for the day")

    else:
        month = "all"
        day = "all"

    print("\nYou chose to explore the \033[1m{}\033[0m dataset using the \033[1m\"{}\"\033[0m filter for days and months".format(city,filter))
    time.sleep(1.5)
    if filter == 'month' or filter =='both':
        print("You chose to explore the following month: \033[1m{}\033[0m".format(month))
        time.sleep(1.5)
    if filter == 'day' or filter == 'both':
        print("You chose to explore the following day: \033[1m{}\033[0m".format(list(calendar.day_name)[int(day)]))
        time.sleep(1.5)

    print('-'*40)
    return city, month, day

# Load the chosen city/month/day file.
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column at the same time
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = list(calendar.month_name[1:7])
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]

    return df

# Calculate and outputs the time stats
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    #start_time = time.time()

    # display the most common month
    if month == "all":
        most_common_month = df['month'].value_counts().index[0]
        print('Most common month: \033[1m{}\033[0m'.format(list(calendar.month_name)[most_common_month]))

    # display the most common day of week
    if day == "all":
        most_common_day = df['day_of_week'].value_counts().index[0]
        print('Most common day: \033[1m{}\033[0m'.format(list(calendar.day_name)[most_common_day]))

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.value_counts().index[0]
    print('Most common start hour: \033[1m{}h\033[0m'.format(most_common_hour))

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    #start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].value_counts().index[0]
    print("Most commonly used start station: \033[1m{}\033[0m".format(most_common_start))

    # display most commonly used end station
    most_common_end = df['End Station'].value_counts().index[0]
    print("Most commonly used end station: \033[1m{}\033[0m".format(most_common_end))

    # display most frequent combination of start station and end station trip
    start_and_end = df['Start Station'] + " - > " + df['End Station']
    most_common_sae = start_and_end.value_counts().index[0]
    print("Most frequent combination of start station and end station trip:\n \033[1m{}\033[0m".format(most_common_sae))

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    #start_time = time.time()

    Hours = df['End Time'].dt.hour - df['Start Time'].dt.hour
    Minutes = df['End Time'].dt.minute - df['Start Time'].dt.minute
    Seconds = df['End Time'].dt.second - df['Start Time'].dt.second

    Travel_Time = Hours*60 + Minutes + Seconds/60

    # display total travel time
    Total_Travel_Time = int((Travel_Time).sum())
    print("Total travel time:\033[1m ~ {} minutes \033[0m".format(Total_Travel_Time))

    # display mean travel time
    Mean_Travel_Time = int((Travel_Time).mean())
    print("Mean travel time:\033[1m ~ {} minutes \033[0m".format(Mean_Travel_Time))

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    #start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types:')
    for i in range(len(user_types)):
        print("- {}: \033[1m{}\033[0m".format(user_types.index[i], user_types[i]))

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('Gender types:')
        for i in range(len(gender_types)):
            print("- {}: \033[1m{}\033[0m".format(gender_types.index[i], gender_types[i]))

    except:
        print("\nThere is no gender data available in this dataset.")

    # Display earliest, most recent, and most common year of birth
    try:
        DOB = df['Birth Year'].dropna(axis=0)
        DOB = DOB.astype(int)
        most_common_DOB = DOB.value_counts().index[0]

        print("\nYoungest user is born in \033[1m{}\033[0m".format(DOB.max()))
        print("Oldest user is born in \033[1m{}\033[0m".format(DOB.min()))
        print("Most common year of birth is: \033[1m{}\033[0m".format(most_common_DOB))

    except:
        print("There is no birth year data available in this dataset.")

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(city):
    Raw = input("\nWould you like to see the row data ? yes or no. \n")

    if Raw == "yes":
        with open(CITY_DATA[city]) as raw_data:
            read = True
            while read:
                print("")
                for i in range(5):
                    print(raw_data.readline())
                read_decision = input("Would you like to see more rows? yes or no.\n")
                if read_decision.lower() != "yes":
                    read = False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    
    list_cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Which city would you like to analyze?\n")
        if city.lower() in list_cities:
            print("Thank you for your input!\nYou have selected {} for the analysis.\n".format(city.upper()))
            break
        else:
            print("Oops! Please enter a name of one of the folling cities: Chicago, New York City or Washington.\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Please select month you want to analyze? Choices: All, January, February, March, April, May, June:\n")
        if month.lower() in month_options:
            print("Thank you for your input!\nYou have selected {} for the analysis.\n".format(month.upper()))
            break
        else:
            print("Oops! Please try again: 'All' or select one month between January and June.\n")
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please select day you want to analyze? Choices: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday:\n")
        if day.lower() in day_options:
            print("Thank you for your input!\nYou have selected {} for the analysis.\n".format(day.upper()))
            break
        else:
            print("Oops! Please try again: 'All' or select one day between Monday and Sunday.\n")

    # change to lower case
    city = city.lower()
    month = month.lower()
    day = day.lower()

    print('-'*40)
    print('--' + "We're getting the data ready for you" + '--')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data and cast datetime columns    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        list_months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = list_months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def preview_dataframe(df):
    """Prompt user if he/she wants to see preview of dataframe"""
    action = input("\nDo you want to see the first five rows of dataframe? (yes or no):\n")
    if action.lower() == 'yes':
        print(df.head())
        # number of rows already printed (0:4)
        row_start = 0
        row_stop = 4
        
        while True:
            action = input("\nDo you want to see the next five rows of dataframe? (yes or no):\n")
            if action.lower() == 'yes':
                row_start = row_stop + 1
                row_stop += 6
                slice_df = df.iloc[row_start:row_stop, :]
                print(slice_df)
                row_stop -= 1
            else: 
                break
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = df['month'].mode()[0]
    list_months = ['January', 'February', 'March', 'April', 'May', 'June']
    mode_month = list_months[mode_month - 1]
    print("The most common month is: {}".format(mode_month))

    # TO DO: display the most common day of week
    mode_dow = df['day_of_week'].mode()[0]
    print("The most common day of week is: {}".format(mode_dow))

    # TO DO: display the most common start hour
    mode_hour = df['hour'].mode()[0]
    print("The most common hour is: {}".format(mode_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mode_start_station = df['Start Station'].value_counts(sort=True).index[0]
    print("The most commonly used start station is: {}".format(mode_start_station))

    # TO DO: display most commonly used end station
    mode_end_station = df['End Station'].value_counts(sort=True).index[0]
    print("The most commonly used start station is: {}".format(mode_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['combined_start_end'] = df['Start Station'] + "_" + df['End Station']
    mode_combined_stations = df['combined_start_end'].value_counts(sort=True).index[0]
    most_start = mode_combined_stations.split("_")[0] 
    most_end = mode_combined_stations.split("_")[1]
    print("\nThe most frequent combination of start and end station:")
    print("Start station: {}".format(most_start))
    print("End station: {}".format(most_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: {}".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average travel time: {}".format(round(mean_travel_time,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types in this dataframe:")
    print(df['User Type'].value_counts(sort=True))
    print("")

    # TO DO: Display counts of gender
    if 'Gender' in list(df.columns.values):
        print("Counts of gender in this dataframe:")
        print(df['Gender'].value_counts(sort=True))
        print("")
    else:
        print("No gender information in Washington")    

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in list(df.columns.values):
        min_byear = int(df['Birth Year'].min())
        max_byear = int(df['Birth Year'].max())
        mode_byear = int(df['Birth Year'].mode()[0])
        print("\nBirth Year Summary of Bikeshare Users\n")
        print("Earliest birth year is {}".format(min_byear))
        print("Most recent birth year is {}".format(max_byear))
        print("Most common birth year is {}".format(mode_byear))
    else:
        print("\nNo birth year information in Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# main() to run the program
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        preview_dataframe(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# run the program
if __name__ == "__main__":
	main()
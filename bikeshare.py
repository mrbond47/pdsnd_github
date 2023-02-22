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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Which city data would you like to explore? Your options are Chicago, Washington or New York City : ').lower()
        if city in CITY_DATA:
            print("You've selected {} as city \n".format(city))
            break
        else:
            print("{} is an invalid city\n".format(city)) # Print statement when user enters any string not in the city dictionary


    # get user input for month (all, january, february, ... , june)
    #Dictionary used to check users input
    month_dict = {
        'all' : 'all',
        'january' : 1,
        'february' : 2,
        'march': 3,
        'april' : 4,
        'may' : 5,
        'june' : 6,
    }

    while True:
        month_name = input("Enter the month (January - June) you want to filter by OR 'all' if you don't want any month filter : ").lower()
        if month_name in month_dict:
            month = month_dict[month_name] #Using the month_dict dictionary, assign the value of the 'month_name' key entered to the month variable
            print("You've entered {} as month filter\n".format(month_name))
            break
        else:
            print("{} is an invalid month\n".format(month_name))
            

    # get user input for day of week (all, monday, tuesday, ... saturday)
    # There's no data data for Sunday hence the omission 


    day_name_dict = {

    
        'all' : 'all',
        'monday' : 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6
    }

    while True:  
        day_name = input("Please enter the day(Mon-Sat) you want to filter by OR 'all' if you don't want any day filter : ").lower()
        if day_name in day_name_dict:
            day = day_name_dict[day_name]
            print("You've entered {} as day filter".format(day_name))
            break
        else:
            print("{} is invalid\n".format(day_name))
            


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

    df = pd.read_csv(CITY_DATA[city])

    df = df.dropna() # Remove all NaaN values to ensure accurate data calculations and conversations 
    df['Start Time'] = pd.to_datetime(df['Start Time']) # convert the Time columns to datetime data type
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    #Washington is missing the Birth Year column, If statement to prevent the program from crashing
    if city != 'washington':
        df['Birth Year'] = df['Birth Year'].astype('int') #convert birth year to int64 data type
    


    # Check users input to determine which filter to apply
    if month != 'all':
        df = df[df['Start Time'].dt.month == month]

    if day != 'all':
        df = df[df['Start Time'].dt.day_of_week == day]


    """While loop to prompt user to display raw data. The code below ensures only two inputs are valid, exits when he subset dataframe is empty"""

    start_index = 0
    prompts = ('yes','no') #tuple to check that only two possible values are entered by the user


    while True:
        user_prompt = input("Do you want to see 5 lines of raw data? Enter 'yes' or 'no' :").lower()
    
        if user_prompt not in prompts:
            print("You can only enter 'yes' or 'no'\n")
        elif user_prompt == 'no' or df.iloc[start_index:start_index+5, :].empty : 
            break
        elif user_prompt == 'yes':
            print('\n')
            print(df.iloc[start_index:start_index+5, :])
            print('\n')
            start_index = start_index + 5



    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print('The most common month(1=Jan,2=Feb...) for travel is: {}\n'.format(df['Start Time'].dt.month.mode()[0]))

    # display the most common day of week
    print('The most common day of the week(1=Mon,2=Tue...) for travel is: {}\n'.format(df['Start Time'].dt.dayofweek.mode()[0]))

    # display the most common start hour
    print('The most common start hour(24Hr-Time) for travel is: {}\n'.format(df['Start Time'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('The most commonly used start station is : {}\n'.format(df['Start Station'].value_counts().idxmax()))


    # display most commonly used end station

    print('The most commonly used end station is : {}\n'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
   
    print('The most frequent combination of start station and end station trip is : {} respectively\n'.format(df[['Start Station', 'End Station']].value_counts().idxmax()))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print('The total travel time is : {:.2f} hours\n'.format((df['Trip Duration'].sum()) / 3600)) #Convert from seconds to hours


    # display mean travel time

    print('The average travel time is : {:.2f} minutes'.format( (df['Trip Duration'].mean()) * 0.016667)) #Convert from seconds to minutes


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    if city == 'washington':  #The user_stats for washington isn't available, this informs the user so they don't think the data is missing
        print('Unfortunate the user_stats data is not available')
    else:
        print('The count for each user type is: \n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
        print('The count for each gender type is: \n{}\n'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
        print('Birth year details is as follows :\nThe oldest users birth year is {}. \nThe youngest users birth year is {}. \nThe most common birth year is {}'.
              format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
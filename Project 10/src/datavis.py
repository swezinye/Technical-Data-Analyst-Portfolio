import pandas as pd
import matplotlib.pyplot as plt

#Read CSV file
df = pd.read_csv('covid_state_data.csv')

def graph_deaths_by_state(data: pd.DataFrame):
    """
    Takes a dataframe of COVID data, calculates total deaths by state,
    returns a summary dataframe, and saves a column chart.
    """
    # Group by state and sum new_death to get total deaths
    state_deaths = data.groupby('state')['new_death'].sum().reset_index()

    # Rename the column to match requirements
    state_deaths.rename(columns={'new_death': 'tot_death'}, inplace=True)

    # Create the column chart
    plt.figure(figsize=(15, 8))  # Adjust size to fit all states
    plt.bar(state_deaths['state'], state_deaths['tot_death'])

    # Add labels and title
    plt.title('Total COVID-19 Deaths by State')
    plt.xlabel('State')
    plt.ylabel('Total Deaths')

    # Rotate x-axis labels for readability
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Saves the figure
    plt.savefig('deaths_by_state.png')
    # Does not call plt.show()
    plt.close()

    return state_deaths
# Call the function with your dataframe
result = graph_deaths_by_state(df)
print(result)


def graph_deaths_over_time(data: pd.DataFrame):
    """
    Takes a dataframe of COVID data, aggregates deaths over time,
    calculates rolling averages, returns a summary dataframe, and saves an XY scatter diagram.
    """
    # 1. Aggregate new_death by submission_date
    # Grouping by date sums up the new deaths from all states for that specific day
    daily_deaths = data.groupby('submission_date')['new_death'].sum().reset_index()


    # Rename 'new_death' to 'tot_death' as requested for the return value
    daily_deaths.rename(columns={'new_death': 'tot_death'}, inplace=True)

    # Sort by date to ensure rolling calculations are correct
    daily_deaths = daily_deaths.sort_values('submission_date')


    # new_death column
    daily_deaths['ma_7'] = daily_deaths['tot_death'].rolling(window=7).mean()
    daily_deaths['ma_30'] = daily_deaths['tot_death'].rolling(window=30).mean()
    daily_deaths['ma_90'] = daily_deaths['tot_death'].rolling(window=90).mean()


    # 3. Plotting
    plt.figure(figsize=(15, 8))

    # Actual new deaths (points, orange)
    plt.scatter(daily_deaths['submission_date'], daily_deaths['tot_death'],
                color='orange', label='Actual new deaths', alpha=0.6, s=15)

    # 7 day averages (line, dark red)
    plt.plot(daily_deaths['submission_date'], daily_deaths['ma_7'],
             color='darkred', label='7 day average', linewidth=2)

    # 30 day average (line, blue)
    plt.plot(daily_deaths['submission_date'], daily_deaths['ma_30'],
             color='blue', label='30 day average', linewidth=2)

    # 90 day average (line, green)
    plt.plot(daily_deaths['submission_date'], daily_deaths['ma_90'],
             color='green', label='90 day average', linewidth=2)

    # Labels, Title, Legend
    plt.title('COVID-19 New Deaths Over Time with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('New Deaths')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Save the figure
    plt.savefig('deaths_over_time.png')
    plt.close()

    # 4. Return the requested DataFrame columns
    return daily_deaths[['submission_date', 'tot_death']]
# # Call the function with your dataframe
result = graph_deaths_over_time(df)
print(result)


def graph_oregon_death_freq(data: pd.DataFrame):
    """
    Filters for Oregon data, creates a histogram of new deaths with specified bins,
    saves the chart, and returns a frequency table.
    """
    # 1. Filter data for Oregon
    or_data = data[data['state'] == 'OR'].copy()
    new_deaths = or_data['new_death'].values

    # 2. Define Bins
    # Start with fixed bins: 0, 1, 2, 5

    bins = [0, 1, 2, 5,10,20]

    # Calculate the upper limit: smallest multiple of 10 > max(new_death)
    max_death = new_deaths.max()
    # (max // 10 + 1) * 10 gives the next multiple of 10
    #next_multiple_10 = (int(max_death) // 10 + 1) * 10
    #Add multiple of 10 starting from 30
    current = 30
    while current <= max_death +10:
        bins.append(current)
        current += 10

    # print("DEBUG - Generated bins:", bins)  # ADD THIS LINE
    # print("DEBUG - Number of bins:", len(bins))  # ADD THIS LINE

    #Add one final endpoint
    bins.append(current)

    # Add steps of 10 up to that limit
    #bins.extend(range(10, next_multiple_10 + 1, 10))

    # 3. Create Histogram
    plt.figure(figsize=(10, 6))

    # counts = bin frequencies, edges = bin endpoints
    counts, edges, _ = plt.hist(new_deaths, bins=bins, edgecolor='black', color='lightgreen')

    # 4. Formatting
    plt.title('Frequency of New Deaths in Oregon')
    plt.xlabel('Number of New Deaths (Bin Start)')
    plt.ylabel('Frequency (Days)')
    plt.grid(axis='y', alpha=0.3)

    # Save the figure
    plt.savefig('OR_death_freq.png')
    plt.close()

    # 5. Create Return DataFrame
    # 'bin' column is the left endpoint (edges[:-1])
    # 'tot_death' column is the count in that bin (counts)
    result_df = pd.DataFrame({
        'bin': edges[:-1].astype(float), #convert to float
        'tot_death': counts.astype(float) # convert to float
    })

    return result_df
# Call the function with your dataframe
result = graph_oregon_death_freq(df)
print(result)

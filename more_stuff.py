import pandas as pd
import numpy as np

# Sample data
data = {
    'name': ['John', 'Steve', 'Lucy', 'Anna', 'Mike', 'Eva', 'Tom', 'Jess', 'Will', 'Oscar',
             'Emma', 'Chloe', 'Ethan', 'Sophia', 'Ben', 'Liam', 'Mila', 'Nina', 'Ryan', 'Zoe',
             'Harry', 'Ava', 'Leo', 'Grace', 'Luna'],
    'plane_type': ['Boeing', 'Airbus', 'Boeing', np.nan, 'Airbus', 'Boeing', 'Airbus', np.nan, 'Boeing', 'Airbus',
                   'Boeing', 'Airbus', 'Boeing', 'Airbus', np.nan, 'Boeing', 'Airbus', 'Boeing', 'Airbus', 'Boeing',
                   'Airbus', 'Boeing', np.nan, 'Airbus', 'Boeing'],
    'specific_plane_type': ['737', 'A320', '747', 'A380', np.nan, '737', 'A320', '747', np.nan, '737',
                            'A320', '747', 'A380', '737', 'A320', '747', np.nan, '737', 'A320', '747',
                            'A380', '737', 'A320', '747', 'A380'],
    'fuel': [np.nan, 'Jet A-1', 'Jet A-1', 'Jet A-1', 'JP8', np.nan, 'Jet A-1', 'JP8', 'Jet A-1', 'JP8',
             'Jet A-1', 'JP8', 'Jet A-1', np.nan, 'JP8', 'Jet A-1', 'JP8', 'Jet A-1', 'JP8', 'Jet A-1',
             'JP8', 'Jet A-1', 'JP8', 'Jet A-1', 'JP8'],
    'callsign': ['Alpha', np.nan, 'Bravo', 'Charlie', 'Delta', 'Echo', np.nan, 'Foxtrot', 'Golf', 'Hotel',
                 'India', 'Juliet', 'Kilo', 'Lima', np.nan, 'Mike', 'November', 'Oscar', 'Papa', 'Quebec',
                 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor'],
    'drops': [4, np.nan, 3, 5, np.nan, 2, 4, 1, 3, np.nan, 3, 4, 2, np.nan, 5, 4, 1, 3, 5, 2,
              4, 3, 2, 1, 5]
}

df = pd.DataFrame(data)

# Calculate percentage of populated fields for each combination


def calc_percentage(group):
    return (1 - group.isna().mean()) * 100


result = df.groupby(['plane_type', 'specific_plane_type'],
                    dropna=False).apply(calc_percentage)

# Printing the result
print(result)

# Fetch the percentage values for 'Airbus' and '737'
try:
    percentages = result.loc[('Airbus', '737')]
    print(percentages['fuel'])
    combined_percentage = percentages.mean()

    print(
        f"The average percentage of populated fields for Airbus 737 is {combined_percentage:.2f}%.")
except KeyError:
    print("There is no data for the combination Airbus 737.")

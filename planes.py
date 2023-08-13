import pandas as pd


df = pd.read_csv('planes.csv')
# Assuming df is your DataFrame
unique_models = df['plane_model'].unique()

for model in unique_models:
    model_data = df[df['plane_model'] == model]
    
    # Drop the 'plane_model' column as we're examining the other columns
    model_data = model_data.drop(columns=['plane_model'])
    
    # Finding the percentage of non-null values for each column
    percentages = model_data.notnull().mean() * 100
    
    print(f"Model: {model}")
    for column, percentage in percentages.items(): # Using items() instead of iteritems()
        print(f"		{column}: {percentage}%")

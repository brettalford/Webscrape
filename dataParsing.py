import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#file path
file_path = 'headlines_sentiment.csv'

#reading file values and storing rows in the correct way
with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    headers = next(reader)
    sorted_rows = sorted(reader, key=lambda row: int(row[5]))  # Absolute Time column

with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers)
    writer.writerows(sorted_rows)


#reading csv with pandas
df = pd.read_csv('headlines_sentiment.csv')

df['Absolute Time'] = pd.to_numeric(df['Absolute Time'], errors='coerce')
df['Sentiment Score'] = pd.to_numeric(df['Sentiment Score'], errors='coerce')

# group by Absolute Time and average sentiment scores
grouped = df.groupby('Absolute Time')['Sentiment Score'].mean().reset_index()

plt.scatter(grouped['Absolute Time'], grouped['Sentiment Score'], label='Average Sentiment')

# Best fit line
x = grouped['Absolute Time']
y = grouped['Sentiment Score']
slope, intercept = np.polyfit(x, y, 1)
best_fit_line = slope * x + intercept
plt.plot(x, best_fit_line, color='blue', label='Best Fit Line')

# Labels and grid
plt.xlabel("Time")
plt.ylabel("Average Sentiment Score")
plt.title("News sentiment over time")
plt.grid(True)
plt.show()




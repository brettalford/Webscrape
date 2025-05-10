import csv
import pandas as pd
import matplotlib.pyplot as plt


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

# plot the average sentiment over absolute time
#kind='scatter',
grouped.plot( x='Absolute Time', y='Sentiment Score')
plt.xlabel("Time")
plt.ylabel("Average Sentiment Score")
plt.grid(True)
plt.show()

#df.plot(kind='scatter', x=5, y=2)
#plt.show()



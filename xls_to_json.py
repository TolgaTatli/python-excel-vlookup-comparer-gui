import pandas as pd
import json

dataframe1 = pd.read_excel('file1.xlsx')
dataframe2 = pd.read_excel('file2.xlsx')
print("Dataframe1")
print(dataframe1.to_json(orient='records'))
print("\n")

print("Dataframe2")
print(dataframe2.to_json(orient='records'))
print("\n")
# Select the columns to compare from the two files
column1 = 'Column1'
column2 = 'Column2'

# Convert the JSON data to lists based on the selected columns
data1 = json.loads(dataframe1.to_json(orient='records'))
data2 = json.loads(dataframe2.to_json(orient='records'))

print("Data1")
print(data1)
print("\n")

list1 = [str(record.get(column1, '')).strip() for record in data1]  # buradaki column1 hangi satır olduğunu söylüyor
list2 = [str(record.get(column1, '')).strip() for record in data2]

print(list1)
print(list2)

# Compare the two lists and find the unique values
# Output şu şekilde olacak : file1.xlsx'te olup file2.xlsx'te olmayanlar ve file2.xlsx'te olup file1.xlsx'te olmayanlar

set1 = set(list1)
set2 = set(list2)

unique_in_file1 = set1 - set2

unique_in_file2 = set2 - set1

print("\nContents of the first file (unique values):")

for value in unique_in_file1:
    print(value)

print("\nContents of the second file (unique values):")

for value in unique_in_file2:

    print(value)


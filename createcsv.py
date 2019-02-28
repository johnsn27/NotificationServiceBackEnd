import csv
 
with open('users.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['field1', 'field2'])
    filewriter.writerow(['row1 column1', 'row1 column2'])
import hungarian

tasks = ['wash car', 'change light bulb', 'wash dishes', 'laundry']
workers = ['Rochelle', 'Sarah', 'Steph', 'Soph', 'Nikki', 'Matt']
# construct a 2d list that represents the cost of assigning each person to a
# job
#      task
# w  5  9  3  6
# o  8  7  8  2
# r  6 10 12  7
# k  3 10  8  6
# e  4  5 10  5
# r  5 15 5   2
grid = [[5, 9, 3, 6], 
        [8, 7, 8, 2], 
        [6, 10, 12, 7], 
        [3, 10, 8, 6], 
        [4, 5, 10, 5], 
        [5, 15, 5, 2]]

total, coordinates = hungarian.minimize(grid)
print "The optimal assignment to *minimize* the amount of hours to complete all tasks is", total
for (row, col) in coordinates:
    print "Assign", tasks[col], "to", workers[row]


total, coordinates = hungarian.maximize(grid)
print "The optimal assignment to *maximize* the amount of hours to complete all tasks is", total
for (row, col) in coordinates:
    print "Assign", tasks[col], "to", workers[row]

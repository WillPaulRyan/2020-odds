# Initialize new list
A = {'datetime': '2019-04-25 15:31:48', 'trump': 135, 'warren': 4950, 'booker': 14400, 'biden': 925, 'sanders': 710, 'klobuchar': 9400, 'harris': 1350, 'gillibrand': 30900, 'gabbard': 8900, 'orourke': 2450, 'yang': 3300, 'buttigieg': 1250, 'castro': 69900}

for thing in A:
    try:
        if A[thing] >= 0:
            A[thing] = '+' + str(A[thing])
        else:
            A[thing] = str(A[thing])
    except:
        pass
print (A)

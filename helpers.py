from datetime import datetime
from operator import itemgetter

def candidateSort(A):
    """Sort the candidates by probability and add information"""

    B = [['./static/candidates/trump.png', 'Donald Trump', A[1]], ['./static/candidates/warren.png', 'Elizabeth Warren', A[2]], ['./static/candidates/booker.png', 'Cory Booker', A[3]], ['./static/candidates/biden.png', 'Joe Biden', A[4]], ['./static/candidates/sanders.png', 'Bernie Sanders', A[5]], ['./static/candidates/klobuchar.png', 'Amy Klobuchar', A[6]], ['./static/candidates/harris.png', 'Kamala Harris', A[7]], ['./static/candidates/gillibrand.png', 'Kirsten Gillibrand', A[8]], ['./static/candidates/gabbard.png', 'Tulsi Gabbard', A[9]], ['./static/candidates/orourke.png', "Beto O'Rourke", A[10]], ['./static/candidates/yang.png', 'Andrew Yang', A[11]], ['./static/candidates/buttigieg.png', 'Pete Buttigieg', A[12]], ['./static/candidates/castro.png', 'Julian Castro', A[13]]]

    return A[0], sorted(B, key=itemgetter(2))


def convertToStrings(A):
    """Convert list of ints into proper odds-formatted strings"""

    for candidate in A:
        if candidate[2] >= 0:
            candidate[2] = '+' + str(candidate[2])
        else:
            candidate[2] = str(candidate[2])
    return A


def timeConvert(time):
    """Convert time to a better format"""

    FMTin = '%Y-%m-%d %H:%M:%S'
    FMTout = '%m/%d/%y'

    return datetime.strftime(datetime.strptime(time, FMTin), FMTout)


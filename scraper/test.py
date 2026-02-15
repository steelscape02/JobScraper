# Python 3 program for the 
# haversine formula
import math

# Python 3 program for the
# haversine formula
def haversine(lat1, lon1, lat2, lon2):
    
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) + 
         pow(math.sin(dLon / 2), 2) * 
             math.cos(lat1) * math.cos(lat2));
    rad = 3958.8
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

# Driver code
if __name__ == "__main__":
    lat1 = 43.7225626
    lon1 = -111.0502622
    lat2 = 43.846601
    lon2 = -111.774011
    
    print(haversine(lat1, lon1,lat2, lon2), "mi")

# This code is contributed 
# by ChitraNayal
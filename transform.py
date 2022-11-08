import csv
import requests
import io
import numpy as np
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# this is to test

# Classes to hold the data
class Meteorite:
    def __init__(self, row):
        # Parse earthquake data from USGS
        #self.timestamp = row[0]
        self.lat = float(row[1])
        self.lon = float(row[2])
        try:
            self.mass = float(row[0])
        except ValueError:
            self.mass = 0


def get_meteorite_data(url):
    # Read CSV earthquake data from USGS
    response = requests.get(url)
    csvio = io.StringIO(response.text)
    reader = csv.reader(csvio)
    header = next(reader)
    meteo = [Meteorite(row) for row in reader]
    meteo = [m for m in meteo if m.mass > 0]
    return meteo


# control marker color and size based on magnitude
def get_marker(magnitude):
    markersize = magnitude * 1;
    if magnitude < 100.0:
        return ('bo'), markersize
    if magnitude < 1000.0:
        return ('go'), markersize
    elif magnitude < 10000.0:
        return ('yo'), markersize
    else:
        return ('ro'), markersize


def create_png(url, outfile):
    meteos = get_meteorite_data('https://github.com/devcmddef/meteorite/blob/main/mass_cor.csv')
    print(meteos[0].__dict__)

    # Set up Basemap
    mpl.rcParams['figure.figsize'] = '16, 12'
    m = Basemap(projection='kav7', lon_0=-90, resolution='l', area_thresh=1000.0)
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='0.3')
    m.drawparallels(np.arange(-90., 99., 30.))
    junk = m.drawmeridians(np.arange(-180., 180., 60.))

    # sort earthquakes by magnitude so that weaker earthquakes
    # are plotted after (i.e. on top of) stronger ones
    # the stronger quakes have bigger circles, so we'll see both
    #start_day = quakes[-1].timestamp[:10]
    #end_day = quakes[0].timestamp[:10]
    meteos.sort(key=lambda m: m.mass, reverse=True)

    # add earthquake info to the plot
    for q in meteos:
        x, y = m(q.lon, q.lat)
        mcolor, msize = get_marker(q.mass)
        m.plot(x, y, mcolor, markersize=msize)

    # add a title
    plt.title("Meteorites locations" )
    plt.savefig(outfile)


if __name__ == '__main__':
    #url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.csv'
    url = 'https://github.com/devcmddef/meteorite/blob/main/mass_cor.csv'
    outfile = 'meteorites.png'
    create_png(url, outfile)

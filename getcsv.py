import os
import csv
from analyzer import calcular_puntuacion
import glob
import xml

def save_to_csv():

    with open('results_snap.csv', 'a', newline='') as csvfile:
        fieldnames = ['Project', 'Path' ,'Level', 'Score', 'Average', 'Conditional',
                      'Synchronization', 'Flow Control', 'Abstraction', 'Parallelism',
                      'Diversity', 'User Interactivity', 'Data']
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fieldnames)
        for filename in glob.glob("/media/rcruiz/TOSHIBA EXT/snap_projects/snap-projects/**/**/project.xml", recursive=False):
            writer.writerow(calcular_puntuacion(filename))


if __name__ == "__main__":

    save_to_csv()

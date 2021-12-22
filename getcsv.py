import csv
from analyzer import calcular_puntuacion
import glob


PATH = "/media/rcruiz/TOSHIBA EXT/snap_projects/snap-projects/**/**/project.xml"
PATH2 = "/home/rcruiz/Downloads/prueba_snap/**/**/project.xml"
# PATH3 = "/home/rcruiz/Downloads/prueba_snap2/2141/**/project.xml"


def save_to_csv():
    with open('result_snap_metrics.csv', 'a', newline='') as csvfile:
        fieldnames = ['Project', 'Path', 'Level', 'Total', 'Average', 'Conditional',
                      'Synchronization', 'Flow Control', 'Abstraction', 'Parallelism',
                      'User Interactivity', 'Data']
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fieldnames)
        for filename in glob.glob(PATH, recursive=False):
            writer.writerow(calcular_puntuacion(filename))


if __name__ == "__main__":

    save_to_csv()

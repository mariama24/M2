#!/bin/env python3

#!/bin/env python3

import os
import sys
import time
import importlib
import glob
import multiprocessing
import matplotlib.pyplot as plt

class MyProcess(multiprocessing.Process):
    def __init__(self, fichiers, total_processors, results_queue):
        multiprocessing.Process.__init__(self)
        self.fichiers = fichiers
        self.total_processors = total_processors
        self.results_queue = results_queue

    def run(self):
        for fichier in self.fichiers:
            self.Jobs(fichier)

    def Jobs(self, chemin_jobs):
        nom_jobs = chemin_jobs[:-3]

        job_mod = importlib.import_module(nom_jobs)
        start_time = time.time()

        try:
            result = str(job_mod.run())
        except Exception as ex:
            result = f"Exception : {str(ex)}\nStatut : Exception\n"

        resu = job_mod.__name__ + '.result'

        try:
            with open(resu, 'w') as res_f:
                res_f.write(result)
        except Exception as ex:
            e = ex
            with open(resu, 'w') as res_f:
                res_f.write(f"Exception : {str(ex)}\n")
                res_f.write("Statut : Exception\n")

        end_time = time.time()

        with open(f"log_fichiers_{self.total_processors}_procs.log", 'a') as le:
            le.write(f"nom_fichier: {nom_jobs},\tTemps d'exécution : {end_time - start_time}\n")
            le.write(f"Processeur : {multiprocessing.current_process().name.split('-')[1]}/{self.total_processors}\n")
            if 'ex' in locals():
                le.write("Statut : Exception\n")
                le.write(f"Exception : {str(e)}\n")
            else:
                le.write("Statut : Terminé normalement\n")

        self.results_queue.put(end_time - start_time)

def plot_execution_time(num_processors_list, execution_time_list):
    plt.plot(num_processors_list, execution_time_list, marker='o')
    plt.title('Impact du nombre de cœurs sur le temps d\'exécution')
    plt.xlabel('Nombre de cœurs')
    plt.ylabel('Temps d\'exécution (s)')
    plt.grid(True)
    plt.show()

def main():
    debut = time.time()
    if len(sys.argv) != 3:
        print("Usage: python script.py <nom_dossier>")
        sys.exit(1)

    dir_name = sys.argv[1]
    max_processors = int(sys.argv[2])

    if not os.path.exists(dir_name) or not os.path.isdir(dir_name):
        print(f"Le répertoire {dir_name} n'existe pas.")
        sys.exit(1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    chemin_binome_module = os.path.join(current_dir, dir_name)

    sys.path.insert(0, chemin_binome_module)
    os.chdir(chemin_binome_module)

    fichiers = glob.glob("*.py")
    processes = []
    results_queue = multiprocessing.Queue()
    execution_times = []

    for num_processors in range(1, max_processors + 1):
        start_time = time.time()

        for i in range(num_processors):
            files_for_process = [fichier for j, fichier in enumerate(glob.glob("*.py")) if j % num_processors == i]
            process = MyProcess(files_for_process, num_processors, results_queue)
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

        print(f"Temps d'exécution pour {num_processors} cœurs : {execution_time} secondes")

    plot_execution_time(range(1, max_processors + 1), execution_times)

    #print(time.time() - debut)

if __name__ == "__main__":
    main()

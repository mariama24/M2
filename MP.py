#!/bin/env python3

import os,sys
import time
import importlib
import glob
#import multiprocessing
#from multiprocessing import Pipe



def Jobs(chemin_jobs):
    if not chemin_jobs.endswith(".py"):
        print(chemin_jobs)
        return None
   
    nom_job = chemin_jobs[:-3]
    resu = f"{nom_job}.result"
    start_time= time.time()
    
    # chemin_binome_module = "/users/2024/ds2/121009626/Téléchargements/jobs/modules"
    #sys.path.append(chemin_binome_module)
    try: 
        
        job_mod = importlib.import_module(nom_job)
        resultat = job_mod.run()

        with open(resu, 'w') as res_f:
            res_f.write(str(resultat))
            
    except Exception as ex:
        e=ex
        with open(resu, 'w') as res_f:
            res_f.write(f"Exception : {str(e)}\n")
            res_f.write("Statut : Exception\n")
            
    end_time = time.time()
    
    with open("log_fichiers.log", 'a') as le:
        le.write(f"nom_fichier: {nom_job}, ,\t Temps d'exécution : {end_time-start_time} \n")
        if 'ex' in locals():
            le.write("Statut : Exception\n")
            le.write(f"Exception : {str(e)}\n")
        else:
            le.write("Statut : Terminé normalement\n")

    

if __name__ == "__main__":
    
    dir_name = sys.argv[1]
    if not os.path.exists(dir_name) or not os.path.isdir(dir_name):
        print(f"Directory {dir_name} does not exist.")
        sys.exit(1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    module_folder_name = "modules"
    chemin_binome_module = os.path.join(current_dir, module_folder_name)
    sys.path.append(chemin_binome_module)

    pattern = os.path.join(dir_name, "*.py")
    for fichier in glob.glob(pattern):
        if os.access(fichier, os.X_OK):
            Jobs(os.path.basename(fichier))
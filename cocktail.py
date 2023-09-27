#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:21:48 2023

@author: mmbay
"""
import time,sys

class Accessoire :
    pass
class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents
        et libérer le dernier embroché. """
        
    def __init__(self):
        self.postits = []
        
    def embrocher(self,postit):
        self.postits.append(postit)
        
    def liberer(self):
        if self.postits:
           return self.postits.pop()

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
   
    def __init__(self):
        self.plateaux = []
   
    def recevoir(self,plateau):
        self.plateaux.append(plateau)
        
    def evacuer(self):
        if self.plateaux:
           return self.plateaux.pop()

class Serveur:
    def __init__(self,pic,bar,commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = []
        print(f"[{self.__class__.__name__}] prêt pour le service !")
        time.sleep(1)
        
    def prendre_commande(self,commande):
        """ Prend une commande et embroche un post-it. """
        
        print(f"[{self.__class__.__name__}] je prends la commande de '{commande}'")
        time.sleep(2)
        self.commandes.append(commande)
        self.pic.embrocher(commande)
        time.sleep(1)
        
              
        
    def servir(self):
        """ Prend un plateau sur le bar. """
        if self.commandes:
            commande = self.commandes.pop()
            self.bar.recevoir(commande)
            print(f"[{self.__class__.__name__}] je sers '{commande}'")
        

class Barman:
    def __init__(self,pic,bar):
        self.pic = pic
        self.bar = bar
        print(f"[{self.__class__.__name__}] prêt pour le service !")
        time.sleep(1)
        
    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        if self.pic.postits:
            commande = self.pic.liberer()
            time.sleep(1)
            print(f"[{self.__class__.__name__}] je commence la fabrication de {commande}")
            time.sleep(2)
            print(f"[{self.__class__.__name__}] je termine la fabrication de {commande}")
            self.bar.recevoir(commande)
        

        
if __name__ == "__main__":
    pic = Pic()
    bar = Bar()
    # commandes = sys.argv[1:]
    #serveur = Serveur(pic, bar,commandes)
    barman = Barman(pic, bar)
    serveur = Serveur(pic, bar,[])
    #print("[Barman] prêt pour le service !")
    #print("[Serveur] prêt pour le service")
    

    commandes = sys.argv[1:]
    for commande in commandes:
        serveur.prendre_commande(commande)
    print("[Serveur] il n'y a plus de commande à prendre")

    
        
    # if not serveur.commandes:
    #     print("[Serveur] il n'y a plus de commande à prendre")

    for _ in range(len(commandes)):
        barman.preparer()

    for _ in range(len(commandes)):
        serveur.servir()
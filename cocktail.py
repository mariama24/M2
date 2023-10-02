#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:21:48 2023

@author: mmbay
"""
import time, sys


# Niveaux de verbosité
verbosite_0 = 0
verbosite_1 = 1
verbosite_2 = 2

# Variable globale pour le niveau de verbosité actuel
actuel_verbosite = verbosite_0

# Fonction de gestion de la verbosité
def verbosity(verbosity_level):
    global actuel_verbosite
    actuel_verbosite = verbosity_level

# Fonction pour envoyer des messages avec gestion de la verbosité
def send_message(message, verbosity_level=verbosite_0):
    if verbosity_level <= actuel_verbosite:
        print(message)

class Accessoire:
    pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents
        et libérer le dernier embroché. """

    def __init__(self):
        self.postits = []

    def embrocher(self, postit):
        self.postits.append(postit)
        send_message(f"[{self.__class__.__name__}] post-it '{postit}' embroché")

    def liberer(self):
        if self.postits:
            return self.postits.pop()

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """

    def __init__(self):
        self.plateaux = []

    def recevoir(self, plateau):
        self.plateaux.append(plateau)
        send_message(f"[{self.__class__.__name__}] '{plateau}' reçu")

    def evacuer(self):
        if self.plateaux:
            plateau = self.plateaux.pop()
            send_message(f"[{self.__class__.__name__}] '{plateau}' évacué")
            return plateau

class Serveur:
    def __init__(self, pic, bar, commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = []
        send_message(f"[{self.__class__.__name__}] prêt pour le service !")
        time.sleep(1)

    def prendre_commande(self, commande):
        """ Prend une commande et embroche un post-it. """
        send_message(f"[{self.__class__.__name__}] je prends la commande de '{commande}'")
        time.sleep(1)
        self.commandes.append(commande)
        self.pic.embrocher(commande)
        time.sleep(1)

    def servir(self):
        """ Prend un plateau sur le bar. """
        if self.commandes:
            commande = self.commandes.pop()
            #self.bar.recevoir(commande)
            #print(f"[{self.__class__.__name__}] je sers '{commande}'")

class Barman:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar
        send_message(f"[{self.__class__.__name__}] prêt pour le service ")
        time.sleep(1)

    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        if self.pic.postits:
            commande = self.pic.liberer()
            time.sleep(1)
            #send_message(f"[Pic] état={self.pic.postits}")
            send_message(f"[Pic] post-it '{commande}' libéré")
            send_message(f"[{self.__class__.__name__}] je commence la fabrication de {commande}")
            time.sleep(2)
            send_message(f"[{self.__class__.__name__}] je termine la fabrication de {commande}")
            self.bar.recevoir(commande)

if __name__ == "__main__":
    verbosity(verbosite_0)
    pic = Pic()
    bar = Bar()

    barman = Barman(pic, bar)
    serveur = Serveur(pic, bar, [])
    

    commandes = sys.argv[1:]
    for commande in commandes:
        serveur.prendre_commande(commande)
        send_message(f"[Pic] état={pic.postits}")
        
    send_message("[Serveur] il n'y a plus de commande à prendre")
    send_message(f"[Pic] état={pic.postits}")

    for _ in range(len(commandes)):
        barman.preparer()
        send_message(f"[Bar] état={bar.plateaux}")
        send_message(f"[Pic] état={pic.postits}")
        
   
    send_message("[Pic] est vide")
    send_message(f"[Bar] état={bar.plateaux}")
    
    for _ in range(len(commandes)):
        plateau = bar.evacuer()
        serveur.servir()
        print(f"[Serveur] je sers '{plateau}'")
        print(f"[Bar] état={bar.plateaux}")

    send_message("Bar est vide")
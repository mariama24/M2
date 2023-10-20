#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:22:39 2023

@author: mariamadiabymbaye
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 20:56:05 2023

@author: mariamadiabymbaye
"""

# =============================================================================
#  Version  avec fonction encaisser du barman
# =============================================================================
import time
import sys
import asyncio
import threading
import queue

class Accessoire:
    pass

class Pic(Accessoire):
    
    def __init__(self, verbosite=0):
        self.postits = queue.LifoQueue()
        self.verbosite = verbosite

    async def embrocher(self, postit):
        self.postits.put(postit)
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] post-it '{postit}' embroché")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] etat={list(self.postits.queue)}")

    async def liberer(self):
        postit = self.postits.get()
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] post-it '{postit}' libéré")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.3f}s] [{self.__class__.__name__}] etat = {list(self.postits.queue)}")
        return postit

class Bar(Accessoire):
    
    def __init__(self, verbosite=0):
        self.plateaux = asyncio.LifoQueue()
        self.verbosite = verbosite

    async def recevoir(self, plateau):
        await self.plateaux.put(plateau)
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] '{plateau}' reçu")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] etat={list(self.plateaux._queue)}")

    async def evacuer(self):
        plateau = await self.plateaux.get()
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] '{plateau}' évacué")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] etat={list(self.plateaux._queue)}")
        return plateau

class Serveur(threading.Thread):
    
    def __init__(self, pic, bar, commandes, verbosite=0):
        threading.Thread.__init__(self)
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        self.verbosite = verbosite
        print(f" [{time.time() - debut:.2f}s] [{self.__class__.__name__}] prêt pour le service")

    async def prendre_commande(self):
        global service_prendre_commande
        for k in range(len(self.commandes)-1, -1, -1):
            print(f"[{time.time() - debut:.3f}s] [{self.__class__.__name__}] je prends commande de '{self.commandes[k]}'")
            await self.pic.embrocher(self.commandes[k])
            await asyncio.sleep(3)
            self.commandes.pop()
        print(f"[{time.time() - debut:.3f}s] [{self.__class__.__name__}] il n'y a plus de commandes à prendre.")
        service_prendre_commande = False
        if self.verbosite >= 2:
            print(f"[{time.time() - debut:.3f}s] [{Pic.__name__}] etat = {list(self.pic.postits.queue)}")

    async def servir(self):
        global servir_commande 
        while True:
            commande = await self.bar.evacuer() # on enlève le plateau avec la commande du bar 
            print(f" [{time.time() - debut:.2f}s] [{self.__class__.__name__}] je sers '{commande}'")
            await asyncio.sleep(2)
            if self.verbosite == 2:
                print(f"[{time.time() - debut:.3f}s] [{Bar.__name__}] etat = {list(self.bar.plateaux._queue)}")
            if self.bar.plateaux.empty() and not prepare_commande:
                break
        print(f"[{time.time() - debut:.2f}s] Bar est vide")
        servir_commande = False
        
        
    def run(self):
        async def main():
            async with asyncio.TaskGroup() as tg:
                task1 = tg.create_task(self.prendre_commande())
                task2 = tg.create_task(self.servir())
        asyncio.run(main())
        
        
        

class Barman(threading.Thread):
    
    def __init__(self, pic, bar, verbosite):
        threading.Thread.__init__(self)
        self.pic = pic
        self.bar = bar
        self.verbosite = verbosite
        self.commandes_a_encaisser = asyncio.LifoQueue()
        print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] prêt pour le service!")

    async def preparer(self):
        global prepare_commande
        while not self.pic.postits.empty() or service_prendre_commande:
            postit = await self.pic.liberer()
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] je commence la fabrication de {postit}")
            await asyncio.sleep(3)
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] je termine la fabrication de {postit}")
            await self.bar.recevoir(postit)
            #await asyncio.sleep(0.5)
            await self.commandes_a_encaisser.put(postit)
            if self.verbosite == 2:
                print(f"[{time.time() - debut:.3f}s] [{Pic.__name__}] etat = {list(self.pic.postits.queue)}")
        print(f"[{time.time() - debut:.3f}s] le pic est vide!")
        prepare_commande = False

    async def encaisser(self):
        while servir_commande == True or not self.commandes_a_encaisser.empty():
            postit = await self.commandes_a_encaisser.get()  # Attend une commande de la file d'attente
            await asyncio.sleep(4)
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] j'encaisse la commande {postit}")
        await asyncio.sleep(2)
        print(f"[{time.time() - debut:.2f}s] Fin du service ")
        
        
    def run(self):
        async def main():
            async with asyncio.TaskGroup() as tg:
                task1 = tg.create_task(self.preparer())
                task2 = tg.create_task(self.encaisser())
        asyncio.run(main())
            

if __name__ == "__main__":
    
    verbose = int(input("Entrer le niveau de verbosité : 0, 1 ou 2 ?"))
    
    global debut
    debut = time.time()
    global prepare_commande
    prepare_commande = True
    global service_prendre_commande
    service_prendre_commande = True
    global servir_commande
    servir_commande = True
    
    pic = Pic(verbose)
    bar = Bar(verbose)
    commandes = sys.argv[1:]
    barman = Barman(pic, bar, verbose)
    serveur = Serveur(pic, bar, commandes, verbose)

    

    serveur.start()
    barman.start()
    
    serveur.join()
    barman.join()
    
import time
import sys
import asyncio
import threading

class Accessoire:
    pass

class Pic(Accessoire):
    
    def __init__(self, verbosite=0):
        self.postits = asyncio.LifoQueue()
        self.verbosite = verbosite

    async def embrocher(self, postit):
        await self.postits.put(postit)
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] post-it '{postit}' embroché")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] etat={list(self.postits._queue)}")

    async def liberer(self):
        postit = await self.postits.get()
        if self.verbosite >= 1:
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] post-it '{postit}' libéré")
        if self.verbosite == 2:
            print(f"[{time.time() - debut:.3f}s] [{self.__class__.__name__}] etat = {list(self.postits._queue)}")
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
            await asyncio.sleep(2)
            self.commandes.pop()
        print(f"[{time.time() - debut:.3f}s] [{self.__class__.__name__}] il n'y a plus de commandes à prendre.")
        service_prendre_commande = False
        if self.verbosite >= 2:
            print(f"[{time.time() - debut:.3f}s] [{Pic.__name__}] etat = {list(self.pic.postits._queue)}")

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def main():
            await self.prendre_commande()
            await self.servir()
        loop.run_until_complete(main())
        
    # def run(self):
    #     async def main():
    #         prepare_commande_task = asyncio.create_task(self.prendre_commande())
    #         servir_task = asyncio.create_task(self.servir())
    #         await asyncio.gather(prepare_commande_task,servir_task)
    #     asyncio.run(main())

class Barman(threading.Thread):
    
    def __init__(self, pic, bar, verbosite):
        threading.Thread.__init__(self)
        self.pic = pic
        self.bar = bar
        self.verbosite = verbosite
        self.commandes_a_encaisser = asyncio.Queue()
        print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] prêt pour le service!")
        
    

    async def preparer(self):
        global prepare_commande
        while not self.pic.postits.empty() or service_prendre_commande:
            postit = await self.pic.liberer()
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] je commence la fabrication de {postit}")
            await asyncio.sleep(3)
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] je termine la fabrication de {postit}")
            await self.bar.recevoir(postit)
            await self.commandes_a_encaisser.put(postit)
            if self.verbosite == 2:
                print(f"[{time.time() - debut:.3f}s] [{Pic.__name__}] etat = {list(self.pic.postits._queue)}")
        print(f"[{time.time() - debut:.3f}s] le pic est vide!")
        prepare_commande = False

    async def encaisser(self):
        while servir_commande == True or not self.commandes_a_encaisser.empty():
            postit = await self.commandes_a_encaisser.get()  # Attend une commande de la file d'attente
            await asyncio.sleep(3)
            print(f"[{time.time() - debut:.2f}s] [{self.__class__.__name__}] j'encaisse la commande {postit}")
        await asyncio.sleep(2)
        print(f"[{time.time() - debut:.2f}s] Fin du service ")
        
        
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def main():
            preparer_task = asyncio.create_task(self.preparer())
            encaisser_task = asyncio.create_task(self.encaisser())
            await asyncio.gather(preparer_task,encaisser_task)
        loop.run_until_complete(main())
    
    

if __name__ == "__main__":
    global debut
    debut = time.time()
    global prepare_commande
    prepare_commande = True
    global service_prendre_commande
    service_prendre_commande = True
    global servir_commande
    servir_commande = True

    verbose = int(input("Entrer le niveau de verbosité : 0, 1 ou 2 ?"))
    pic = Pic(verbose)
    bar = Bar(verbose)
    commandes = sys.argv[1:]
    barman = Barman(pic, bar, verbose)
    serveur = Serveur(pic, bar, commandes, verbose)

    # prendre_commande_task = asyncio.create_task(serveur.prendre_commande())
    # preparer_task = asyncio.create_task(barman.preparer())
    # servir_task = asyncio.create_task(serveur.servir())
    # encaisser_task = asyncio.create_task(barman.encaisser())

    # await asyncio.gather(prendre_commande_task, preparer_task, servir_task, encaisser_task)

    serveur.start()
    barman.start()
    
    serveur.join()
    barman.join()
    
    
    

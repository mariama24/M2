#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:02:26 2023

@author: mmbay
"""

def read_file(file_path):
    # Lire le fichier et construire le réseau de pages
    pages = {}
    with open(file_path, 'r') as file:
        for line in file:
            source, target = map(int, line.strip().split())
            if source not in pages:
                pages[source] = {'outlinks': [], 'inlinks': [], 'weight': 0}
            pages[source]['outlinks'].append(target)
            if target not in pages:
                pages[target] = {'outlinks': [], 'inlinks': [], 'weight': 0}
            pages[target]['inlinks'].append(source)
    return pages

def pagerank(pages, c=0.15, iterations=10):
    N = len(pages)
    print(f"nombre total de page : {N}")
    for _ in range(iterations):
        new_weights = {}
        total_weight = 0
        for page in pages:
            new_weight = c / N + (1 - c) * sum(pages[j]['weight'] / max(1, len(pages[j]['outlinks'])) for j in pages[page]['inlinks'])
            new_weights[page] = new_weight
            total_weight += new_weight
        for page in pages:
            if 'inlinks' in pages[page] and not pages[page]['inlinks']:
                # Si la page est pointée par d'autres pages mais n'a aucun lien entrant, attribuer le poids de c/N
                pages[page]['weight'] = c / N
            else:
                # Sinon, utiliser le nouveau poids calculé
                pages[page]['weight'] = new_weights.get(page, c / N)

    print(f"Somme des poids à la dernière itération : {total_weight}")


def main():
    file_path = 'soc-Epinions1.txt'  # Remplacez avec le chemin vers votre fichier
    pages = read_file(file_path)
    pagerank(pages, c=0.15, iterations=10)

    # Trier les pages par PageRank (ordre décroissant)
    sorted_pages = sorted(pages.items(), key=lambda x: x[1]['weight'], reverse=True)

    # Afficher les 5 premières pages avec les meilleurs PageRank
    print("Top 5 pages avec les meilleurs PageRank:")
    for page, data in sorted_pages[:5]:
        print(f"Page {page}: PageRank = {data['weight']}")

if __name__ == "__main__":
    main()



#soc-Epinions1.txt
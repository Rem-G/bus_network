#!/usr/bin/python
# -*- coding: utf-8 -*-
 
 
"""
Quelques fonctions python utiles ici :
 
- on va rentrer un graphe comme un dictionnaire de dictionnaires pour pouvoir pondérer les arêtes:
g = {'a': {'b': 4, 'c': 2},
     'b': {'a' : 4,'d': 5, 'c': 1},
     'c': {'a' : 2, 'b' : 1, 'd' : 8,'e': 10},
     'd': {'b': 5, 'c': 8, 'e': 2},
     'e': {'c': 10, 'd' : 2, 'f': 3},
     'f': {'e' : 3,'d' : 6}}
 
Ainsi, g['a'] est le dictionnaire des voisins avec leurs poids :
 
>>> g['a']
{'c': 2, 'b': 4}
>>> g['a']['b']
4
>>> 'c' in g['a']
True
 
- pour trouver la clé correspondant à la valeur mini d'un dictionnaire, on utilise une syntaxe très pythonesque. Par exemple, pour avoir le voisin le plus proche de 'a' :
 
>>> min(g['a'], key = g['a'].get)
'c'
 
- dict.get(cle,defaut) : retourne la valeur de cle si elle se trouve dans le dictionnaire et defaut sinon ;
 
- float('inf') représente l'infini
 
"""
 
 
 
 
def affiche_peres(pere,depart,extremite,trajet):
    """
    À partir du dictionnaire des pères de chaque sommet on renvoie
    la liste des sommets du plus court chemin trouvé. Calcul récursif.
    On part de la fin et on remonte vers le départ du chemin.
    
    """
    if extremite == depart:
        return [depart] + trajet
    else:
        return (affiche_peres(pere, depart, pere[extremite], [extremite] + trajet))
 
def plus_court(graphe,etape,fin,visites,dist,pere,depart):
    """
    Trouve récursivement la plus courte chaine entre debut et fin avec l'algo de Dijkstra
    visites est une liste et dist et pere des dictionnaires 
    graphe  : le graphe étudié                                                               (dictionnaire)
    étape   : le sommet en cours d'étude                                                     (sommet)
    fin     : but du trajet                                                                  (sommet)
    visites : liste des sommets déjà visités                                                 (liste de sommets)
    dist    : dictionnaire meilleure distance actuelle entre départ et les sommets du graphe (dict sommet : int)
    pere    : dictionnaire des pères actuels des sommets correspondant aux meilleurs chemins (dict sommet : sommet)
    depart  : sommet global de départ                                                        (sommet)
    Retourne le couple (longueur mini (int), trajet correspondant (liste sommets)) 
       
    """
    # si on arrive à la fin, on affiche la distance et les peres
    if etape == fin:
       return dist[fin], affiche_peres(pere,depart,fin,[])
    # si c'est la première visite, c'est que l'étape actuelle est le départ : on met dist[etape] à 0
    if  len(visites) == 0 : dist[etape]=0
    # on commence à tester les voisins non visités
    for voisin in graphe[etape]:
        if voisin not in visites:
            # la distance est soit la distance calculée précédemment soit l'infini
            dist_voisin = dist.get(voisin,float('inf'))
            # on calcule la nouvelle distance calculée en passant par l'étape

            print(dist)
            candidat_dist = dist[etape] + graphe[etape][voisin]
            # on effectue les changements si cela donne un chemin plus court
            if candidat_dist < dist_voisin:
                dist[voisin] = candidat_dist
                pere[voisin] = etape
    # on a regardé tous les voisins : le noeud entier est visité
    visites.append(etape)
    # on cherche le sommet *non visité* le plus proche du départ
    non_visites = dict((s, dist.get(s,float('inf'))) for s in graphe if s not in visites)
    noeud_plus_proche = min(non_visites, key = non_visites.get)
    # on applique récursivement en prenant comme nouvelle étape le sommet le plus proche 
    return plus_court(graphe,noeud_plus_proche,fin,visites,dist,pere,depart)
 
def dij_rec(graphe,debut,fin):
    return plus_court(graphe,debut,fin,[],{},{},debut)
 
if __name__ == "__main__":
    g3 = {'a': {'d': 2, 'g': 2},
          'b': {'a' : 1}, 
          'c': {'b' : 1, 'f' : 2, 'g' : 3},
          'd': {'g': 4, 's': 7},
          'e': {'a': 5, 'b' : 3, 'c': 2},
          'f': {'d' : 1,'s' : 6},
          'g': {'f' :4},
          's':{}
    }
    l3,c3 = dij_rec(g3,'e','s')
    print ('Plus court chemin ex3 : ',c3, ' de longueur :',l3)
    g4 = {'a': {'d': 5, 'e': 7, 'b' : 2},
          'b': {'e' : 4, 'c' : 9},
          'c': {'e' : 4, 'g' : 6},
          'd': {'e': 3, 'f': 5},
          'e': {'f': 3, 'g' : 4},
          'f': {'h' : 5},
          'g': {'h' : 3},
          'h': {}
    }
    l4,c4 = dij_rec(g4,'a','h')
    print ('Plus court chemin ex4 : ',c4, ' de longueur :',l4)
 
 
 
"""
Réponse :
Plus court chemin ex3 :  ['e', 'c', 'f', 's']  de longueur : 10
Plus court chemin ex4 :  ['a', 'b', 'e', 'g', 'h']  de longueur : 13
"""


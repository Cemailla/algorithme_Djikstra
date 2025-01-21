import numpy.random as rm
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import copy as cp
import time

###############################################~~ ~~~ LIGNE 560 POUR LES TESTS ~~~ ~~###############################################

#==================================================================================================================================#
#=============================================================== §2 ===============================================================#
#==================================================================================================================================#

    #Affiche le diagramme de la matrice M et
    #les arêtes d'une liste l en rouge
def printMatrice(M,l):
    
    #crée un graphe orienté G
    G = nx.DiGraph()
    #Parcours de la matrice
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i,j] != float('inf'):      #si il existe une flèche de i à j
            
                #ajout de la connexion
                G.add_edge(i, j, weight=M[i,j])
                
    pos = nx.circular_layout(G)             #calcul de la disposition du graph
    nx.draw(G, pos, with_labels=True)       #dessine le graph G, de disposition pos
    
    #ajout des poids
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    #si une liste de sommets est donnée
    if len(l) > 1:
        
        verif = True    #variable de verification du chemin
        
        #création du chemin donné par la liste de sommets l
        chemin = []
        for i in range(len(l)-1):
            chemin.append((l[i],l[i+1]))
            
            #vérification du chemin
            if M[l[i],l[i+1]] == float('inf'):
                verif = False
        
        #si le chemin éxiste
        if verif:
            
            #change la couleur du chemin donné
            nx.draw_networkx_edges(G, pos, edgelist=chemin, edge_color='red')
        
        #si le chemin n'éxiste pas
        else:
            print("Erreur : le chemin de sommets l n'existe pas.")
    
    plt.show()      #affichage
    
    
#==================================================================================================================================#
#=============================================================== §3 ===============================================================#
#==================================================================================================================================#

    #La fonction graphe permet de créer une matrice de taille n avec
    #à 50% une distance infinie et 50% une distance entre a et b
def graphe(n,a,b):
    
    #Initialisation :
    #création d'une matrice aléatoire de 0 et de 1
    M = rm.randint(0,2,(n,n))
    #changement du type de matrice pour pouvoir mettre float('inf')
    M = M.astype('float64')
    
    #parcours de la matrice
    for i in range (n):
        for j in range (n):
            if M[i,j] == 1:
                M[i,j] = rm.randint(a,b)    #remplace les 1 par des aléatoirs sur l'intervalle [a,b[
            else:
                M[i,j] = float('inf')       #remplace les 0 par float('inf') (infini positif, absence de chemin)
    return M
    
    
    #La fonction graphe2 permet de créer une matrice de taille n avec
    #à 1-p% une distance infinie et p% une distance entre a et b
def graphe2(n,p,a,b):
    
    #Initialisation :
    #création d'une matrice aléatoire de 0 et de 1 à proportion p
    M = rm.binomial(1,p,(n,n))
    #changement du type de matrice pour pouvoir mettre float('inf')
    
    #parcours de la matrice
    M = M.astype('float64')
    for i in range (n):
        for j in range (n):
            if M[i,j] == 1:
                M[i,j] = rm.randint(a,b)    #remplace les 1 par des aléatoirs sur l'intervalle [a,b[
            else:
                M[i,j] = float('inf')       #remplace les 0 par float('inf') (infini positif, absence de chemin)
    return M
    
    
#==================================================================================================================================#
#=============================================================== §4 ===============================================================#
#==================================================================================================================================#

#Fonction qui permet l'affichage final du résultat de l'execution des algorithme

def lePrintFinal(tableau,d,M):
    for i in tableau:
        
        #si le sommet de départ est sélectionné
        if i == d:
            print("Sommet de depart " + chr(i+ord('a')) + "\n")
        
        #si il n'y a pas de chemin entre d et le sommet sélectionné
        elif tableau[i]["dist"] == float('inf'):
            print("Sommet " + chr(i+ord('a')) + " non joignable à " + chr(d+ord('a')) + " par un chemin dans le graphe G\n")
            
        #si il y a un chemin entre d et le sommet sélectionné
        else:
            
            #création de la liste des prédécesseurs
            t = []
            a = tableau[i]["pred"]
            if a != -1:
                tour = 0
                while a != d and tour < len(M):
                    t.append(a)
                    a = tableau[a]["pred"]
                    tour += 1
            text = ""
            l = len(t)
            for j in range(l):
                if j == l-1:
                    text += chr(t.pop()+ord('a'))
                    t.append(0)
                else:
                    text += chr(t.pop()+ord('a')) + ", "
                
            #si il y a un cycle négatif le chemin entre d et le sommet sélectionné
            if l == len(M):
                print("Le sommet " + chr(i+ord('a')) + " est joignable depuis " + chr(d+ord('a')) + " par un chemin dans le graphe G, mais pas de plus court chemin (présence d’un cycle négatif)\n")
                
            #si il y a des sommets sur le chemin entre d et le sommet sélectionné
            elif l > 0:
                print("Le sommet " + chr(i+ord('a')) + " est joignable à " + chr(d+ord('a')) + " pour une distance de", tableau[i]["dist"], "en passant par les sommets numéros", text, "\n")
            
            #si le chemin entre d et le sommet sélectionné est direct
            else:
                print("Le sommet " + chr(i+ord('a')) + " est joignable directement à " + chr(d+ord('a')) + " pour une distance de", tableau[i]["dist"], "\n")
    liste = []
    printMatrice(M, liste)


################## Algorithme de Dijkstra ##################

# Sous fonctions
 
    #La fonction inf permet de retrouver l'élément avec le chemin le plus court
    #parmi les sommets qui n'ont pas encore trouvé leur chemin le plus court
def inf(dic):
    
    #sélectionne une des distances pour faire la comparaison
    for i in dic:
        if dic[i]["status"] == False :
            a = i
            
    #parcours du dictionnaire pour trouver le plus petit chemin
    for i in dic:
        if dic[i]["status"] == False and dic[i]["dist"] < dic[a]["dist"]:
            a = i
    return a
    
    #La fonction countFalse compte le nombre d'éléments qui n'ont pas leur chemin
    #le plus court confirmé. Quand countFalse renvoie 0, tout les chemins sont trouvés
def countFalse(dic):
    a = 0
    for i in dic:
        if dic[i]["status"] == False:
            a+=1
    return a

#Fonction principale

    #Fonction principale, prend en paramètre une matrice M et un sommet d
    #renvoie les plus courts chemins de d a chaque autre sommet en utilisant l'algorithme Dijkstra
def Dijkstra(M,d):
    
    # initialisation :
    # création et remplissage du dictionnaire
    tableau = {}
    for i in range(len(M)):
        tableau[i] = {"dist" : M[d,i], "pred" : d, "status" : False}
    tableau[d]["dist"] = 0
    tableau[d]["status"] = True
    #sommet à la plus petite distance (chemin avec le poids le plus petit)
    plusPetiteDistance = inf(tableau)
    tableau[plusPetiteDistance]["status"] = True
    
    #Tant qu'il reste des sommets a vérifier
    while countFalse(tableau) > 0:
        for i in tableau:
            if tableau[i]["status"] == False:
                #comparaison de vérification (dist(s) + dist(s,t) ? dist(t))
                if tableau[plusPetiteDistance]["dist"] + M[plusPetiteDistance,i] < tableau[i]["dist"]:
                    tableau[i]["dist"] = tableau[plusPetiteDistance]["dist"] + M[plusPetiteDistance,i]
                    tableau[i]["pred"] = plusPetiteDistance
        plusPetiteDistance = inf(tableau)
        tableau[plusPetiteDistance]["status"] = True
    return tableau
    

################## Algorithme de Bellman-Ford ##################

# Sous fonctions

    #fonction d'initialisation du tableau des flèches du graphe
    #renvoie un dictionnaire qui correspond au tableau
    #dictionnaire construit de cete manière : {(s,t) : dist(ds), dist(st), dist(dt)}
    #l'ordre des flèches est déterminé de manière arbitraire (ordre de lecture de la matrice)
def initialisation(M,d):
    listeFleches = []       #création de la liste
    
    #parcours de la matrice
    for i in range(len(M)): 
        for j in range(len(M)):
            if M[i,j] != float('inf'):  #si il y a une flèche entre i et j
            
                #ajoute la fleche (i,j)
                listeFleches.append((i,j))
                
    return listeFleches


    #Fonction qui effectuele parcours du tableau de l'algorithme (opération dist(s) + dist(st) ? dist(t))
def tour(fleches, tableau, M):
    
    #pour chaque ligne du tableau   i = couple (s,t) donc i[0] = s et i[1] = t
    for i in fleches:
        
        #si dist(s) + dist(st) < dist(t)
        if tableau[i[0]]["dist"] + M[i[0],i[1]] < tableau[i[1]]["dist"]:
        
            #alors dist(t) = membre de gauche (dist(s) + dist(st))
            tableau[i[1]]["dist"] = tableau[i[0]]["dist"] + M[i[0],i[1]]
            
            #et predecesseur de t = s
            tableau[i[1]]["pred"] = i[0]
            
        #sinon, ne rien faire

#Fonction principale

    #Fonction principale, prend en paramètre une matrice M et un sommet d
    #renvoie les plus courts chemins de d a chaque autre sommet en utilisant l'algorithme Bellman-Ford
def Bellman_Ford(M,d):
    
    # initialisation :
    nbTour = 0
    stop = False
    #création et remplissage du dictionnaire
    tableau = {}
    for i in range(len(M)):
        tableau[i] = {"dist" : M[d,i], "pred" : -1}
        if tableau[i]["dist"] != float('inf'):
            tableau[i]["pred"] = d
    tableau[d]["dist"] = 0
    tableau[d]["pred"] = d
    #création de la liste des flèches du graphe
    fleches = initialisation(M,d)
    
    #tant que le nombre d'itération ne dépasse pas la taille de la matrice -1 (présence d'une boucle a poids négatif)
    #s'arrête aussi si aucune modification n'a été faite pendaant le tour
    while nbTour < len(M)-1 and stop == False:
        
        Comparaison = cp.deepcopy(tableau)       #création d'une copie du tableau de flèches pour la comparaison après le tour
        tour(fleches,tableau, M)                #passage du tour (opération dist(s) + dist(st) ? dist(t) sur chaque flèche)
        stop = Comparaison == tableau           #comparaison pour savoir si modification à été faite
        nbTour += 1
    
    #affichage
    #print("Nombre de tour : ",nbTour, "\n")
    return tableau

    
#==================================================================================================================================#
#=============================================================== §5 ===============================================================#
#==================================================================================================================================#


    #Fonction de parcours en largeur, prend en entrée la matrice M du graphe et le sommet de départ d
    #renvoie la liste des sommets du triés grace au parcours en largeur
def parcoursL(M,d):
    
    #initialisation :
    listeSommets = []               #création puis remplissage de la liste des sommets décalés par d
    for i in range(d, len(M)+d):
        listeSommets.append(i)
        if i >= len(M):
            listeSommets[i-d] -= len(M)
    listeTemp = []          #file de parcours des sommets
    liste = []              #liste finale
    
    #ajout du sommet d à la liste et à la file
    listeTemp.append(d)
    liste.append(d)
    
    #parcours
    while len(listeTemp) != 0:
        s = listeTemp.pop(0)           #extraction du premier élément de la file
        for i in range(len(M)):
            if M[s,i] != float('inf'):      #pour tout les voisins de s
                if i not in liste:          #qui n'ont pas été encire visités
                    listeTemp.append(i)     #enfiler le sommet
                    liste.append(i)         #ajouter le sommet à la liste des sommets visités (liste finale)
    return liste
                    
                    
    #fonction d'initialisation du tableau des flèches du graphe
    #renvoie un dictionnaire qui correspond au tableau
    #dictionnaire construit de cete manière : {(s,t) : dist(ds), dist(st), dist(dt)}
    #l'ordre des flèches est déterminé par le parcours en largeur du graphe
def initialisationLargeur(M,d):
    listeFleches = []                   #création de la liste
    listeSommets = parcoursL(M, d)      #liste dessommets par parcours en largeur de M depuis le sommet d
    
    #parcours de la matrice
    for i in listeSommets: 
        for j in range(len(M)):
            if M[i,j] != float('inf'):  #si il y a une flèche entre i et j
            
                #ajoute la fleche (i,j)
                listeFleches.append((i,j))
    
    return listeFleches

    #Fonction principale, prend en paramètre une matrice M et un sommet d
    #renvoie les plus courts chemins de d a chaque autre sommet en utilisant l'algorithme Bellman-Ford
def Bellman_FordLargeur(M,d):
    
    # initialisation :
    nbTour = 0
    stop = False
    #création et remplissage du dictionnaire
    tableau = {}
    for i in range(len(M)):
        tableau[i] = {"dist" : M[d,i], "pred" : -1}
        if tableau[i]["dist"] != float('inf'):
            tableau[i]["pred"] = d
    tableau[d]["dist"] = 0
    tableau[d]["pred"] = d
    #création de la liste des flèches du graphe
    fleches = initialisationLargeur(M,d)
    
    #tant que le nombre d'itération ne dépasse pas la taille de la matrice -1 (présence d'une boucle a poids négatif)
    #s'arrête aussi si aucune modification n'a été faite pendaant le tour
    while nbTour < len(M)-1 and stop == False:
        
        Comparaison = cp.deepcopy(tableau)       #création d'une copie du tableau de flèches pour la comparaison après le tour
        tour(fleches,tableau, M)                #passage du tour (opération dist(s) + dist(st) ? dist(t) sur chaque flèche)
        stop = Comparaison == tableau           #comparaison pour savoir si modification à été faite
        nbTour += 1
    
    #affichage
    #print("Nombre de tour : ",nbTour, "\n")
    return tableau
    
    #fonction visiteP, sert dans le parcours en profondeur, prend en entrée le dictionnaire des sommets, le sommet a visiter, la liste finale, et la matrice
    #fonction récursive, modifie la liste finale des sommets a renvoyer après le parcours
def visiteP(dictSommets, s, liste, M):
      dictSommets[s] = True             #sommet visité
      liste.append(s)                   #donc ajout a la liste finale
      for i in range(len(M)):
          if M[s,i] != float('inf'):        #pour tout les voisins de s
              if dictSommets[i] == False:   #qui n'ont pas été encire visités
                  visiteP(dictSommets, i, liste, M)     #appel récursif pour visiter le sommet et ses voisins
                  
    #Fonction de parcours en profondeur, prend en entrée la matrice M du graphe et le sommet de départ d
    #renvoie la liste des sommets du triés grace au parcours en profondeur
def parcoursP(M,d):
    
    #initialisation :
    listeSommets = []               #création puis remplissage de la liste des sommets décalés par d
    for i in range(d, len(M)+d):
        listeSommets.append(i)
        if i >= len(M):
            listeSommets[i-d] -= len(M)
            
    dictSommets = {}        #création puis remplissage du dictionnaire des sommets décalés par d accompagnés d'un booléen (True = sommet visité)
    for i in listeSommets:
        dictSommets[i] = False
    liste = []                          #liste final à renvoyer
    visiteP(dictSommets, d, liste, M)   #parcours
    return liste


    #fonction d'initialisation du tableau des flèches du graphe
    #renvoie un dictionnaire qui correspond au tableau
    #dictionnaire construit de cete manière : {(s,t) : dist(ds), dist(st), dist(dt)}
    #l'ordre des flèches est déterminé par le parcours en profondeur du graphe
def initialisationProfondeur(M,d):
    listeFleches = []                   #création de la liste
    listeSommets = parcoursL(M, d)      #liste dessommets par parcours en profondeur de M depuis le sommet d
    
    #parcours de la matrice
    for i in listeSommets: 
        for j in range(len(M)):
            if M[i,j] != float('inf'):  #si il y a une flèche entre i et j
            
                #ajoute la fleche (i,j)
                listeFleches.append((i,j))
                
    return listeFleches

    #Fonction principale, prend en paramètre une matrice M et un sommet d
    #renvoie les plus courts chemins de d a chaque autre sommet en utilisant l'algorithme Bellman-Ford
def Bellman_FordProfondeur(M,d):
    
    # initialisation :
    nbTour = 0
    stop = False
    #création et remplissage du dictionnaire
    tableau = {}
    for i in range(len(M)):
        tableau[i] = {"dist" : M[d,i], "pred" : -1}
        if tableau[i]["dist"] != float('inf'):
            tableau[i]["pred"] = d
    tableau[d]["dist"] = 0
    tableau[d]["pred"] = d
    #création de la liste des flèches du graphe
    fleches = initialisationProfondeur(M,d)
    
    #tant que le nombre d'itération ne dépasse pas la taille de la matrice -1 (présence d'une boucle a poids négatif)
    #s'arrête aussi si aucune modification n'a été faite pendaant le tour
    while nbTour < len(M)-1 and stop == False:
        
        Comparaison = cp.deepcopy(tableau)       #création d'une copie du tableau de flèches pour la comparaison après le tour
        tour(fleches,tableau, M)                #passage du tour (opération dist(s) + dist(st) ? dist(t) sur chaque flèche)
        stop = Comparaison == tableau           #comparaison pour savoir si modification à été faite
        nbTour += 1
    
    #affichage
    #print("Nombre de tour : ",nbTour, "\n")
    return tableau


#==================================================================================================================================#
#=============================================================== §6 ===============================================================#
#==================================================================================================================================#

    #fonction tempsDij(n) génère une matrice aléatoire de taille n
    #calcule les plus cours chemins du premier sommet avec l'algorithme de Dijkstra
    #renvoie le temps de calcul
def tempsDij(n):
    M = graphe(n, 2, 10)        #génère un graphe aléatoire
    start=time.perf_counter()   #début du timer
    Dijkstra(M, 0)              #calcule les plus cours chemins du premier sommet
    stop=time.perf_counter()    #fin du timer
    return(stop-start)          #renvoie le temps du timer

    #fonction tempsBF(n) génère une matrice aléatoire de taille n
    #calcule les plus cours chemins du premier sommet avec l'algorithme de Bellman-Ford
    #renvoie le temps de calcul
def tempsBF(n):
    M = graphe(n, 2, 10)        #génère un graphe aléatoire
    start=time.perf_counter()   #début du timer
    Bellman_FordLargeur(M, 0)   #calcule les plus cours chemins du premier sommet
    stop=time.perf_counter()    #fin du timer
    return(stop-start)          #renvoie le temps du timer


#==================================================================================================================================#
#=============================================================== §7 ===============================================================#
#==================================================================================================================================#
    
    #Fonction trans(M) prend en entrée une matrice et renvoie sa fermeture transitive
def trans(M):
    n = len(M)
    for i in range(n):
        for j in range(n):
            if (M[j,i] != float('inf')):
                for k in range(n):
                    if (M[i,k] != float('inf')):
                        M[j,k] = 1
    return M

    #Retourne un booléan répondant à la question :
    #Le graphe G donné par la matrice M est-il fortement connexe ?
def fc(M) :
    M2 = trans(M)                   #fermeture transitive de M
    for i in range(len(M2)):
        for j in range(len(M2)):
            if M2[i,j] != 1:        #si il n'existe aucun chemin de i vers j
                return False
    return True


#==================================================================================================================================#
#=============================================================== §8 ===============================================================#
#==================================================================================================================================#

    #retourne le pourcentage de matrice fortement connexe
    #pour une taille de matrice n
def test_stat_fc(n):
    nbVrai = 0
    for i in range(100): #pour 100 essais
        M = graphe2(n,0.5,1,5) #genere une matrice de taille n
        if (fc(M)):
            nbVrai += 1
    return nbVrai


#==================================================================================================================================#
#=============================================================== §9 ===============================================================#
#==================================================================================================================================#

    #retourne le pourcentage de matrice fortement connexe
    #pour une taille de matrice n et un taux de fleche p
def test_stat_fc2(n,p):
    nbVrai = 0
    for i in range(100): #pour 100 essais
        M = graphe2(n,p,1,5) #genere une matrice de taille n et de taux p
        if (fc(M)):
            nbVrai += 1
    return nbVrai

    #trouve le taux fleche pour lequelle la matrice de taille n est
    #presque toujours fortement connexe
    #avec p qui diminue
def seuil(n):
    i = 0
    while i < 1 :
        stat = test_stat_fc2(n,i)
        if stat >= 99:
            return i
        i += 0.01
    return 1


#==================================================================================================================================#
#============================================================== §10 ===============================================================#
#==================================================================================================================================#

       #trouve le taux fleche pour lequelle la matrice de taille n est
       #presque toujours fortement connexe
       #avec p qui augmente
def seuil2(n):                  #méthode plus rapide, donnée en cours par notre enseignant
    i = 0
    while i < 1 :
        stat = test_stat_fc2(n,i)
        if stat >= 99:
            return i
        i += 0.01 #augmentation de p
    return 1

#==================================================================================================================================#
#============================================================= tests ==============================================================#
#==================================================================================================================================#

#Instructions :
'''
la zone de test est triée par question et par étape, il suffit de retirer les '#'
sur les lignes de chaque zone, en vérifiant que les variables utilisées ne soient pas en commentaire.
'''

#==================== §2 ====================#                          #code ligne 14

### 2.1 : ###


##matrice (modifiez la à votre goût)
B = np.array(([0,0,2,0,0],[3,0,2,0,0],[0,0,0,0,0],[0,-4,0,0,1],[5,0,0,0,0]))

M3=np.array([[15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14],
       [0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0],
       [ 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 12, 0, 13, 0, 0, 0, 0, 0],
       [0, 0, 0, 14, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0],
       [0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  8, 0, 0],
       [0,  9,  9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
       [ 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0,  8, 0, 16, 0, 14, 13, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 14, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
         
N3=np.array([[-11,  0,  0,  0,  0,  0, -16,  0,  -7, -17],
       [ 0,  0,   3,   6,  0,  0,  0,  0,  0,  0],
       [ 0,  0,   8,  -7,  0,  0, -11,   5,  0,  0],
       [ 0, -20,  -8,  0,  0,  0,  0,  0,   3,  0],
       [ 0,  0,  -6,  0,  0,  0, -11,  0,  0,  0],
       [ 0,  0,  0,  0,  -1,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0, -14,  0,  10,  0,  0],
       [ 0,  0,  0,  0,  0, -19,  -5,  0,  0,  0],
       [ 0,  0,  0,  0,  0, -16,  0,  14,  0,  0],
       [ 0,  19,  0,  0,  14,  0,  0,  -9,  11,  0]])


P3=np.array([[1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0],
       [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
       [0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
       [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
       [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
       [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
       [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1],
       [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
       [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
       [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
       [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
       [0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
       [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0]])



N3 = N3.astype('float64')     #conversion pour les float('inf')

#remplacement des 0 par des float('inf')
for i in range(len(N3)):
    for j in range(len(N3)):
        if N3[i,j] == 0:
            N3[i,j] = float('inf')
            
l = []

## tests :
#printMatrice(B, l)

### 2.2 : ###

l = [3,4,0,2]       ##liste des sommets, à modifier à votre guise
#printMatrice(B, l)

#==================== §3 ====================#                          #code ligne 66

l = []

### 3.1 : ###

#M1 = graphe(5, 1, 10)
#printMatrice(M1, l)

### 3.2 : ###

#M2 = graphe2(5, 0.25, 1, 1)
#printMatrice(M2, l)

#==================== §4 ====================#                          #code ligne 110

### 4.1 : ###                                                           #code ligne 190

#M3 =  graphe(5, 1, 10)     #truc random taille, poids de truc a truc
d1 = 0
lePrintFinal(Dijkstra(B, d1), d1, B)

### 4.2 : ###                                                           #code ligne 260

#M4 =  graphe(5, 1, 10)
#d2 = 0
#lePrintFinal(Bellman_Ford(M4, d), d, M4)

#==================== §5 ====================#                          #code ligne 290

##Pour le nombre de tour : supprimer le '#' devant les lignes 286, 369 et 447

#M5 = graphe(5, 1, 10)
#d3 = 2
#Bellman_Ford(M5, d3)
#Bellman_FordLargeur(M5, d3)                                            #code ligne 340
#Bellman_FordProfondeur(M5, d3)                                         #code ligne 420

#==================== §6 ====================#                          #code ligne 450

### 6.1 : ###

#n1 = 5
#tempsDij(n1)
#tempsBF(n1)

### 6.2 : ###

#liste des temps
tabDi = []
tabBF = []

#temps
#for i in range(2,200):
#    tabDi.append(tempsDij(i))
#    tabBF.append(tempsBF(i))

#affichage
#plt.plot(tabDi, label="Dijkstra")
#plt.plot(tabBF, label="Bellman-Ford")
#plt.legend()
#plt.show()

#==================== §7 ====================#                          #code ligne 480

#M6 = graphe2(8,0.3,1,10)
#printMatrice(M6, l)
#print("Le graphe est il fortement connexe ? :", fc(M6))

#==================== §8 ====================#                          #code ligne 500

#n2 = 15
#print("Nombre de graphes fortement connexes :", test_stat_fc(n2))

#==================== §9 ====================#                          #code ligne 520

#n3 = 15
#p1 = 0.5
#print("Nombre de graphes fortement connexes :", test_stat_fc2(n3, p1))

#print("seuil :", seuil(n3))

#=================== §10 ====================#                          #code ligne 540

### 10.1 : ###

#X = [n for n in range(10,40,1)]
#Y = [seuil2(x) for x in X]

#plt.scatter(X,Y)
#coef = np.polyfit(X,Y,1)
#poly1d_fn = np.poly1d(coef) 
#plt.plot(X,Y, 'o', X, poly1d_fn(X))
#plt.show()

### 10.1 : ###

#X = [n for n in range(10,40,1)]
#Y = [seuil2(x) for x in X]
#logX = np.log10(X)
#logY = np.log10(Y)
#coef = np.polyfit(logX, logY, 1)
#a, c = coef[0], 10**coef[1]
#print(a, c)
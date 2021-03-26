# phonetique
projet de synthese vocale (Le textgrid et le fichier audio vont arriver)

Projet en python de synthese vocale (concatenation de diphones) à partir de phonemes enregistrés.

Possibilités d'effectuer de nombreuses permutations par rapport aux phrases enregistrées de base.

Le dictionnaire de mots est présent directement dans le script sous la forme d'un dict donnant pour chaque mot sa réalisation phonétique.

Les trois phrases enregistrées de base sont :

"La jolie petite maison est une péniche."

"Le petit garçon vit sur un beau bateau."

"Un enfant joue aux petit soldats."

Par ailleurs, j'ai ajouté la conjonction de coordination 'et' et le script supporte la possibilité de mettre 2 verbes dans une phrase

et adapte la prosodie en conséquence.

Il y a la possibilité de faire un certain nombre de combinaisons comme l'allongement :

"La jolie petite maison est une péniche et un enfant joue aux petit soldats". 

"Un enfant joue aux petit soldats sur un beau bateau".

"Le petit garçon et un enfant jouent aux petits soldats".

"Un enfant et le petit garçon vivent sur la péniche".

Mais également des permutations comme celles-ci (non exhaustives):

"Le joli petit bateau est une péniche/maison."

"Un enfant joue sur la péniche."

"Le joli bateau est une petite maison."

"Le garçon joue sur la maison."

"La maison est jolie."

"Sur la péniche un enfant joue."

etc...
Le script prend en compte les liaisons entre tous les mots et ajoute des phonèmes si nécéssaire

exemple : 'est' + voyelle donne une réalisation phonétique de 'est' qui est Et

Pareil pour 'un', qui devant voyelle se réalise In.

Dans le cas où une liaison n'est pas présente dans le textGrid, le script passe au phonème suivant

dans le but de gérer les exceptions et de ne pas tomber dans une boucle infinie.

Par ailleurs, en ce qui concerne la prosodie, le script se base sur deux petits algorithmes pour donner à chaque mot dans la phrase en fonction

de sa position par rapport au verbe une frequence et une durée relative differentes

Pour ce faire, le script détecte automatiquement la position du ou des verbes dans la phrase.

La frequence monte progressivement jusqu'au verbe puis redescend.

La durée reste relativement stable jusqu'au verbe puis augmente progressivement.

Ces modifications sont opérées au niveau du mot.

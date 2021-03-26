# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""

Il faut installer les modules suivants :
pip install praat-parselmouth
pip install praat-textgrids
"""

# modules importés
import parselmouth
import textgrids
from parselmouth.praat import call

# variables globales
SOUND_PATH_FILE = 'projet.wav'
GRID_PATH_FILE = 'projet.TextGrid'
RESULT_PATH_FILE = 'resultats.wav'

# phrases à faire prononcer
ORTHO_SENTENCES = ['la jolie petite maison est une péniche', 'le petit garçon vit sur un beau bateau',
'un enfant joue aux petits soldats']

phono_dict = {'la':'la', 'jolie':'ʒoli', 'petite':'pœtit', 'maison':'mEzO', 'est':'E', 'une':'yn', 'péniche':'peniʃ',
'le':'lœ', 'petit':'pœti', 'garçon':'gaRsO', 'vit':'vi', 'sur':'syR', 'un':'I', 'beau':'bo', 'bateau':'bato',
'enfant':'AfA', 'joue':'ʒu', 'aux':'o', 'petits':'pœti', 'soldats':'sɔlda', 'et':'e', 'jouent':'ʒu', 'vivent':'viv'}

# liste des verbes pour les 3 phrases
verbs_list = {'est':'E', 'joue':'ʒu', 'jouent':'ʒu', 'vit':'vi', 'vivent':'viv'}

def get_coefficient(nbr_words):

    """
    fonction qui définit un coefficient en fonction de la taille de la phrase
    pour adapter les algorithmes de frequence et de durée relative en fonction
    de la taille de la phrase (nombre de mots)
    """
    # si la phrase fait moins de 8 mots, on applique un coefficient de 1
    if nbr_words < 8:
        return 1
    # sinon, le coefficient est de 1.8
    else:
        return 1.8

def get_frequency_with_word(num_word, num_word_verbs, conj_offset, coefficient):

    """ 
    fonction qui renvoie une fréquence "idéale" correspondante à la position du mot dans la phrase
    par rapport au verbe
    num_word -- integer, position du mot
    num_word_verbs -- list, position du/des verbe(s)
    conj_offset -- integer, position de la conjonction de coordination
    renvoie la fréquence idéale (selon moi) pour le mot en question
    """

    # si il n'y a qu'un verbe dans la phrase
    if len(num_word_verbs) == 1:
    
        if num_word == 0:
            return 100
        elif num_word < num_word_verbs[0]:
            return 100 + (num_word * (12/coefficient))
        elif num_word_verbs[0] == num_word:
            return 115
        else:
            return 110 - ((num_word - num_word_verbs[0]) * (10/coefficient))

    # si il y en a deux
    else:
        # si nous sommes dans la premiere proposition de la phrase
        if num_word < conj_offset:

            if num_word == 0:
                return 100
            elif num_word < num_word_verbs[0]:
                return 100 + (num_word * (12/coefficient))
            elif num_word_verbs[0] == num_word:
                return 115
            else:
                return 110 - ((num_word - num_word_verbs[0]) * (10/coefficient))
        
        # si le mot courant est la conjonction de coordination
        elif num_word == conj_offset:
            return 100
        else:
            # on récupere la position du mot courant et du verbe dans la deuxieme proposition
            num_word = num_word - conj_offset
            num_verb = num_word_verbs[1] - conj_offset
            if num_word < num_verb:
                return 100 + (num_word * (12/coefficient))
            elif num_verb == num_word:
                return 115
            else:
                return 110 - ((num_word - num_verb) * (10/coefficient)) 


def get_relative_duration_with_word(num_word, num_word_verbs, conj_offset, coefficient):

    """ 
    fonction qui renvoie une durée "idéale" correspondante à la position du mot dans la phrase
    par rapport au verbe
    num_word -- integer, position du mot
    num_word_verbs -- list, position du/des verbe(s)
    conj_offset -- integer, position de la conjonction de coordination
    renvoie la durée relative idéale (selon moi) pour le mot en question
    """    
    
    # si il n'y a qu'un verbe dans la phrase
    if len(num_word_verbs) == 1 :

        if num_word == 0:
            return 0.67
        elif num_word < num_word_verbs[0] - 1:
            return 0.67 - (num_word / (11*coefficient))
        elif num_word_verbs[0] == num_word - 1:
            return 0.67
        elif num_word_verbs[0] == num_word:
            return 0.67
        else:
            return 0.67 + ((num_word - num_word_verbs[0]) / (30*coefficient))

    else:
        
        # si le mot courant est avant la conjonction de coordination, on traite la premiere proposition de la phrase
        if num_word < conj_offset:

            if num_word == 0:
                return 0.67
            elif num_word < num_word_verbs[0] - 1:
                return 0.67 - (num_word / (11*coefficient))
            elif num_word_verbs[0] == num_word - 1:
                return 0.67
            elif num_word_verbs[0] == num_word:
                return 0.67
            else:
                return 0.67 + ((num_word - num_word_verbs[0]) / (30*coefficient))
        
        # si le mot courant est la conjonction de coordination
        elif num_word == conj_offset:
            return 0.67
        
        # sinon, on traite la deuxieme proposition de la phrase
        else:
            
            # on récupere la position du mot courant et du verbe dans la deuxieme proposition
            num_word = num_word - conj_offset
            num_verb = num_word_verbs[1] - conj_offset

            if num_word < num_verb - 1:
                return 0.67 - (num_word / (11*coefficient))
            elif num_verb == num_word - 1:
                return 0.67
            elif num_verb == num_word:
                return 0.67
            else:
                return 0.67 + ((num_word - num_verb) / (30*coefficient))


def get_intensity(num_word, num_word_verbs, nbr_words, record_intensity):

    """ 
    fonction qui renvoie l'intensité "idéale" correspondante à la position du mot dans la phrase
    Si c'est le premier mot de la phrase ou si il s'agit du verbe, on augmente l'intensité de 5 db
    Si c'est le dernier mot de la phrase, on baisse l'intensité de 3 db
    num_word -- integer, position du mot
    num_word_verbs -- list, position du/des verbe(s)
    nbr_words -- integer, nombre de mots dans la phrase
    record_intensity -- float, intensité de l'enregistrement
    renvoie l'intensité "idéale" pour le mot en question
    """
    
    if num_word == 0 or num_word in num_word_verbs:
        return record_intensity + 5
    elif num_word == nbr_words - 1:
        return record_intensity - 3
    else:
        return record_intensity

        
def convert_ortho_sentence(sentence):
    
    """
    fonction qui convertit la phrase orthographique en sa représentation phonétique
    et en prenant compte les liaisons entre les mots
    """
    
    # liste des mots phonétiques
    new_words_list = list()
    
    # on découpe la phrase en mots
    # convertion phonétique de chaque mot de la phrase orthographique
    for word in sentence.split():
        new_words_list.append(phono_dict[word])
        
    # liste des positions des verbes dans la phrase
    verb_offset = list()
    # position de la conjonction de coordination dans la phrase
    conj_offset = 0

    # on récupère l'offset du verbe dans la phrase (sa position)
    for i in range(len(new_words_list)):

        # si il s'agit d'un verbe, on récupere sa position
        if new_words_list[i] in verbs_list.values():
            verb_offset.append(i)
        
        # on récupere la position de la conj de coordination dans la phrase
        if new_words_list[i] == 'e':
            conj_offset = i

        # on effectue un traitement pour la liaison du mot 'est' si le mot suivant commence par une voyelle
        # dans ce cas, on ajoute le phonème t
        if new_words_list[i] == 'E' and new_words_list[i+1][0].lower() in ('a', 'e', 'i', 'o', 'u', 'y'):
            new_words_list[i] += 't'

        # on procède de la meme facon pour la liaison entre le mot 'un' + voyelle
        # dans ce cas, on ajoute le phonème n
        if new_words_list[i] == 'I' and new_words_list[i+1][0].lower() in ('a', 'e', 'i', 'o', 'u', 'y'):
            new_words_list[i] += 'n'
                  

    # on retourne la liste de mots de la phrase, la position du verbe,
    # la position de la conjonction de coordination et si elle est présente et le nombre de mots 
    return new_words_list, verb_offset, conj_offset, len(new_words_list)

# fonction qui modifie la frequence fondamentale de l'enregistrement
def alter_pitch(sound, manipulation, frequence):

    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0, sound.duration)
    call(pitch_tier, "Add point", sound.duration/2, frequence)
    call([pitch_tier, manipulation], "Replace pitch tier")

    return call(manipulation, "Get resynthesis (overlap-add)")

# fonction qui modifie la durée de l'enregistrement (durée relative)
def alter_duration(sound, manipulation, relative_duration):

    duration_tier = call(manipulation, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, sound.duration)
    call(duration_tier, "Add point", sound.duration/2, relative_duration)
    call([duration_tier, manipulation], "Replace duration tier")
    
    return call(manipulation, "Get resynthesis (overlap-add)")

# definition de la fonction principale
def main():
    
    try:

        # création d'un objet Sound avec notre fichier audio
        snd = parselmouth.Sound(SOUND_PATH_FILE)
        
        # on récupere la fréquence d'échantillonnage
        frequency = snd.get_sampling_frequency()

        # on récupere l'intensité de l'enregistrement
        record_intensity = snd.get_intensity()
        
        # on crée un nouvel objet Sound
        new_sound = call("Create Sound from formula", "fichier_synthese", 1, 0, 0.05, frequency, "0")
        
        # on ouvre le fichier textGrid
        segmentation = textgrids.TextGrid(GRID_PATH_FILE)

        # phrase à faire prononcer (par défaut, c'est la premiere)
        sentence = ORTHO_SENTENCES[0]
        
        # on récupere la liste de mots de la phrase, la position du verbe,
        # la position de la conjonction de coordination et si elle est présente et le nombre de mots
        phono_sentence, verb_offsets, conj_offset, nbr_words = convert_ortho_sentence(sentence)

        # on récupère le coefficient pour les algorithmes
        coefficient = get_coefficient(nbr_words)
        
        # pour chaque mot de la phrase
        for num_word in range(len(phono_sentence)):
        
            # mot avant le mot actuel word, valeur '_' au debut car ce phonème represente le silence de début ou de fin de phrases
            # dans mon textGrid. De plus, impossible de laisser une chaine vide pour l'indexage
            word_before = '_'
            # si le mot n'est pas le premier dans la phrase, alors on determine le mot qui le précède (pour les liaisons)
            if num_word != 0:
                word_before = phono_sentence[num_word-1]
            # mot actuel
            word = phono_sentence[num_word]
            
            # pour chaque lettre du mot word, i est l'index de chaque lettre du mot word
            i = 0
            while i < len(word):

                middle_last_phon = middle_phon = None
                
                # phonème précédent
                last_text_phon = ''
                last_phon = None

                # on parcourt l'ensemble des intervals
                for j, phon in enumerate(segmentation['diphones']):
                    
                    # si il s'agit du premier phonème du mot
                    if i == 0:
                        
                        # on prend on compte le dernier phoneme du mot précédent et le premier du mot actuel pour les liaisons
                        if last_text_phon == word_before[-1] and phon.text == word[i]:

                            # on calcule le milieu du phonème actuel et celui du précédent
                            middle_last_phon = last_phon.xmin + ((last_phon.xmax - last_phon.xmin) / 2)
                            middle_phon = phon.xmin + ((phon.xmax - phon.xmin) / 2)
                            # on incremente i de 1 = on passe au phoneme suivant et on sort de la boucle for
                            i += 1
                            break
                        
                    else:

                        # si il s'agit du dernier phoneme de la phrase, on ajoute le diphone de pause de fin de phrase
                        # le signe de pause est '_' dans mon textGrid
                        if num_word == len(phono_sentence) - 1 and i == len(word) - 1 : 
                            
                            if last_text_phon == word[i] and phon.text == '_':
                            
                                # on calcule le milieu du phonème actuel et celui du précédent
                                middle_last_phon = last_phon.xmin + ((last_phon.xmax - last_phon.xmin) / 2)
                                middle_phon = phon.xmin + ((phon.xmax - phon.xmin) / 2)
                                # on incremente i de 1 = on passe au phoneme suivant et on sort de la boucle for
                                i += 1
                                break                           
                            
                        else:
                            # sinon, on cherche les diphones dans le mot
                            if last_text_phon == word[i-1] and phon.text == word[i]:
                            
                                # on calcule le milieu du phonème actuel et celui du précédent
                                middle_last_phon = last_phon.xmin + ((last_phon.xmax - last_phon.xmin) / 2)
                                middle_phon = phon.xmin + ((phon.xmax - phon.xmin) / 2)
                                # on incremente i de 1 = on passe au phoneme suivant et on sort de la boucle for
                                i += 1
                                break
                    
                    # si le diphone est introuvable, on passe au phoneme suivant du mot word
                    # il s'agit le plus souvent d'une liaison non prise en compte
                    if j == len(segmentation['diphones']) - 1:
                        print('AVERTISSEMENT : Un des diphones est introuvable !')
                        i += 1
                    
                    # on passe au phoneme suivant dans le textgrid
                    # le phoneme actuel devient le phoneme précédent
                    last_phon = phon
                    last_text_phon = phon.text
                
                # si le diphone a été trouvé dans le textgrid
                if middle_phon is not None and middle_last_phon is not None:
                    
                    # on recupere l'intersection avec zéro la plus proche pour le milieu de chaque phonème
                    middle_last_phon = snd.get_nearest_zero_crossing(middle_last_phon, 1)
                    middle_phon = snd.get_nearest_zero_crossing(middle_phon, 1)
                        
                    # on extrait le diphone voulu dans la variable extrait
                    extrait = snd.extract_part(middle_last_phon, middle_phon, parselmouth.WindowShape.RECTANGULAR, 1, False)

                    # création d'un objet Manipulation pour modifier la frequence
                    # et la durée de l'extrait
                    manipulation = call(extrait, "To Manipulation", 0.001, 75, 600)
                            
                    frequence = get_frequency_with_word(num_word, verb_offsets, conj_offset, coefficient)
                    relative_duration = get_relative_duration_with_word(num_word, verb_offsets, conj_offset, coefficient)
                    intensity = get_intensity(num_word, verb_offsets, nbr_words, record_intensity)

                    # on modifie la fréquence fondamentale de l'extrait
                    extrait = alter_pitch(extrait, manipulation, frequence)
                    # on modifie la durée de l'extrait
                    extrait = alter_duration(extrait, manipulation, relative_duration)
                    # on modifie l'intensité de l'extrait
                    extrait.scale_intensity(intensity)

                    # on concatène le diphone obtenu avec new_sound
                    new_sound = new_sound.concatenate([new_sound, extrait])
        
        # on sauvegarde le résultat dans un fichier .wav
        new_sound.save(RESULT_PATH_FILE, parselmouth.SoundFileFormat.WAV)

    # si une erreur se produit
    except Exception as error:
        print('Une erreur s\'est produite : {}'.format(error))


if __name__ == "__main__":
    
    main()

import os,sys # Importation of os and sys modules
import gzip # Importation of gzip module
import json # Importation of the json module

###############################################################################################################################################################################
# Programme permettant la génération de dictionnaires à deux niveaux au format json, la premiere cle correspondant aux identifiants des genomes, la deuxieme cle aux
# transcriptID ou aux protID des genes de ces genomes, la valeur correspond aux annotations KOG ou SigP. Le programme attend en entree le nom du repertoire contenant les fichiers
# d annotations KOG ou SigP en format texte ou en format byte. Pour les dictionnaires KOG la cle transcriptID ou protID est choisie a l aide de la variable col_transcriptID.
# Concernant les dictionnaires d'annotation SigP le dictionnaire prenant comme deuxieme cle les protID des genes peut etre genere a partir de la premiere partie de code. Pour 
# generer le dictionnaire SigP prenant en deuxieme cle les transcriptID qui ne sont pas disponibles dans les fichiers SigP il faut utiliser la deuxieme partie du code
# (ecrite pour ouvrir des fichiers en format byte ici) qui charge un dictionnaire associant transcriptID et protID et genere le dictionnaire prenant en premiere cle tous les
# genomes, en deuxieme cle les transcriptID des genes et en valeur les protID des genes et leur annotation SigP
###############################################################################################################################################################################

inputType = sys.argv[1] # Recovery of the annotation type 'KOG' or 'SigP' from the terminal
AnnotType = "/home/mbourema/mycocosm2024/mycocosm2024_purified/"+str(inputType) # Path to the file according to selected annotation

d1 = {} # Intilization of a dictionary
d2 = {} # Initialization of another dictionary
d3 = {} # Initialization of another dictionary

# Writting of the dictionnary associating transcriptID and protID of each genomes in d3
with open("/home/mbourema/python/removing_sequences/second_approach/dico_transcriptID_protID", "r") as f:
	d4 = json.load(f)

d3.update(d4)

# For each file of the folder of the selected annotation recovery of species name and for each species creation of a dictionnary with the protID as keys and the KOG annotations as values or with
# the transcriptID as keys and the KOG annotations as values (depending on the value of col_transcriptID)
for Files in os.listdir(AnnotType+"/"):
	if inputType2 == "all_KOG_files_ordered":
		col_transcriptID = 0
		SpeciesNames = Files.split('_GeneCatalog')[0]
		d1[str(SpeciesNames)] = {}
# Open each file (compressed) of the folder in byte format
	with open(str(AnnotType)+"/"+str(Files), "r") as f:
# Initialization of protID and annotation variables
		transcriptID = ""
		annotation = ""
		lines = f.read()
# Separation of each line by 'back to line' as a separator
		for line in lines.split("\n"):
# Separation of the lines by tabulation
			if line and not line.startswith("#"):
				elements = line.split('\t')
				if elements[col_transcriptID] == transcriptID:
					annotation = list(zip(annotation, elements[1:]))
				elif elements[col_transcriptID] != "":
					d1[str(SpeciesNames)][str(transcriptID)] = annotation
					transcriptID = elements[col_transcriptID]
					annotation = elements[1:]


'''
# For each file of the folder of the selected annotation in byte format, recovery of species name and for each species creation of a dictionnary with the transcriptID in keys and the SigP annotations as values
for Files in os.listdir(AnnotType+"/"):
	if inputType == "all_SigP_files":
		col_protID = 0
	SpeciesNames = Files.split('_GeneCatalog')[0]
	d2[str(SpeciesNames)] = {}
# Open each file (compressed) of the folder in byte format
	with gzip.open(str(AnnotType2)+"/"+str(Files), "rb") as f:
# Initialization of protID and annotation variables
		transcriptID = ""
		annotation = ""
# Conversion of the file from byte format to text format
		data_byte = f.read()
		data_texte = data_byte.decode("utf-8")
# Separation of each line by 'back to line' as a separator
		for line in data_texte.split('\n'):
# Remove the 'back to ligne' character at the end of each line with rstrip methode
			line = line.rstrip('\n')
# Separation of the lines by tabulation
			if line and not line.startswith("#"):
				elements = line.split('\t')
				if SpeciesNames in d3 :
					for key, value in d3[str(SpeciesNames)].items():
						try:
							if elements[0] in value :
								annotation = elements[0:]
								transcriptID = key
# The dictionnary d is filled with the transcriptID as a key, and with SigP annotation associated with this transcriptID as value 
								d2[str(SpeciesNames)][protID] = annotation
								break
						except KeyError :
							continue

# Writting of the dictionnaries in json format
'''
with open("/home/mbourema/mycocosm2024/mycocosm2024_purified/dico.KOG_queries.json", "w") as f :
	json.dump(d1, f)

'''
with open("/home/mbourema/mycocosm2024/mycocosm2024_purified/dico.SigP_queries2.json", "w") as f :
	json.dump(d2, f)
'''

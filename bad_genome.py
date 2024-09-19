###############################################################################################################################################################################
# Program that browses in all diamonds outputs and checks if some contains wrong formated queries or wrong formated hits. The list of wrong formated diamonds outputs is then printed
###############################################################################################################################################################################

import shutil # Importation of the shutil module
import os # Importation of the os module

diamonds_path = "/home/mbourema/mycocosm2024/mycocosm2024_purified/files_diamonds/"
list_bad_diamonds = []

list_diamonds_CDS = os.listdir(diamonds_path)
list_diamonds = []
for n in list_diamonds_CDS :
	if "diamond" in n :
		list_diamonds.append(n)

for n in list_diamonds :
	diamond_path= os.path.join(diamonds_path, n)
	with open(diamond_path) as f :
		for line in f:
			list_line = line.split("\t")
			if "|" not in list_line[0] :
				list_bad_diamonds.append(n)
			if ("|" not in list_line[1] and "*" not in list_line[1]):
				list_bad_diamonds.append(n)

print(list_bad_diamonds)

###############################################################################################################################################################################
# Program for creating repertories named by the genomes names and copying on them their KOG and SigP files from a repertory containing all KOG and SigP files.
# The first part creates repertories and copy files from genomes that have at least 2 KOG and SigP files. The second part creates repertories and copy files from genomes
# that have exactely  1 KOG and 1 SigP files
###############################################################################################################################################################################

import os # Le module os permet d'effectuer des opérations telles que la manipulation de fichiers et de répertoires, le travail avec des chemins de fichiers et repertoires...
import shutil # Le module shutil permet aussi d'effectuer des opérations sur des fichiers et des répertoires, il fournit une couche d'abstraction plus élevée que 'os' pour certaines opérations, il est souvent utilisé conjointement avec ce dernier.

'''
KOG_SigP_files_path = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/all_KOG_and_SigP_files/" # Chemin vers le dossier contenant les fichiers KOG et SigP des génomes mycocosm2024
more_KOG_SigP_files_path = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/more_KOG_SigP/" # Chemin du dossier dans lequel on va creer des repertoires et y copier leurs fichiers KOG et SigP
SigP_KOG_files = os.listdir(KOG_SigP_files_path) # Obtention d'une liste des nom des fichiers
n = 0 # Définition d'une variable de contrôle

# Boucle qui va parcourir chaque fichiers et va vérifier si il contient la chaîne de caractère qui correspond à son génome. Si c'est la cas, son répertoire est créé et il y est copié
for file_name in SigP_KOG_files :
        for keyword in ['Capcor1','Capep1','Claps1','Claye1', 'Eryha1','Kurca1','Metro1','Pendig1','Pengri1','Penita1','RhiirA4','Sodal1','Symat1','Triham1','Trias8904']: 
                if keyword in file_name:
                        keyword_folder = os.path.join(more_KOG_SigP_files_path, keyword)
                        os.makedirs(keyword_folder, exist_ok=True)
                        n = n+1
                        source_path = os.path.join(KOG_SigP_files_path, file_name)
                        shutil.copy2(source_path, keyword_folder)

print(f"Le nombre de fichiers créés est de : {n}")
'''

# Même script pour créer et copier les fichiers appartenant aux répertoires qui contiennent 1 fichier KOG et 1 fichier SigP. On vérifie que les fichiers ne proviennent pas de répertoires qu'on souhaite éliminer et on vérifie qu'on ne copie pas des fichiers
# appartenant à un autre répertoire dans un autre répertoire car il ont le même mot-clé avant "_"
KOG_SigP_files_path = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/all_KOG_and_SigP_files/"
file_path = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/1_KOG_1_SigP"
alebreton = "/home/alebreton/mycocosm2024_01_12/"
n = 0
SigP_KOG_files = os.listdir(KOG_SigP_files_path)
repertories = os.listdir(alebreton)
keywords_to_delete = ['Agabi_varbisH97_2', 'Agabi_varbur_1', 'Chagl_1', 'Crypa2', 'Hetan2', 'Neudi1', 'Neute_matA2', 'Phybl2', 'PleosPC15_2', 'Pospl1', 'Mycfi2', 'Triat2', 'TriviGv29_8_2', 'Aspca3', 'Mycgr3', 'PleosPC9_1', 'Picst3', 'Sporo1', 'Trire2', 'Batde5', 'Cante1', 'Cersu1', 'Necha2', 'Neute_mat_a1', 'SerlaS7_3_2', 'Spapa3', 'Treme1', 'Aspac1', 'Capcor1', 'Capep1', 'Claps1', 'Claye1', 'Eryha1', 'Kurca1', 'Metro1', 'Pendig1', 'Pengri1', 'Penita1', 'RhiirA4', 'Sodal1', 'Symat1', 'Triham1', 'Trias8904'] 

for file_name in SigP_KOG_files :
	for keyword in repertories :
		if keyword not in keywords_to_delete :
			if keyword in file_name :
				keyword_folder = os.path.join(file_path, keyword)
				os.makedirs(keyword_folder, exist_ok=True)
				n = n+1
				if keyword + "_GeneCatalog" in file_name : 
					source_path = os.path.join(KOG_SigP_files_path, file_name)
					shutil.copy2(source_path, keyword_folder)

print(f"Le nombre de fichiers créés est de : {n}")

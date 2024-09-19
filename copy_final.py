###############################################################################################################################################################################
# From the repertories generated and filled by the script copy_create.py and after a manual filtering of the folder that contains 2 or more KOG and SigP files,
# the KOG and SigP files are copied in the all_KOG_SigP_files folder, without duplication 
###############################################################################################################################################################################

import os # Le module os permet d'effectuer des opérations telles que la manipulation de fichiers et de répertoires, le travail avec des chemins de fichiers et repertoires...
import shutil # Le module shutil permet aussi d'effectuer des opérations sur des fichiers et des répertoires, il fournit une couche d'abstraction plus élevée que 'os' pour certaines opérations, il est souvent utilisé conjointement avec ce dernier.

source_folder2 = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/1_KOG_1_SigP/" # Chemin vers le dossier contenant les repertoires de génomes nettoyés
final_destination = "/home/mbourema/mycocosm2024/mycocosm2024_purified/all_KOG_SigP_files/" # Chemin vers le dossier de destination
folders_in_folder = os.listdir(source_folder2) # Obtention d'une liste des noms des répertoires de génomes
n = 0 # Définition d'une variable de contrôle
# Boucle qui va parcourir chaque répertoire et va créer son chemin, puis lister tout les fichiers qu'il contient. Ensuite les fichiers de chaque répertoires ont leur chemin de créé et on verifie que leur chemin n'existe pas déjà dans le dossier de destination, si c'est le cas le fichier est copié et n est incrémenté. 
for folder in folders_in_folder :
        full_source_path = os.path.join(source_folder2, folder)
        files_in_folder = os.listdir(full_source_path)
        for file in files_in_folder :
                full_file_path_source = os.path.join(full_source_path, file)
                full_file_path_destination = os.path.join(final_destination, file)
                # Vérifier si le fichier existe déjà dans le dossier de destination
                if not os.path.exists(full_file_path_destination):
                        # Copier le fichier vers le dossier final
                        shutil.copy2(full_file_path_source, final_destination)
                        n = n + 1

print(f"Le nombre de fichiers copiés est : {n}")

'''
# Script effectuant les mêmes opération pour le dossier 2_more_files_fasta.gz. Pour ce dossier le test 'anti-doublon' n'était pas nécessaire


source_folder1 = "/home/mbourema/mycocosm2024/mycocosm2024_pre_purified/more_KOG_SigP/"
final_destination = "/home/mbourema/mycocosm2024/mycocosm2024_purified/all_KOG_SigP_files/"
n = 0
folders_in_folder = os.listdir(source_folder1) # liste les dossiers dans le dossier

for folder in folders_in_folder :
        full_source_path = os.path.join(source_folder1, folder)
        file_in_folder = os.listdir(full_source_path)
        for file in file_in_folder : 
                full_file_path = os.path.join(full_source_path, file)
                shutil.copy2(full_file_path, final_destination)
                n = n + 1

print(f"Le nombre de fichiers copiés est de : {n}")

'''

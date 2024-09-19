################################################################################################################################################################################################
#Definition of a function that browses the aa.fasta.gz files in the all_aa.fasta.gz_files directory, checks whether these files contain the string
#{name of genome to be removed}_GeneCatalog' and assembles the files that do not satisfy this condition, 1000 by 1000, into a file 'all_aa_but_{name of genome to be removed}.fasta.gz', which will be
# will be stored in the directory specified by output_dir. Next, the function searches for the cds file of the genome to be removed and copies it to the directory specified by output_dir
################################################################################################################################################################################################

import os # Importation du module os qui permet d'effectuer des opérations liées au système d'exploitation comme la manipulation des fichiers et des répertoires
import subprocess # Importation du module subprocess qui fournit une interface pour travailler avec les commandes système et les programmes externes depuis un script Python
import time # Importation du module time pour récuperer le temps auquel la ligne est exécutée
import sys # Module qui fournit un certaines variables utilisées ou maintenues par l'interpréteur Python, et à des fonctions qui intéragissent étroitement avec l'interpréteur

start_time = time.time()


''' Définition d'une fonction qui parcourt les fichiers aa.fasta.gz du répertoire all_aa.fasta.gz_files, vérifie si ces fichiers ne contiennent pas la chaîne de caractère
'{nom du génome à retirer}_GeneCatalog' et assemble les fichiers qui satisfons cette condition, 1000 par 1000, au sein d'un fichier 'all_aa_but_{nom du génome à retirer}.fasta.gz', qui
 sera stocké dans le répertoire spécifié par output_dir. Ensuite, la fonction cherche le fichier cds du génome à retirer et le copie dans le répertoire spécifié par output_dir'''

def assemble_and_copy_files(genome_name):
	# Chemin du répertoire contenant tous les fichiers aa.fasta.gz
	input_dir = "/home/mbourema/mycocosm2024/mycocosm2024_purified/all_aa.fasta.gz_files/"

	# Chemin du répertoire ou seront stockés le fichier assemblé et le fichier cds du génome a retirer
	output_dir = "/home/mbourema/mycocosm2024/mycocosm2024_purified/files_for_diamond/"

	# Construction du nom du fichier à assembler
	assembled_file_name = f"all_aa_but_{genome_name}.fasta.gz"

	# Parcours des fichiers dans le répertoire all_aa.fasta.gz_files
	files_to_assemble = [f for f in os.listdir(input_dir) if f"{genome_name}_GeneCatalog" not in f]

	# Assemblage des fichiers par lots
	batch_size = 1000  # On peut ajuster cette valeur selon notre besoin

	# Boucle à travers la liste des fichiers à assembler par lots, à chaque itération, la boucle traite un lot de fichiers
	for i in range(0, len(files_to_assemble), batch_size):

		# Sélection des fichiers pour le lot actuel, création d'une sous-liste de fichiers à partir de l'index i jusqu'à i + batch_size
		batch_files = files_to_assemble[i:i+batch_size]

		# Construction de la commande cat pour assembler les fichiers du lot. Création d'une liste de chemins complets vers les fichiers du lot, puis utilisation de ''.join() pour concaténer les chemins en une seule chaîne
		cat_command = f"cat {' '.join([os.path.join(input_dir, f) for f in batch_files])} >> {os.path.join(output_dir, assembled_file_name)}"

		# Exécution de la commande cat
		subprocess.run(cat_command, shell=True)

	# Copie du fichier all_cds correspondant (dont le nom contient "Claye1_GeneCatalog")
	cds_file_to_copy = [f for f in os.listdir('/home/mbourema/mycocosm2024/mycocosm2024_purified/all_cds.fasta.gz_files/') if f"{genome_name}_GeneCatalog" in f]
	cds_file = cds_file_to_copy[0]
	cp_command = f"cp {os.path.join('/home/mbourema/mycocosm2024/mycocosm2024_purified/all_cds.fasta.gz_files/', cds_file)} {output_dir}"
	subprocess.run(cp_command, shell=True)
	output_file_aa = os.path.join(output_dir, assembled_file_name)
	output_file_cds = os.path.join(output_dir, cds_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembly_but.py <genome_name1> <genome_name2> ...")
        sys.exit(1)

    start_time = time.time()

    for genome_name in sys.argv[1:]:
        assemble_and_copy_files(genome_name)

    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)

end_time = time.time()

total_time = end_time - start_time

print(total_time)

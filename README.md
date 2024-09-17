# Nettoyage de la base de donnée Mycocosm2024
## Problématique

2526 répertoires de génomes sont obtenus suite à leur téléchargement à partir du site mycocosm : 'https://mycocosm.jgi.doe.gov/mycocosm/home' en 2024. Dans ces répertoires figurent différents fichiers d'annotations fonctionnelles, .README, de séquences protéiques ou nucléiques.
Pour effectuer un alignement Diamond des génomes mycocosm contre la base de donnée mycocosm, il faut disposer des fichiers CDS et séquences aa de tout les génomes mycocoms2024. Le nettoyage de la base de donnée mycocosm2024 a consisté en la récupération dans un dossier 'mycocosm2024_purified'
d'un fichier CDS et d'un fichier de séquence protéique (aa) pour chaque répertoires de génomes mycocosm.

## Diagnostique

Le nombre de répertoires de génomes obtenu à l'issue du téléchargement est obtenu à l'aide de l'exécution de la commande 'ls | wc -l' après déplacement dans le dossier où ils sont stockés : /home/alebreton/mycocosm2024_01_12/. La commande affiche 2526 répertoires.
Les fichiers CDS et séquences aa de chaques génomes ont une extension '.fasta.gz'. Le nombre de fichiers ayant une extension '.fasta.gz' pour les 2526 répertoires de génomes peut être obtenu à l'aide de la commande : ls /home/alebreton/mycocosm2024_01_12/**/** | grep -E '.fasta.gz' | wc -l
Le nombre de fichier '.fasta.gz' pour tout les répertoires est : 5045. La commande utilisée pour obtenir le nombre de répertoires contenant respectivement au moins 1, 2, 3, 4, 5 et 6 fichiers '.fasta.gz' est :
find /home/alebreton/mycocosm2024_01_12/ -mindepth 1 -type d -exec sh -c 'test $(find "{}" -type f -name " "*.fasta.gz" | wc -l) -ge x ' \; -print | wc -l en renseignant le nombre minimal de fichiers '.fasta.gz' que les répertoires décomptés doivent contenir à la place de 'x' pour l'argument '-ge x'
find /chemin/vers/le/dossier -type d permet la recherche de tous les sous-répertoires dans le dossier spécifié, – mindepth 1 signifie que la commande find recherche tous les sous-répertoires (-type d) dans le dossier spécifié, en commençant à une profondeur minimale de 1,
pour éviter de compter le dossier racine lui-même. Ensuite, -exec sh -c '[ $(find "{}" -type f -name "*.fasta.gz" | wc -l) -ge 2 ]' \; exécute une commande shell pour chaque sous-dossier trouvé. Ici, la commande shell vérifie si le sous-dossier contient au moins deux fichiers se terminant par '.fasta.gz'.
Enfin, -print: Si la condition est vraie, find imprime le chemin du sous-dossier, | wc -l : compte le nombre total de sous-dossiers qui satisfont la condition. 

Le nombre de répertoires contenant :
 
- Aucun fichier fasta : 13

Peut être directement obtenu par le commande bash : find /chemin/vers/le/dossier -mindepth 1 -type d -exec sh -c 'test -z "$(find "{}" -type f -name "*.fasta.gz" -print -quit)"' \; -print | wc -l

-exec sh -c 'test -z "$(find "{}" -type f -name "*.fasta.gz" -print -quit)"' \;: Cela exécute une commande shell pour chaque sous-dossier trouvé. La commande shell utilise find pour rechercher les fichiers ayant l'extension ".fasta.gz". 
La partie -z de test teste si la chaîne résultante est vide, ce qui signifie qu'aucun fichier avec l'extension spécifiée n'a été trouvé 

- 1 fichier fasta : 14 

- 2 fichiers fasta : 2483 

- 3 fichiers fasta : 1

- 4 fichiers fasta : 14
 
- 5 fichiers fasta : 0

- 6 fichiers fasta : 1
 
- Plus de 6 fichiers fasta : 0 

Ces valeurs ont été obtenues pour les valeurs de x de l'option '-ge' allant de 1 à 6, en soustrayant le résultat de la commande avec -ge x par le résultat de la commande avec -ge x + 1 

## Stratégie

On effectue une copie de tout les fichiers des sous-dossiers du répertoire /home/alebreton/mycocosm2024/_01_12 vers le dossier /home/mbourema/mycocosm2024/all_fasta.gz_files, en exécutant le programme copy.py.
On peut s'assurer que le nombre de fichiers copiés est de 5045 grâce à une variable n dans le script qui est incrémentée de 1 à chaque copie de fichier et qui est affichée à la fin de l'exécution du programme. On peut aussi exécuter la commande 'ls | wc -l' dans le dossier de destination.

## Pour les répertoires contenant 2 fichiers fasta
 
Sur 4966 fichiers répartis dans 2483 repertoires, on obtient 2497 fichiers qui se terminent en ‘aa.fasta.gz’, et 2499 fichiers qui ne se terminent pas en ‘aa.fasta.gz’.
On peut obtenir cette information avec l'exécution de la commande : ls /home/alebreton/mycocosm2024_01_12/**/*.fasta.gz | grep -vE 'aa.fasta.gz' | wc -l pour obtenir le nombre de fichiers qui ne se terminent pas en 'aa.fasta.gz'. 
Il suffit d'enlever le 'v' à l'argument 'grep' pour obtenir le nombre de fichiers terminant en 'aa.fasta.gz'
A l'aide de l'exécution de la commande : ls /home/mbourema/mycocosm2024/2_files_fasta.gz/**/*.fasta.gz | grep -E '*CDS.*\.fasta.gz' | wc -l on peut observer que 2498 fichiers qui ne terminenaient pas en 'aa.fasta.gz' sont des fichiers CDS avec une nomenclature de nom variable mais contenant toujours 'CDS'.
Enfin, à l'aide de la commande : ls /home/mbourema/mycocosm2024/2_files_fasta.gz/**/*.fasta.gz | grep -vE 'aa.fasta.gz|.*CDS.*\.fasta.gz' et sans ajouter l'option 'wc -l', on obtient le nombre de fichiers qui ont un nom ne finissant pas par 'fasta.gz' et qui ne contiennent pas 'CDS'.
Il y en a 1 : : Aspac1_filtered_proteins.FilteredModels6.fasta.gz -> on le renomme en Aspac1_filtered_proteins.FilteredModels6.fasta.aa.gz avec la commande 'mv', ce qui nous rammène à 2498 fichiers protéiques et 2498 ficihiers CDS.
On applique le programme copy_create.py qui copie les sous-repertoires concernés avec leur fichiers à partir de /home/mbourema/mycocosm2024/all_fasta.gz_files/ vers /home/mbourema/mycocosm2024/2_files_fasta.gz/.
Pour cela, on puise nos fichiers dans le dossier all_files_fasta.gz et on doit renseigner au script la liste des répertoires contenant moins de 2 fichiers fasta.gz,
ainsi que celle de ceux contenant plus de 2 fichiers fasta.gz, afin que le programme ne copie pas les fichiers de ces répertoires. La liste renseignée est :
‘Agabi_varbisH97_2, Agabi_varbur_1, Chagl_1, Crypa2, Hetan2, Neudi1, Neute_matA2, Phybl2, PleosPC15_2, Pospl1, Mycfi2, Triat2, TriviGv29_8_2, Aspca3, Mycgr3, PleosPC9_1, Picst3, Sporo1, Trire2, Batde5, Cante1, Cersu1, Necha2, Neute_mat_a1, SerlaS7_3_2, Spapa3, Treme1, Capcor1, Capep1, Clasps1, Claye1,
Copci_AmutBmut1, Eryha1, Kurca1, Metro1, Pendig1, Pengri1, Penita1, RhiirA4, Sodal1, Symat1, Triham1, Trias8904’. Soit 43 répertoires.

Le programme incrémente une variable de 1 à chaque copie de fichier, cette dernière étant affichée en fin d'exécution,  mais on peut aussi s’assurer que 4966 fichiers sont présents dans le répertoire final,
et utiliser la commande : find /chemin/vers/le/dossier -mindepth 1 -type d -exec sh -c 'test $(find "{}" -type f -name "*.fasta.gz" | wc -l) -ge 2 ' \; -print | wc -l pour s’assurer en faisant varier l’argument de l’option ‘ge’ de 2 à 6, que tout les répertoires contiennent bien uniquement 
2 fichiers fasta.gz, après s’être assuré qu’aucun n’en contenais 1 ou 0.

## Pour les répertoires contenant plus de 2 fichiers fasta.gz

Il y a en tout 16 répertoires contenant chacun plus de 2 fichiers fasta.gz. On peut afficher leurs chemin en utilisant la commande utilisée précédemment : find /chemin/vers/le/dossier -mindepth 1 -type d -exec sh -c 'test $(find "{}" -type f -name "*.fasta.gz" | wc -l) -ge 2 ' \; -print,
mais en ne spécifiant pas l’argument wc -l.
Les répertoires contenant au moins 3 fichiers fasta.gz sont au nombre de 16 : Capcor1, Capep1, Clasps1, Claye1, Copci_AmutBmut1, Eryha1, Kurca1, Metro1, Pendig1, Pengri1, Penita1, RhiirA4, Sodal1, Symat1, Triham1, Trias8904.
On exécute le programme copy_create.py en exécutant la 2ième partie du script relative au répertoires contenant plus de 2 fichiers fasta.gz.
Elle va copier à partir du dossier all_files_fasta.gz et vers /home/mbourema/mycocosm2024/2_more_files.fasta.gz, les fichiers des répertoires concernés et leur créer un répertoire à leur nom dans lesquel sont stockés leurs fichiers.
On renseigne au script la liste des noms des 16 répertoires.
Le script parcourt tout les fichiers du dossier all_files_fasta.gz et prend la liste des sous-dossiers contenant au moins 3 fichiers fasta.gz en paramètre et applique la copie pour chaque élément de cette liste. 
Il affiche à la fin de son exécution une variable n qui est incrémentée de 1 à chaque copie et qui est égale à 65, le nombre de fichiers pour les 16 répertoires de génomes.
En inspectant 1 à 1 ces répertoires on remarque qu’il peut y avoir plusieurs fichiers protéiques ou nucléiques qui diffèrent dans leurs annotations par leur date. Pour cela on sélectionne les plus récents en supprimant les plus anciens à l’aide de la commande ‘rm’.
Enfin il y a quelques exceptions :

Copci_AmutBmut1 contient 3 fichiers, un doublon pour le fichier cds, mais tandis que l’un possède une nomenclature avec cds en minuscule et pas de date renseignée, l’autre contient CDS majuscule et une date correspondant à celle du fichier aa.fasta.gz -> on ne garde pas le 'cds' mais le 'CDS'

Eryha1 contient 4 fichiers, 2 cds et 2 aa, avec des nomclatures spécifiant diploide ou haploide. On prend les fichiers diploides.

# Ordre d'utilisation des scripts

## copy_files

### copy_create.py

The first one to use, it will from a folder containing for each genomes downloaded from the MycoCosm portail a folder containg his AA, CDS and annotation files
create folders, for each repertory that contain at least 1 CDS, 1 AA, 1 KOG and 1 SigP file and copy on them the CDS, AA, KOG and SigP files of the genomes.
This script is divided in 2 parts, the first one create and copy repertory and files from genomes repertories that contains more than 1 CDS, AA, KOG or SigP file on
a specific repertory. The second part will do the same for repertory that contains exactly 1 CDS, AA, KOG and SigP file. Repertories that contains less than 1 CDS,
AA file are excluded.

### copy_finale.py

The second one to use. It will copy after a manual filtering of the folders that contains more than 2 AA, CDS, KOG and SigP files, all the files in all the 
repertories generated by the copy_create.py script in the desired folder

## How to use diamonds script

### assembly_but.py and assembly_but_bash

The bash script launch the python script and needs a list of all genomes names

### bad_genome.py

It finds in the diamonds output if there are misformated queries or hits which is important for the calculation of the percentages of good predictions

### reformating.py

It reformates the diamonds outputs identified by the previous script that contains misformated queries or hits

## How to use annotations script

### recup_transcriptID.R

First one to use to generate from a concatenated table of all CDS of genes of all genomes and from a concatenated table of all aa of all genes of all genomes
a table showing the correspondance between transcriptID and protID of all genes

### dico_transcriptID_protID.py

From this table this script will generate a dictionnary with a key for all genomes associated to all tuples of transcriptID and protID

### order_KOG_files.R

This script must be used before the following one, il will order the KOG annotation files of all the genomes by their protID, which is very important before
generating the following dictionnaries because it will manage the problem of protID associated with several KOG annotations 

### KOG_SiGP_dico.py

This script can then be used to generate 4 dictionnaries using all KOG annotations files, all SigP annotations files and the dictionnary generated by the
dico_transcriptID_protID.py script. It can generate 4 dictionnaries : one associating for all genomes KOG annotations to all transcriptID of their genes,
a second one doing this for all protID of their genes, and a third and a fourth one associating for all genomes transcriptID of their genes and protID of their
genes to their SignalP annotations

### KOG_SiGP.py

The script will use the "protID dictionnaries" generated in the previous step to creates 2 files for each genomes that associate to each queries of their genes
the KOG annotations and the SigP annotations.

### KOG_SiGP_queries.py

This one will then from the files generated add the KOG and SigP annotations of the queries to them. It use the "transcriptID dictionnaries".

## How to use annotations script

### recup_transcriptID.R

First one to use to generate from a concatenated table of all CDS of genes of all genomes and from a concatenated table of all aa of all genes of all genomes
a table showing the correspondance between transcriptID and protID of all genes

### dico_transcriptID_protID.py

From this table this script will generate a dictionnary with a key for all genomes associated to all tuples of transcriptID and protID

### order_KOG_files.R

This script must be used before the following one, il will order the KOG annotation files of all the genomes by their protID, which is very important before
generating the following dictionnaries because it will manage the problem of protID associated with several KOG annotations 

### KOG_SiGP_dico.py

This script can then be used to generate 4 dictionnaries using all KOG annotations files, all SigP annotations files and the dictionnary generated by the
dico_transcriptID_protID.py script. It can generate 4 dictionnaries : one associating for all genomes KOG annotations to all transcriptID of their genes,
a second one doing this for all protID of their genes, and a third and a fourth one associating for all genomes transcriptID of their genes and protID of their
genes to their SignalP annotations

### KOG_SiGP.py

The script will use the "protID dictionnaries" generated in the previous step to creates 2 files for each genomes that associate to each queries of their genes
the KOG annotations and the SigP annotations.

### KOG_SiGP_queries.py

This one will then from the files generated add the KOG and SigP annotations of the queries to them. It use the "transcriptID dictionnaries".

## calculs_pourcentages

### transform_fungaltrait.R

The first one to use because it will annotate the genomes of the fungaltrait database that lacks annotations

### all_table_percentage.data.table and all_table_percentages.R

Theses scripts will use the transformed fungaltrait database. They will calculate from each diamonds outputs the percentages of correct taxonomic, trophic and
functionnal prediction of all genomes

### transform_fungal_closest_ref.R

Last script to use, to calculate a closest taxonomic reference for all the genomes

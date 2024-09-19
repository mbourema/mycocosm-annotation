# The projet

The aim of this project is to evaluate the accuracy and reliability of annotation results for unknown fungal genomes obtained via reference based annotations in MycoCosm. This evaluation requires a comparison of expected annotations
of a genome against the annotations predicted for it by the database via a diamond blastx of its coding sequence against all the amino acid sequences of all the genomes listed in it. The approach consisted in removing each genome from the database
and querying it against the remaining genomes in a systematic way on the entire phylogeny
of the Fungi kingdom. From the resulting dataset, different combinations of taxonomy, guilds and functions were investigated (see Markdown).

# Cleaning up the Mycocosm 2024 database
## Problematic

2526 genome directories have been downloaded from the mycocosm website: 'https://mycocosm.jgi.doe.gov/mycocosm/home' in 2024. These directories include various functional annotation files, .README files, protein sequence files and nucleic sequence files.
To perform a Diamond alignment of the mycocosm genomes against the mycocosm database, the CDS (coding sequence) and AA (amino acid) files of all the genomes in the MycoCosm 2024 database must be available. The clean-up of the MycoCosm 2024 database consisted in recovering a CDS file and AA a file stored for each MycoCosm genome in a directory.

## Diagnostic

The number of genome directories obtained after downloading is obtained by running the bash command: 'ls | wc -l' after moving to the folder where they are stored: /home/alebreton/mycocosm2024_01_12/. The command displays 2526 directories.
The CDS and AA files for each genome have a '.fasta.gz' extension. The number of files with a '.fasta.gz' extension for the 2526 genome directories can be obtained using the command: ls /home/alebreton/mycocosm2024_01_12/**/** | grep -E '.fasta.gz' | wc -l
The number of '.fasta.gz' files for all directories is 5045. The command used to obtain the number of directories containing at least 1, 2, 3, 4, 5 and 6 '.fasta.gz' files respectively is :
find /home/alebreton/mycocosm2024_01_12/ -mindepth 1 -type d -exec sh -c 'test $(find “{}” -type f -name “”*.fasta.gz” | wc -l) -ge x ‘ ; -print | wc -l, specifying the minimum number of ’.fasta.gz‘ files that the directories counted must contain in place of ’x‘ for the ’-ge x' argument,
(find /path/to/the/folder -type d) searches all subdirectories in the specified folder, (- mindepth 1) means that the find command searches all subdirectories (-type d) in the specified folder, starting at a minimum depth of 1,
to avoid counting the root folder itself. Next, (-exec sh -c '[ $(find “{}” -type f -name “*.fasta.gz” | wc -l) -ge 2 ]' \) executes a shell command for each subfolder found. Here, the shell command checks whether the subfolder contains at least two files ending in '.fasta.gz'.
Finally, (-print): If the condition is true, find prints the subfolder path, (| wc -l): counts the total number of subfolders that satisfy the condition. 

The number of directories containing :
 
- No fasta files: 13

This can be obtained directly with the bash command: find /path/to/the/folder -mindepth 1 -type d -exec sh -c 'test -z “$(find ‘{}’ -type f -name ‘*.fasta.gz’ -print -quit)”' -print | wc -l

-exec sh -c 'test -z “$(find ‘{}’ -type f -name ‘*.fasta.gz’ -print -quit)”' \;: Executes a shell command for each subfolder found. The shell command uses find to search for files with the extension “.fasta.gz”.

The -z part of the test checks whether the resulting string is empty, meaning that no files with the specified extension have been found 

- 1 fasta file: 14 

- 2 fasta files: 2483 

- 3 fasta files: 1

- 4 fasta files: 14
 
- 5 fasta files: 0

- 6 fasta files: 1
 
- More than 6 fasta files: 0 

These values were obtained for x values of the '-ge' option ranging from 1 to 6, by subtracting the result of the command with -ge x from the result of the command with -ge x + 1. 

## Strategy

We copy all the files in the sub-folders of the /home/alebreton/mycocosm2024/_01_12 directory to the /home/mbourema/mycocosm2024/all_fasta.gz_files folder, by running the copy.py program.
You can check that the number of files copied is 5045 by means of a variable n in the script, which is incremented by 1 each time a file is copied and displayed at the end of program execution. You can also run the command 'ls | wc -l' in the destination folder.

## For directories containing 2 fasta files
 
Out of 4966 files in 2483 directories, we obtain 2497 files ending in 'aa.fasta.gz', and 2499 files not ending in 'aa.fasta.gz'.
This information can be obtained by executing the command: ls /home/alebreton/mycocosm2024_01_12/**/*.fasta.gz | grep -vE 'aa.fasta.gz' | wc -l to obtain the number of files not ending in 'aa.fasta.gz'. 
Simply remove the 'v' from the 'grep' argument to obtain the number of files ending in 'aa.fasta.gz'.
By executing the command: ls /home/mbourema/mycocosm2024/2_files_fasta.gz/**/*.fasta.gz | grep -E '*CDS.*\.fasta.gz' | wc -l, we can see that 2498 files that didn't end in 'aa.fasta.gz' are CDS files with a variable name nomenclature, but always containing 'CDS'.
Finally, using the command: ls /home/mbourema/mycocosm2024/2_files_fasta.gz/**/*.fasta.gz | grep -vE 'aa.fasta.gz|.*CDS.*\.fasta.gz' and without adding the 'wc -l' option, we obtain the number of files with names not ending in 'fasta.gz' and not containing 'CDS'.
There's 1: Aspac1_filtered_proteins.FilteredModels6.fasta.gz -> we rename it to Aspac1_filtered_proteins.FilteredModels6.fasta.aa.gz with the 'mv' command, which brings us back to 2498 AA files and 2498 CDS files.
We apply the copy_create.py program, which copies the relevant sub-directories with their files from /home/mbourema/mycocosm2024/all_fasta.gz_files/ to /home/mbourema/mycocosm2024/2_files_fasta.gz/.
To do this, we draw our files from the all_files_fasta.gz folder and we must inform the script of the list of directories containing less than 2 fasta.gz files,
as well as those containing more than 2 fasta.gz files, so that the program doesn't copy files from these directories. The list entered is :
'Agabi_varbisH97_2, Agabi_varbur_1, Chagl_1, Crypa2, Hetan2, Neudi1, Neute_matA2, Phybl2, PleosPC15_2, Pospl1, Mycfi2, Triat2, TriviGv29_8_2, Aspca3, Mycgr3, PleosPC9_1, Picst3, Sporo1, Trire2, Batde5, Cante1, Cersu1, Necha2, Neute_mat_a1, SerlaS7_3_2, Spapa3, Treme1, Capcor1, Capep1, Clasps1, Claye1,
Copci_AmutBmut1, Eryha1, Kurca1, Metro1, Pendig1, Pengri1, Penita1, RhiirA4, Sodal1, Symat1, Triham1, Trias8904'. A total of 43 directories.

The program increments a variable by 1 each time a file is copied, and this is displayed at the end of execution, but we can also ensure that 4966 files are present in the final directory,
and use the command: find /path/to/the/folder -mindepth 1 -type d -exec sh -c 'test $(find “{}” -type f -name “*.fasta.gz” | wc -l) -ge 2 ' ; -print | wc -l to ensure, by varying the argument of the 'ge' option from 2 to 6, that all directories contain only 
2 fasta.gz files, after checking that none contain 1 or 0.

## For directories containing more than 2 fasta.gz files

There are 16 directories containing more than 2 fasta.gz files. We can display their paths using the command used previously: find /path/to/the/folder -mindepth 1 -type d -exec sh -c 'test $(find “{}” -type f -name “*.fasta.gz” | wc -l) -ge 2 ' \; -print,
but without specifying the wc -l argument.
There are 16 directories containing at least 3 fasta.gz files: Capcor1, Capep1, Clasps1, Claye1, Copci_AmutBmut1, Eryha1, Kurca1, Metro1, Pendig1, Pengri1, Penita1, RhiirA4, Sodal1, Symat1, Triham1, Trias8904.
We run the copy_create.py program by executing the 2nd part of the script relating to directories containing more than 2 fasta.gz files.
It will copy from the folder all_files_fasta.gz to /home/mbourema/mycocosm2024/2_more_files.fasta.gz, the files in the directories concerned and create a directory in their name in which to store their files.
The script is given a list of the names of the 16 directories.
The script browses all the files in the all_files_fasta.gz folder and takes the list of sub-folders containing at least 3 fasta.gz files as parameters, and applies the copy for each item in this list. 
At the end of its execution, it displays a variable n which is incremented by 1 with each copy and equals 65, the number of files for the 16 genome directories.
Inspecting these directories 1 by 1, we notice that there may be several protein or nucleic files whose annotations differ by date. To do this, select the most recent and delete the oldest using the 'rm' command.
Finally, there are a few exceptions:

Copci_AmutBmut1 contains 3 files, a duplicate for the cds file, but while one has a nomenclature with lower-case cds and no date, the other contains upper-case CDS and a date corresponding to that of the aa.fasta.gz file -> we don't keep the 'cds' but the 'CDS'.

Eryha1 contains 4 files, 2 cds and 2 aa, with nomclatures specifying diploid or haploid. We take the diploid files.

# Order of use for the scripts

## How to use copy script

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

It finds in the diamonds outputs if there are misformated queries or hits which is important for the calculation of the percentages of good predictions

### reformating.py

It reformates the diamonds outputs identified by the previous script that contains misformated queries or hits

## How to use annotations script

### recup_transcriptID.R

First one to use to generate from a concatenated table of all CDS of genes of all genomes and from a concatenated table of all AA sequence of all genes of all genomes
a table showing the correspondance between transcriptID and protID of all genes of all genomes

### dico_transcriptID_protID.py

From this table this script will generate a dictionnary with a key for all genomes associated to all tuples of transcriptID and protID

### order_KOG_files.R

This script will order the KOG annotation files of all the genomes by their protID, which is very important before
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

## How to use calculs scripts

### transform_fungaltrait.R

The first one to use because it will annotate the genomes of the fungaltrait database that lacks annotations

### all_table_percentage.data.table and all_table_percentages.R

Theses scripts will use the transformed fungaltrait database. They will calculate from each diamonds outputs the percentages of correct taxonomic, trophic and
functionnal prediction of all genomes

### transform_fungal_closest_ref.R

Last script to use, to calculate a closest taxonomic reference for all the genomes

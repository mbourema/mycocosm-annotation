library(tidyverse) # Importation of the tidyverse library

###############################################################################################################################################################################
# This program takes as input a file containing all informations about all genomes CDS (database, genome name, transcriptID and description) and a file containing all 
# informations about all genomes Amino acid sequence (database, genome name, protID and description) and create a table where for each genomes transcriptsID are 
# associated to protIDs 
###############################################################################################################################################################################

# Read the file containing all transcriptID of all genes of genomes 
cds_aa_columns <- "Myc_contig"
diamonds_cds <- read.delim("/home/mbourema/all_cds_transcriptID", header = FALSE, col.names = cds_aa_columns) %>% separate(Myc_contig, c("db_CDS","JGI_ID_CDS","transcriptID","descr"), sep = "\\|") %>% select(JGI_ID_CDS, transcriptID, descr)
# Read the file containing all protID of all genes of genomes
diamonds_aa <- read.delim("/home/mbourema/all_aa_protID", header = FALSE, col.names = cds_aa_columns) %>% separate(Myc_contig, c("db_aa","JGI_ID_aa","protID","descr"), sep = "\\|") %>% select(JGI_ID_aa, protID, descr)
# Merging of the two files by JGI_ID and description to associate all transcriptID to all protID
diamonds_cds_aa <-  diamonds_cds %>% left_join(diamonds_aa, by=c("descr"="descr", "JGI_ID_CDS"="JGI_ID_aa")) %>% select(JGI_ID_CDS, transcriptID, protID) %>% rename(JGI_ID = JGI_ID_CDS)
# Write the table
write_delim(diamonds_cds_aa, file = "/home/mbourema/transcriptID_protID", delim = "\t")

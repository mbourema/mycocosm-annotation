library(tidyverse) #Importation of the tidyverse library
library(dplyr) #Importation of the dplyr library

###############################################################################################################################################################################
# Order all annotation file lines in function of the protID column or the transcriptID column
###############################################################################################################################################################################

# Definition of the folder path containing the annotation files 
KOGs_folder <- "/home/mbourema/mycocosm2024/mycocosm2024_purified/all_KOG_files"

# List of the files annotation paths
files_list <- list.files(path = KOGs_folder, full.names = TRUE)

# For each file in the folder
for (file_path in files_list) {
    # Read the file and add columns names
    df <- read.table(file_path, sep = "\t", header = FALSE, col.names = c("transcriptId", "proteinId", "kogid", "kogdefline", "kogClass", "kogGroup"), comment.char = "#")

    # Order the dataframe in function of the protID column
    df <- arrange(df, proteinId)

    # Extract the file name
    file_name <- basename(file_path)

    # Save path of the ordered dataframe
    output_path <- file.path("/home/mbourema/mycocosm2024/mycocosm2024_purified/all_KOG_files_ordered", file_name)

    # Write the ordered dataframe in a file
    write.table(df, file = output_path, sep = "\t", quote = FALSE, row.names = FALSE)
}

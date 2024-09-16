###############################################################################################################################################################################
# This program takes the fungaltrait database as input and annotate the genomes that have no taxonomic values from an excel file
###############################################################################################################################################################################

library("tidyr") # Importation of the tidyverse library
library("readr") # Importation of the readr library
library("dplyr") # Importation of the dplyr library
library('openxlsx') # Importation of the openxlsx library

# Importation of the fungaltrait database
fungal <- read.delim("~/Desktop/R scripts/Markdown/fungaltrait2024.txt")
# Importation of the excel file containing the annotation of the 7 non annoted genomes
unknown_genomes <- read.xlsx("7 génomes.xlsx")

### Function to transform data

transform_data <- function(data) {
  transformed_data <- data %>%
    mutate(
      Genus = case_when(JGI_ID %in% c("AgarPMI687_1", "Cap6580_1", "Cha5317_1", "Epi6094_1", "Inolan1", "Thiap1", "Thihy1") ~ unknown_genomes$Genus[match(JGI_ID, unknown_genomes$JGI_ID)],
                        Genus == "Unclassified" ~ paste("Unclassified_", JGI_ID),
                        TRUE ~ Genus),
      Family = case_when(JGI_ID %in% c("AgarPMI687_1", "Cap6580_1", "Cha5317_1", "Epi6094_1", "Inolan1", "Thiap1", "Thihy1") ~ unknown_genomes$Family[match(JGI_ID, unknown_genomes$JGI_ID)],
                         grepl("incertae sedis", Class) & Order == "Unclassified" & Family == "Unclassified" ~ paste(Phylum, "family incertae sedis"),
                         !grepl("incertae sedis", Class) & Order == "Unclassified" & Family == "Unclassified" ~ paste(Class, "family incertae sedis"),
                         !grepl("incertae sedis", Order) & Order != "Unclassified" & Family == "Unclassified" ~ paste(Order, "family incertae sedis"),
                         TRUE ~ Family),
      Order = case_when(JGI_ID %in% c("AgarPMI687_1", "Cap6580_1", "Cha5317_1", "Epi6094_1", "Inolan1", "Thiap1", "Thihy1") ~ unknown_genomes$Order[match(JGI_ID, unknown_genomes$JGI_ID)],
                        grepl("incertae sedis", Class) & Order == "Unclassified" ~ paste(Phylum, "order incertae sedis"),
                        !grepl("incertae sedis", Class) & Order == "Unclassified" ~ paste(Class, "order incertae sedis"),
                        TRUE ~ Order),
      Class = case_when(JGI_ID %in% c("AgarPMI687_1", "Cap6580_1", "Cha5317_1", "Epi6094_1", "Inolan1", "Thiap1", "Thihy1") ~ unknown_genomes$Class[match(JGI_ID, unknown_genomes$JGI_ID)],
                        TRUE ~ Class),
      Phylum = case_when(JGI_ID %in% c("AgarPMI687_1", "Cap6580_1", "Cha5317_1", "Epi6094_1", "Inolan1", "Thiap1", "Thihy1") ~ unknown_genomes$Phylum[match(JGI_ID, unknown_genomes$JGI_ID)],
                         TRUE ~ Phylum)) 
  
  return(transformed_data)
}

# filter na genomes
fungal_transformed <- transform_data(fungal) %>% filter(!is.na(JGI_ID))
write_delim(fungal_transformed , file = "/Users/mehdi/Desktop/fungaltrait2024_transformed", delim = "\t")

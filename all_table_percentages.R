###############################################################################################################################################################################
# Same script as all_table_percentages.data.table but using the tidyverse library
###############################################################################################################################################################################

# Importation of tidyverse library for a concise and efficient manipulation, visualization and data analysis. Tidyverse contains ggplot2.
library('tidyverse')

### FUNCTIONS 
# function for importing the diamond file in a table format, adding to him columns names, importing the fungal traits file, renaming his columns, and joining him with the diamond file by the "JGI_ID" columns 
import_diamond10_MycData <- function(diamond_Myc) {
  ## Diamond file
  #Mycnames <- c("Myc_contig", "Myc_Hit", "Myc_description", "Myc_score", "Myc_evalue", "Myc_coverage") #column names of the diamond file
  MycAn <- read.table(diamond_Myc, sep="\t", quote="", header=TRUE, fill=TRUE, comment.char = "") #read diamond file and add the column names
  ## FunGuild
  portal_data <- read_delim("/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/real_transformed_fungal", delim="\t", escape_double = FALSE, trim_ws = TRUE) #read fungaltraits data
  MycFG <- MycAn %>% separate(Myc_Hit, c("db", "JGI_ID", "ID", "descr"), sep="\\|", extra = "drop") %>% #split sequence ID in 4 columns, one will contain the JGI_ID
    left_join(portal_data, by="JGI_ID") %>% #merge diamond file and fungaltraits file
    rename(pred_Phylum = Phylum, pred_Class = Class, pred_Order = Order, pred_Family = Family, pred_Genus = Genus, pred_primary_lifestyle = primary_lifestyle, pred_Secondary_lifestyle = Secondary_lifestyle) %>% #renaming of the fungal traits columns
    mutate(pred_guild = case_when(pred_primary_lifestyle %in% c("ectomycorrhizal") ~ "Ectomycorrhizal",
                                  pred_primary_lifestyle %in% c("soil_saprotroph","unspecified_saprotroph","litter_saprotroph","wood_saprotroph","dung_saprotroph","fungal_decomposer") | pred_Secondary_lifestyle %in% c("dung_saprotroph","litter_saprotroph","unspecified_saprotroph","soil_saprotroph","wood_saprotroph","fungal_decomposer") ~ "Saprotroph",
                                  pred_primary_lifestyle %in% c("unspecified_pathotroph","plant_pathogen") | pred_Secondary_lifestyle %in% c("unspecified_pathotroph","plant_pathogen") ~ "Pathotroph",
                                  TRUE ~ "Others")) #add the pred_guild column
  return(MycFG)
}

### import files
# Genomes diamond file

diamond <- import_diamond10_MycData(file.path("/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/all_diamonds_final_light")) #Importation of the diamond file corresponding to file_name

# Fungaltraits genomes metadata
fungal <- read_delim("/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/real_transformed_fungal", "\t", escape_double = FALSE, trim_ws = TRUE) %>%
  select(JGI_ID, Phylum, Class, Order, Family, Genus, primary_lifestyle, Secondary_lifestyle) %>% #select only relevant columns
  rename(exp_JGI_ID = JGI_ID, exp_Phylum = Phylum, exp_Class = Class, exp_Order = Order, exp_Family = Family, exp_Genus = Genus, exp_primary_lifestyle = primary_lifestyle, exp_Secondary_lifestyle = Secondary_lifestyle) %>% # Rename them
  mutate(exp_guild = case_when(exp_primary_lifestyle %in% c("ectomycorrhizal") ~ "Ectomycorrhizal",
                               exp_primary_lifestyle %in% c("soil_saprotroph","unspecified_saprotroph","litter_saprotroph","wood_saprotroph","dung_saprotroph","fungal_decomposer") | exp_Secondary_lifestyle %in% c("dung_saprotroph","litter_saprotroph","unspecified_saprotroph","soil_saprotroph","wood_saprotroph","fungal_decomposer") ~ "Saprotroph",
                               exp_primary_lifestyle %in% c("unspecified_pathotroph","plant_pathogen") | exp_Secondary_lifestyle %in% c("unspecified_pathotroph","plant_pathogen") ~ "Pathotroph",
                               TRUE ~ "Others")) #add the exp_guild column

### sorting Life_style and guild
final_data <- diamond %>%
  separate(Myc_contig, sep="\\|", into=c("jgi","exp_JGI_ID","ref_ID","ref_descr"), remove=FALSE) %>% #split sequence ID
  left_join(fungal, by="exp_JGI_ID") %>% #join the fungal traits genomes metadata and the diamond genomes metadata
  mutate(compare_life_style = case_when((is.na(JGI_ID) ~ 'NO-HIT'), (pred_primary_lifestyle == exp_primary_lifestyle | pred_primary_lifestyle == exp_Secondary_lifestyle | pred_Secondary_lifestyle == exp_primary_lifestyle | pred_Secondary_lifestyle == exp_Secondary_lifestyle ~ 'MATCH'), TRUE ~ 'NO-MATCH')) %>%
  mutate(compare_guild = case_when(is.na(JGI_ID) ~ "NO-HIT",
                                   pred_guild == exp_guild ~ "correct_guild",
                                   TRUE ~ "incorrect_guild")) %>% # adding of compare_life_style and compare_guild columns
  select("exp_JGI_ID", "compare_life_style", "compare_guild") %>% # selection of the relevant columns
  mutate(alignments_count = 1) %>% # add a column which value is 1 for each row
  group_by(exp_JGI_ID) %>% mutate(number_alignments = sum(alignments_count)) %>% # add a column that will count for each genome the number of diamond genes hit
  mutate(total_na = sum(compare_life_style == 'NO-HIT')) %>% mutate (total_match = sum(compare_life_style == 'MATCH')) %>% # add of columns that count the number of 'NO-HIT' and 'MATCH' for each genomes
  mutate(percentage_life_style_match = (total_match/number_alignments)*100) %>% # add a column that will show for each genomes the percentage of life_style match
  mutate(percentage_na = (total_na/number_alignments)*100) %>% # add a column that will show for each genomes the percentage of no-hit
  mutate(total_no_hit = sum(compare_guild == "NO-HIT")) %>% mutate(total_match_guild = sum(compare_guild == "correct_guild")) %>% mutate(total_no_match_guild = sum(compare_guild == "incorrect_guild")) %>% #add columns that count the number of "NO-HIT", "correct_guild" and "incorrect_guild" for the compare_guild column
  mutate(percentage_guild_match = (total_match_guild/number_alignments)*100) %>% mutate(percentage_no_hit_guild = total_no_hit/number_alignments * 100) %>% mutate(percentage_no_match_guild = total_no_match_guild/number_alignments * 100) %>% # add columns that count the percentages of guild_match, no hit and guild_no_match
  ungroup() %>% select("exp_JGI_ID", "percentage_life_style_match", "total_na", "percentage_na", "percentage_guild_match", "percentage_no_hit_guild", "percentage_no_match_guild") #select relevent columns

percentage_life_style_match_myc <- final_data %>% distinct() # Selection of one row per genome
life_style <- percentage_life_style_match_myc %>% select(-percentage_na, -percentage_no_hit_guild, percentage_no_match_guild, -total_na, -percentage_no_match_guild) #select only the columns we will add to the taxonomy table

### sorting TAXONOMY
correct_data <- diamond %>% mutate(gene_count=1) %>%  #add gene_count column, set value to 1 for each line
  separate(Myc_contig, sep="\\|", convert = TRUE, into=c("jgi","exp_JGI_ID","ref_ID","ref_descr"), remove=FALSE) %>% #split sequence ID
  left_join(fungal, by="exp_JGI_ID") %>% #join the fungal traits genomes metadata and the diamond genomes metadata
  mutate(compare_tax = case_when(is.na(pred_Phylum) ~ "NoHit", pred_Genus == exp_Genus ~ "correct_genus", pred_Family == exp_Family ~ "correct_family", pred_Order == exp_Order ~ "correct_order", pred_Class == exp_Class ~ "correct_class", pred_Phylum == exp_Phylum ~ "correct_phylum", TRUE ~ "NO_TAXONOMIC_MATCH")) %>%
  group_by(exp_JGI_ID) %>% mutate(genome_gene_number=sum(gene_count)) %>% # group by genome and sum 'gene_counts' (provide total number of gene per genome)
  group_by(exp_JGI_ID, compare_tax, genome_gene_number) %>% summarise(total=sum(gene_count)) %>% # group by genome and correct taxonomy level and genome_gene_number and summarise (by sum of genes) to get how many genomes for each value of compare tax
  ungroup() %>%
  pivot_wider(names_from=compare_tax, values_from=total, values_fill = 0) %>% #creates columns according to the values of compare_tax and create columns which values will be calculated from the values of the created columns
  group_by(exp_JGI_ID) %>%
  mutate(genus = case_when(exists("correct_genus") ~ correct_genus/genome_gene_number * 100, TRUE ~ 0),
         family = case_when(exists("correct_family") ~ correct_family/genome_gene_number * 100 + genus, TRUE ~ genus),
         order = case_when(exists("correct_order") ~ correct_order/genome_gene_number * 100 + family, TRUE ~ family),
         class = case_when(exists("correct_class") ~ correct_class/genome_gene_number * 100 + order, TRUE ~ order),
         phylum = case_when(exists("correct_phylum") ~ correct_phylum/genome_gene_number * 100 + class, TRUE ~ class),
         noHit = case_when(exists("NoHit") ~ NoHit/genome_gene_number * 100, TRUE ~ 0),
         no_taxonomic_match = case_when(exists("NO_TAXONOMIC_MATCH") ~ NO_TAXONOMIC_MATCH/genome_gene_number * 100, TRUE ~ 0)) %>% left_join(life_style, by="exp_JGI_ID") %>%
  ungroup() %>%
  pivot_longer(cols=c(genus, family, order, class, phylum, noHit, no_taxonomic_match, percentage_life_style_match, percentage_guild_match), names_to="compare_tax", values_to = "relative")

if("correct_genus" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-correct_genus)
}
if("correct_class" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-correct_class)
}
if("correct_family" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-correct_family)
}
if("correct_order" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-correct_order)
}
if("correct_phylum" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-correct_phylum)
}
if("NO_TAXONOMIC_MATCH" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-NO_TAXONOMIC_MATCH)
}
if("NoHit" %in% colnames(correct_data)) {
  correct_data <- correct_data %>% select(-NoHit)
}
correct_data <- correct_data %>% select(-genome_gene_number)

### KOG and SigP
KOG_columns <- c("contig", "Pred_proteinId", "Pred_kogid", "Pred_kogdefline", "Pred_kogClass", "Pred_kogGroup", "proteinId", "kogid", "kogdefline", "kogClass", "kogGroup")
diamond_KOG <- read_delim("/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/all_KOG", delim="\t", quote="", col_names=KOG_columns, escape_double = FALSE, trim_ws = TRUE)
diamond_KOG_separated <- diamond_KOG %>% separate(contig, c("db", "JGI_ID", "ID", "descr"), sep="\\|", extra = "drop") %>% group_by(JGI_ID) %>%
  mutate(count = 1) %>% mutate(total_count = sum(count)) %>%
  mutate(number_good_predicted_kogdefline = case_when(kogdefline == Pred_kogdefline ~ 1,
                                                 TRUE ~ 0)) %>% mutate(percentage_good_prediction_kogdefline = (sum(number_good_predicted_kogdefline)/total_count)*100) %>%
  mutate(number_bad_predicted_kogdefline = case_when(kogdefline != Pred_kogdefline & Pred_kogdefline != "Unknown" & Pred_kogdefline != "NoHit" ~ 1,
                                                     TRUE ~ 0)) %>% mutate(percentage_wrong_prediction_kogdefline = (sum(number_bad_predicted_kogdefline)/total_count)*100) %>%
  mutate(number_no_kogdefline_predicted = case_when(Pred_kogClass == "Unknown" | Pred_kogClass == "NoHit"  ~ 1,
                                               TRUE ~ 0)) %>% mutate(percentage_no_kogdefline_predicted = (sum(number_no_kogdefline_predicted)/total_count)*100) %>%
  select(JGI_ID, percentage_good_prediction_kogdefline, percentage_wrong_prediction_kogdefline, percentage_no_kogdefline_predicted) %>% distinct()

sigP_columns <- c("contig", "Pred_nn_cutpos", "Pred_neuro_net_vote", "Pred_hmm_cutpos", "Pred_hmm_signalpep_probability", "proteinid", "nn_cutpos", "neuro_net_vote", "hmm_cutpos", "hmm_signalpep_probability")
diamond_sigP <- read_delim("/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/all_SigP", delim="\t", quote="", col_names=sigP_columns, escape_double = FALSE, trim_ws = TRUE)
diamond_sigP_separated <- diamond_sigP %>% separate(contig, c("db", "JGI_ID", "ID", "descr"), sep="\\|", extra = "drop") %>% group_by(JGI_ID) %>%
  mutate(secreted = case_when(hmm_signalpep_probability == "Unknown" | hmm_signalpep_probability == "NoHit" | hmm_signalpep_probability < 0.8 ~ "Not_Secreted",
                                   TRUE ~ "Secreted")) %>%
  mutate(pred_secreted = case_when(Pred_hmm_signalpep_probability == "Unknown" | Pred_hmm_signalpep_probability == "NoHit" | Pred_hmm_signalpep_probability < 0.8 ~ "Not_Secreted",
                                   TRUE ~ "Secreted")) %>%
  mutate(secreted_count = case_when(secreted == "Secreted" ~ 1,
                                    TRUE ~ 0)) %>% mutate(sum_secreted = sum(secreted_count)) %>%
  mutate(not_secreted_count = case_when(secreted == "Not_Secreted" ~ 1,
                                    TRUE ~ 0)) %>% mutate(sum_not_secreted = sum(not_secreted_count)) %>%
  mutate(TRUE_POSITIVE_count = case_when(secreted == "Secreted" & pred_secreted == secreted ~ 1,
                                         TRUE ~ 0)) %>% mutate(pred_TRUE_POSITIVE_total_count = sum(TRUE_POSITIVE_count)) %>% mutate(pred_percentage_TRUE_POSITIVE = (pred_TRUE_POSITIVE_total_count/sum_secreted)*100) %>%
  mutate(TRUE_NEGATIVE_count = case_when(secreted == "Not_Secreted" & pred_secreted == secreted ~ 1,
                                             TRUE ~ 0)) %>% mutate(pred_TRUE_NEGATIVE_total_count = sum(TRUE_NEGATIVE_count)) %>% mutate(pred_percentage_TRUE_NEGATIVE = (pred_TRUE_NEGATIVE_total_count/sum_not_secreted)*100) %>%
  mutate(FALSE_POSITIVE_count = case_when(pred_secreted == "Secreted" & secreted == "Not_Secreted"~ 1,
                                        TRUE ~ 0)) %>% mutate(pred_FALSE_POSITIVE_total_count = sum(FALSE_POSITIVE_count)) %>% mutate(pred_percentage_FALSE_POSITIVE = (pred_FALSE_POSITIVE_total_count/sum_not_secreted)*100) %>%
  mutate(FALSE_NEGATIVE_count = case_when(pred_secreted == "Not_Secreted" & secreted == "Secreted"~ 1,
                                      TRUE ~ 0)) %>% mutate(pred_FALSE_NEGATIVE_total_count = sum(FALSE_NEGATIVE_count)) %>% mutate(pred_percentage_FALSE_NEGATIVE = (pred_FALSE_NEGATIVE_total_count/sum_secreted)*100) %>%
  select(JGI_ID, pred_percentage_TRUE_POSITIVE, pred_percentage_TRUE_NEGATIVE, pred_percentage_FALSE_POSITIVE, pred_percentage_FALSE_NEGATIVE) %>% distinct() %>% left_join(diamond_KOG_separated, by="JGI_ID")

# Calcul du nombre de de protéine ayant un KOG defline inconnu malgrès qu'elles soient sécrétées
diamond_KOG_sigP <- diamond_KOG %>% left_join(diamond_sigP, by = "contig") %>% select(kogdefline, hmm_signalpep_probability) %>% mutate(count = 1) %>% mutate(number = sum(count)) %>% mutate(type = case_when(kogdefline == "Unknown" & hmm_signalpep_probability != "Unknown" & hmm_signalpep_probability >= 0.8 ~ 1, TRUE ~ 0)) %>%
  mutate(percentage_unknown_secreted = (sum(type)/number)*100) %>% select(percentage_unknown_secreted) %>% distinct()

write_delim(diamond_KOG_sigP, file="/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/percentage_of_unknown_secreted1", delim="\t")

options(scipen = 999) # Deactivate the scientifique notation for decimal numbers

taxo_life_style_functions_percentages <- correct_data %>% pivot_wider(names_from = compare_tax, values_from = relative) %>% left_join(diamond_sigP_separated, by = c("exp_JGI_ID"="JGI_ID")) %>% pivot_longer(cols = genus:percentage_no_kogdefline_predicted, names_to = "Compare_tax", values_to = "Percentages")

write_delim(taxo_life_style_functions_percentages, file="/home/mbourema/mycocosm2024/mycocosm2024_purified/R_script/percentage_taxo_guild_function_R", delim="\t")

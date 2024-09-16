import pandas as pd # importation of the pandas module
import json # importation of the json module

################################################################################################################################################################################
#Permet d obtenir à partir d un tableau associant les transcriptID et les protID de tout les gènes de tout les génomes (la colonne 'JGI_ID' contient le nom de tout les génomes)
#un dictionnaire qui prends pour clé tous les génomes et pour valeurs des tuples transcriptID et protID
################################################################################################################################################################################

# Path of the table and of the output
table_path = "/home/mbourema/python/removing_sequences/second_approach/transcript_ID_prot_ID"
dico_transcriptID_protID_path = "/home/mbourema/python/removing_sequences/second_approach/dico_transcriptID_protID"

# Read the csv table
data = pd.read_csv(table_path, sep='\t', dtype={'JGI_ID': str, 'transcriptID': str, 'protID': str})

# Initialization of the dictionnary
dico_transcriptID_protID_final = {}

# For each genome of the table
for jgi_id, group_data in data.groupby('JGI_ID'):
    # Cration of a dictionnary associating transcriptID and protID
    dico_transcriptID_protID = dict(zip(group_data['transcriptID'], group_data['protID']))
    # Adding of this dictionnary to the final dictionnay
    dico_transcriptID_protID_final[jgi_id] = dico_transcriptID_protID

'''
# Write the dictionnary on a JSON file
with open(dico_transcriptID_protID_path, 'w') as f:
    json.dump(dico_transcriptID_protID_final, f)
'''

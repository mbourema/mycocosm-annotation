import os,sys # Importation of os and sys modules
import json # Importation of the json module

###############################################################################################################################################################################
# For each diamond file, creation of a file containing the query of each gene of the genome, and the annotation (KOG or SigP) of the hit of this query, associated with the
# protID of the hit. This program needs the KOG and SigP hits dictionnaries and a repertory containing the diamonds outputs. Hits and queries positions are to adapt with
# the diamond file structure
###############################################################################################################################################################################

# Recovery of the list containing the names of the diamonds files
diamond_file = sys.argv[1]
# Path of each diamonds files
diamond_files = "/home/mbourema/mycocosm2024/mycocosm2024_purified/files_diamonds_incase/" + str(diamond_file)

# Loading of the dictionnaries containing KOG and SigP annotations associated with the protIDs
'''
with open("/home/mbourema/mycocosm2024/mycocosm2024_purified/dico.KOG_hits.json", "r") as f:
	d1 = json.load(f)
'''
with open("/home/mbourema/mycocosm2024/mycocosm2024_purified/dico.SigP_hits.json", "r") as f:
	d2 = json.load(f)

### KOG annotation of the diamond file
# Create a new file
output1 = open("/home/mbourema/mycocosm2024/mycocosm2024_purified/KOG_SigP_incase/" + str(diamond_file) + "." + "KOG", "w")

# Column number for all annotation types
col1_nb = 5

# Open the diamond file
with open(diamond_files) as f:
	for line in f:
		if line.strip(): # for each line that is not empty recovery of the hit and the query (depending of structure of the diamond file)
			myhit = line.split('\t')[4]
			myquery = line.split('\t')[0] + "|" + line.split('\t')[1] + "|" + line.split('\t')[2] + "|" + line.split('\t')[3]
			output1.write(str(myquery) + "\t")
			if myhit.startswith("jgi") :
				myID = myhit.split('|')
				myspecies = myID[1]
				myprotID = myID[2]
				if d1[myspecies].get(myprotID) is not None:
					mycolumn = [0] * col1_nb
					for i in range(0, col1_nb, 1): 
						mycolumn[i] = str(d1[myspecies][myprotID][i])
						if i < (col1_nb-1):
							output1.write(mycolumn[i]+"\t")
						elif i == (col1_nb-1):
							output1.write(mycolumn[i]+"\n")
				else:
					for i in range(0, col1_nb, 1):
						if i < (col1_nb-1):
							output1.write("Unknown\t")
						elif i == (col1_nb-1):
							output1.write("Unknown\n")
			else:
				for i in range(0, col1_nb,1):    #for each column fill with NoHit
					if i < (col1_nb-1):
						output1.write("NoHit\t")
					elif i == (col1_nb-1):
						output1.write("NoHit\n")

output1.close()


### SigP annotation of the diamond file
# Create a new file
output2 = open("/home/mbourema/mycocosm2024/mycocosm2024_purified/KOG_SigP_incase/" +str(diamond_file) + "." + "SigP", "w")

# Column number for all annotation types
col2_nb = 4

# Open the diamond file
with open(diamond_files) as f:
	for line in f:
		if line.strip():
			myhit = line.split('\t')[1]
			myquery = line.split('\t')[0]
			output2.write(str(myquery) + "\t")
			if myhit.startswith("jgi") :
				myID = myhit.split('|')
				myspecies = myID[1]
				myprotID = myID[2]
				if d2[myspecies].get(myprotID) is not None:
					mycolumn = [0] * col2_nb
					for i in range(0, col2_nb, 1): 
						mycolumn[i] = str(d2[myspecies][myprotID][i])
						if i < (col2_nb-1):
							output2.write(mycolumn[i]+"\t")
						elif i == (col2_nb-1):
							output2.write(mycolumn[i]+"\n")
				else :
					for i in range(0, col2_nb, 1):
						if i < (col2_nb-1):
							output2.write("Unknown\t")
						elif i == (col2_nb-1):
							output2.write("Unknown\n")
			else:
				for i in range(0, col2_nb,1): 
					if i < (col2_nb-1):
						output2.write("NoHit\t")
					elif i == (col2_nb-1):
						output2.write("NoHit\n")

output2.close()

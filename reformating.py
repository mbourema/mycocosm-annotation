###############################################################################################################################################################################
# Script for reformating hits and queries of wrong formated diamonds files. Wrong formated files needs to be stored in the repertory specified by bad_genomes_path
###############################################################################################################################################################################

import shutil
import os

reformated_files_path = "/home/mbourema/mycocosm2024/mycocosm2024_purified/reformated_files/"
bad_genomes_path = "/home/mbourema/mycocosm2024/mycocosm2024_purified/bad_files/"

list_bad_diamonds = os.listdir(bad_genomes_path)

for diamond in list_bad_diamonds :
	diamond_output = open("/home/mbourema/mycocosm2024/mycocosm2024_purified/files_diamonds_incase/" +str(diamond), "w")
	path= os.path.join(diamonds_path, diamond)

	with open(path) as f :
		for line in f:
			query = line.split('\t')[0]
			hit = line.split('\t')[1]
			hit2 = line.split('\t')[2]
			score = line.split('\t')[3]
			evalue = line.split('\t')[4]
			coverage = line.split('\t')[5]
			if "jgi" not in query:
				query = "jgi|Altbr1|" + query[2:7] + "|" + query[2:7]
				query = query.replace("0","")
				diamond_output.write(query+"\t"+hit+"\t"+hit2+"\t"+score+"\t"+evalue+"\t"+coverage+"\n")
			elif "jgi" not in hit and "*" not in hit:
				hit = "jgi|Altbr1|" + hit[2:7] + "|" + hit[2:7]
				hit = hit.replace("0","")
				diamond_output.write(query+"\t"+hit+"\t"+hit2+"\t"+score+"\t"+evalue+"\t"+coverage+"\n")
			else:
				diamond_output.write(query+"\t"+hit+"\t"+hit2+"\t"+score+"\t"+evalue+"\t"+coverage+"\n")

def convert_gizapp_to_score_alignments_format(gizapp_alignments_file,output_filename):
	
	with open(gizapp_alignments_file) as a:
		gizapp_alignments=a.readlines()
	
	new_alignments=[]
	with open(output_filename,'w') as o:	
		for line in gizapp_alignments:
			new_alignment=''
			line=line.split()
			for i in range(0,len(line),2):
				new_alignment+=line[i+1]+'-'+line[i]+' '	# the indexes are inverted and the alignments are written in the form 'index(tw)-index(sw)'
			o.write(new_alignment+'\n')	

if __name__ == '__main__':

	convert_gizapp_to_score_alignments_format('giza-pp/results3/117-01-23.170229.francesca.A3.20','gizapp_model1+3_20iterations_alignments.txt')

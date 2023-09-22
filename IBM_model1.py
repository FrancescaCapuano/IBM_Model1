from pathlib import Path
import subprocess

class IBM_Model1:

	def __init__(self,source_sents,target_sents,iterations):		
		# the source and target sentences have to be 
		# stripped, split and appended to a list
		# we insert the NULL alignment at position 0 of all source sentences
		for sent in source_sents:
			sent.insert(0,'NULL')
		self.source_sents=source_sents
		self.target_sents=target_sents
		self.iterations=iterations
		self.theta=dict()
		self.__EM()

	def __EM(self):
		'''
		theta is initialized: it is a dictionary, where the keys are the words of the 
		source corpus (s), the values are dictionaries where the keys are the words (t)
		that appear in the target sentences corresponding to the source sentences
		where s was found. Each theta[s][t] stores the probability p(t|s).
		'''
		for n in range(len(self.target_sents)):
			for t in self.target_sents[n]:
				for s in self.source_sents[n]:
					if s not in self.theta.keys():
						self.theta[s]=dict()
					if t not in self.theta[s].keys():
						self.theta[s][t]=1 # each probability is initilized with 1


		for s in self.theta.keys():
			Z=len(self.theta[s].keys())
			for t in self.theta[s].keys():
				self.theta[s][t]=self.theta[s][t]/Z # the probabilities are normalized:
				# all p(tx|s) have to sum up to 1 for each s. Therefore, p(t|s) = sum_of_all p(tx|s)
				# divided by number of all t that appear with s.


		# the EM algorithm is repeated self.iterations times.
		for i in range(self.iterations):
			# a self.counts dictionary is instantiated. It has the same structures as theta, but
			# each self.counts[s][t] stores the expected counts
			self.counts=dict()
			# a self.total_counts dictionary is instantiated. For each s it stores the total
			# expected counts
			self.total_counts=dict()
			for n in range(len(self.target_sents)):	# for each couple of paired sentences (they have the same index)
				for t in self.target_sents[n]:	# for each word in the target sentence
					Z=0		# the normalizing Z is initialized to 0
					for s in self.source_sents[n]:
						Z+=self.theta[s][t]		# Z of a t is the sum of all p(t|sx) for all x in the corresponding source sentence 
					for s in self.source_sents[n]:
						c=self.theta[s][t]/Z	# number of expected counts of the alignment t-s is p(t|s)/Z 
						if s not in self.counts.keys():
							self.counts[s]=dict()
						if t not in self.counts[s].keys():
							self.counts[s][t]=c
						else:
							self.counts[s][t]+=c
						if s not in self.total_counts.keys(): # total counts of s are initialized or increased
							self.total_counts[s]=c
						else:
							self.total_counts[s]+=c

			# the new probabilities are calculated and stored in theta
			for s in self.counts.keys():
				for t in self.counts[s]:
					self.theta[s][t]=self.counts[s][t]/self.total_counts[s]



	def most_probable_alignments(self,output_filename):
		self.alignments=[]
		with open(output_filename+'.txt','w') as o:		# output file is created
			for n in range(len(self.target_sents)):	# for each couple of paired sentences
				alignment=''	# the alignment is initialized to an empty string
				for i in range(len(self.target_sents[n])):	# for each word at position i in the target sentence,
					t=self.target_sents[n][i]				# the index of the word in the source sentence with the 
					best_prob=0								# highest alignment probability has to be found 
					best_j=0
					for j in range(len(self.source_sents[n])):
						s=self.source_sents[n][j]
						if self.theta[s][t]>best_prob:
							best_prob=self.theta[s][t]
							best_j=j  
					if best_j==0:	# if the best alignment is a NULL alignment, we don't write it to conform to the score-alignment format
						continue
					alignment+=str(i)+'-'+str(best_j-1)+' '	# we add the word alignment to the sentence alignment in the score-alignment format
					# note that in the gold file there is no NULL alignment and the words are indexed from 0, hence best_j-1 (because we added
					# the NULL alignment at position 0)
				o.write(alignment+'\n')	# the sentence alignments are written to the output file




if __name__ == '__main__':

	iterations=int(input('Enter number of iterations:'))
	# the path to the two corpora
	hansard_e='en600.468/aligner/data/hansards.e'
	hansard_f='en600.468/aligner/data/hansards.f'
	
	# if the files are not already in the path, they are downloaded
	if Path(hansard_e).is_file()==False and Path(hansard_f).is_file()==False:
		subprocess.Popen(["git", "clone", "https://github.com/alopez/en600.468.git"])

	# the sentences are stripped, split and appended to a list
	with open (hansard_f) as f:
		f_sents=[sentence.lower().strip().split() for sentence in f.readlines()]

	with open (hansard_e) as e:
		e_sents=[sentence.lower().strip().split() for sentence in e.readlines()]


	'''
	an IBM_Model1 is instantiated, with the english sentences as source sentences, 
	the french sentences as target, and the number of iterations of the model. 
	'''
	IBM_Model1=IBM_Model1(e_sents,f_sents,iterations)

	# the alignments are written to the specified output file
	alignments=IBM_Model1.most_probable_alignments('ibm_model1_alignments')

import os,re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
more_stopwords = ['film', 'sinopsis', 'pemeran']
stopwords = stopwords + more_stopwords

#Cleaning

def clean_doc(doc) :
    doc = re.sub('\.', ' ', doc)
    doc = re.sub('\(', ' ', doc)
    doc = re.sub('\)', ' ', doc)
    doc = re.sub(':', ' ', doc)
    doc = re.sub(',',' ', doc)
    doc = re.sub(r'\s+', ' ', doc)
    return doc

for root, dirs, files in os.walk(os.getcwd()+"/Korpus"):
    for input_file in files:
        output_file = 'tandabaca/' + input_file
        input_file = 'Korpus/' + input_file
        f = open(input_file,"r")
        f_new = open(output_file,"w")
        f_new.write(clean_doc(f.read()))
        f.close()
        f_new.close
        

documents = []
kata_unik = set()


#Case folding dan Stopword removal    
for root, dirs, files in os.walk(os.getcwd()+"/tandabaca"):
    for input_file in files:
        output_file = input_file
        input_file = 'tandabaca/'+input_file
        documents.append(output_file)
        f = open(input_file,"r")
        f_new = open("preprocessed/" + output_file,"w")
        for line in f.readlines():
            words = line.split()    
            for word in words:
                word = word.lower()
                if word.isalpha() == False:
                    continue
                if word not in stopwords:
                    f_new.write(word+" ")
                    kata_unik.add(word)
            f_new.write("\n")
        f.close()
        f_new.close()
        
doc_freq = dict()
term_freq = dict()
posting_list = dict()

#Inisialisasi matrix term_freq
for word in kata_unik:
    term_freq[word] = dict()
    for root, dirs, files in os.walk(os.getcwd()+"\preprocessed"):
        for input_file in files:
            term_freq[word][input_file] = 0
            
#Update nilai matrix term_freq
for root, dirs, files in os.walk(os.getcwd()+"\preprocessed"):
    for input_file in files:
        f_new = open("preprocessed/" + input_file, "r")
        for line in f_new.readlines():
            words = line.split()
            for word in words:
                word = word.lower()
                if word.isalpha() == False:
                    continue
                if word in kata_unik:
                    term_freq[word][input_file]+=1
        f_new.close()
        
#Update nilai doc_freq
for word in kata_unik:
    doc_freq[word] = 0
    posting_list[word] = []
    for input_file in term_freq[word].keys():
        if term_freq[word][input_file]>0:
            posting_list[word].append(input_file)
            doc_freq[word]+=1
            

import pickle
pickle.dump(posting_list,open("posting_list.dict", "wb"))
pickle.dump(documents, open("documents.dict", "wb"))


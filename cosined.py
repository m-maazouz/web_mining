from pprint import pprint
import gensim
from gensim import corpora,models,similarities
import pandas as pd


documents = ["new york times",
             "new york post",
             "los angles times"]

#query
query = "new new time"

tokens = [[token for token in doc.lower().split() ] for doc in documents]
print('1_: ***********************\n', tokens)

dict = corpora.Dictionary(tokens)
print('2_: ***********************\n',dict)
print('3_: ***********************\n',dict.num_docs)


print('4_: ***********************\n',dict.token2id)

print('5_: ***********************\n',dict[0],dict[1])

print('6_: ***********************\n')
# la methode : doc2bow(document,...)  kt7awel les word --> l' vector d les frequense des mots
corpus_doc2bow_vectors = [dict.doc2bow(tok_doc) for tok_doc in tokens]

for c in corpus_doc2bow_vectors:
    print (c)

print('7_: ***********************\n')


tfidf_model = models.TfidfModel(corpus_doc2bow_vectors, id2word=dict, normalize=False)
corpus_tfidf_vectors = tfidf_model[corpus_doc2bow_vectors]
print("\ntf-idf")
for doc_vector in corpus_tfidf_vectors:
    print(doc_vector)
    
print('8_: ***********************\n')
query = "new new times"
query_bow_vector = dict.doc2bow(query.lower().split())
print(query_bow_vector)

print('9_: ***********************\n')
# Calculate (compute) TF-IDF vector of the query
query_tfidf_vector = tfidf_model[query_bow_vector]
print(query_tfidf_vector)

#create a bow vectore for a new document 
query_bow_vector = dict.doc2bow(query.lower().split())
print('query vector : 10_: ***********************\n')
pprint(query_bow_vector)

#calculate TF-IDF vectore of query
query_tfidf_vector = tfidf_model[query_bow_vector]
print('query tfidf : 11_: ***********************\n')
pprint(query_tfidf_vector)

#compute the similarity betwen the query and the documents
index_matrix = similarities.SparseMatrixSimilarity(corpus_tfidf_vectors,num_features=6)

#calculate the similarity of our query vector against every document
sims = index_matrix[query_tfidf_vector]
list = list(enumerate(sims))
print('similarity : 12_: ***********************\n')
pprint(list)
print('similarity : 13_: ***********************\n')
for i,q in enumerate(sims) :
    print(("document "),i,'cosined : ',q)
print('similarity : 14_: ***********************\n')
d = {'documents' : [documents[i] for i,_ in enumerate(sims)] , 'query' : [query for i in range(len(sims))],'cosined' : [q for _,q in enumerate(sims)]}
df = pd.DataFrame(d)
pprint(df)

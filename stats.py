
import json
from pymongo import MongoClient
import pymongo

import collections


client = MongoClient('mongodb://localhost:27017/') # conecta num cliente do MongoDB rodando na sua máquina
db = client['imdb'] # acessa o banco de dados
collection = db['imdb_oficial'] # acessa a minha coleção dentro desse banco de dados
stats_collection = db['stats'] # coleção de stats
stats_1 = db['stats_prob_cond1'] 
stats_2 = db['stats_prob_cond2'] 

print("sucesso")

# pipeline do somatório ds gêneros dos filmes
soma = collection.aggregate([
   {
     '$group': {
       '_id': '$gender',
       'total':{'$sum': 1}
    }
   }
])

# pipeline da média das avaliações dos filmes
medianIMDB = collection.aggregate([
   {
     '$group': {
       '_id': None, 
       'avgIMDB':{'$avg': '$imdb'}
    }
   }
])
meIMDB = list(medianIMDB)
meIMDB = meIMDB[0]['avgIMDB']

# pipeline da média da duraçã dos filmes
medianDuration = collection.aggregate([
   {
     '$group': {
       '_id': None,
       'avgDURATION':{'$avg': '$duration'}
    }
   }
])

meDuration = list(medianDuration)
meDuration = meDuration[0]['avgDURATION']

# Desvio padrão dos filmes por nome
resSTD =  collection.aggregate([
   { '$group': {'_id': '$name', 'stdDev': { '$stdDevPop': "$imdb" } } }
])


# total filmes
totalFilme = collection.aggregate([{
    '$group': {
       '_id': None,
       'total':{'$sum': 1}    # Cada gender com seu count
       }
}
])
tott =list(totalFilme) # total de filmes na colection


#print(tott)
# filmes com avaliação > 8
maiorfilme = collection.count_documents({ 'imdb': { '$gt': 8 } }) # == 730 /5000  = 0.146
# prob de um filme ser maior do que 8
probFilmeGT8 = maiorfilme/ tott[0]['total'] 
#print(probFilmeGT8)

# Prob. condicional. Filmes de um gênero X com avaliação maior do que 8 dado que a avaliação do filme é maior 8 
probIMDB = collection.aggregate([
   {
      '$match': {
        'imdb': {
          '$gt': 8
        }
      }
    },
   {
    '$group': {
       '_id': '$gender',
       'total':{'$sum': 1}    # Cada gender com seu count
       },
    },
    {
    '$project': { 
            'probImdb': { '$divide': [ '$total', tott[0]['total'] ] } }  # cada gender com sua prob
    },
   {
    '$project': { 
            'probCond': { '$divide': [ '$probImdb', probFilmeGT8 ] } }  # cada gender com sua prob
    }
])


probFilme_pc =list(probIMDB)  
# Inserindo na collection a prob. de um filme ser escolhido ter avaliação maior do que 8

def insert_prob_cond_filme():
   for i in range(len(probFilme_pc)):
      stats_1.insert(probFilme_pc[i])
      print((probFilme_pc[i] ))

# insert_prob_cond_filme()


#  p(A/B) = P(A AND B) / P(B)

# Prob. condicional. Um determinado filme ter avaliação maior do que 8. 
probIMDB_2 = collection.aggregate([
   {
    '$group': {
       '_id': '$gender',
       'total':{'$sum': 1}    # Cada gender com seu count
       },
    },
    {
    '$project': { 
            'probImdb': { '$divide': [ '$total', tott[0]['total'] ] } }  # cada gender com sua prob
    },
   {
    '$project': { 
            'probCond': { '$divide': [ '$probImdb', probFilmeGT8 ] } } 
    }
])

probFilme_ =list(probIMDB_2) 
# prob. de um filme ser escolhido ter avaliação maior do que 8 dado que um filme tem avaliaçaõ >8
def insert_prob_filme():
   for i in range(len(probFilme_)):
      stats_2.insert(probFilme_[i])
      print((probFilme_[i] ))

# insert_prob_filme()

# dado um filme ser > gender
probFilme = collection.aggregate([{
    '$group': {
       '_id': '$gender',
       'total':{'$sum': 1}    # Cada gender com seu count
       }
    },
    {
    '$project': { 
            'probGender': { '$divide': [ '$total', tott[0]['total']  ] } }  # cada gender com sua prob
    }
])

# diretores distintos
totalDiretor =  collection.aggregate([
    {'$group': {'_id': '$diretor'}},
    {'$group': {'_id': '$diretor', 'count': {'$sum': 1}}}
])

# Total de count por diretores
countDiretor =  collection.aggregate([
    {'$group': {'_id': '$diretor', 'count': {'$sum': 1}}},
    { '$sort': { 'count': -1 } },
])

totalDirtinctDir =list(totalDiretor) # total de filmes na colection
totalDirtinctDir = totalDirtinctDir[0]['count']
# print(totalDistinctDir)

totalDir =list(countDiretor)  # lista os diretores em ordem decrescente 

# Inserindo na collection os diretores
def insert_diretores_fav():
   for i in range(len(totalDir)):
      stats_collection.insert(totalDir[i])
      print((totalDir[i] ))

# insert_diretores_fav()

# maiorfilme = collection.count_documents({ 'imdb': { '$gt': 8 } }) # == 730 /5000  = 0.146


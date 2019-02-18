
from flask.json import JSONEncoder
import os
from flask import Flask, jsonify, redirect, url_for, send_from_directory
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient

#------------------------------------------#

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/imdb"
mongo = PyMongo(app)

client =  MongoClient('mongodb://localhost:27017/') 
db = client.imdb.movies_imdb_oficial 
posts = client.imdb.movies_imdb_oficial #.mv[0] 

@app.route('/movie', methods=['POST'])
def hello_world():
    posts.insert_one({'name' : "Cris", 'year' :"2019", 'duration' : 123, 'imdb' : 7, 'votes' : 1234, 'gender' : "Action"  })
    return jsonify("Deu certo")

@app.route('/movie/', methods=['GET'])
def get_all_frameworks():
    framework = client.imdb.movies_imdb_oficial 
    output = []
    for q in framework.find():
        output.append(  {'name' : q['name'], 'year' : q['year'], 'duration' : q['duration'], 'imdb' : q['imdb'], 'votes' : q['votes'], 'gender' : q['gender']  })
    return jsonify({'film' : output})

@app.route('/movie/<name>', methods=['GET'])
def get_one_framework(name):
    framework = client.imdb.movies_imdb_oficial

    q = framework.find_one({'name' : name})
    if q:
        output = {'name' : q['name'], 'year' : q['year'], 'duration' : q['duration'], 'imdb' : q['imdb'], 'votes' : q['votes'], 'gender' : q['gender']  }
    else:
        output = 'No results found'

    return jsonify({'film' : output})

@app.route('/movie/stats', methods=['GET'])
def get_stats():
    collection = client.imdb.movies_imdb_oficial 
    output = []
    for q in collection.find():
        output.append(  {'name' : q['name'], 'year' : q['year'], 'duration' : q['duration'], 'imdb' : q['imdb'], 'votes' : q['votes'], 'gender' : q['gender']  })
  
    # pipeline da média das avaliações dos filmes
    medianIMDB = collection.aggregate([
    {
        '$group': {
        '_id': None, 
        'avgIMDB':{'$avg': '$imdb'}
        }
    }
    ])
    # pipeline da média da duraçã dos filmes
    medianDuration = collection.aggregate([
    {
        '$group': {
        '_id': None,
        'avgDURATION':{'$avg': '$duration'}
        }
    }
    ])

    # total filmes
    totalFilme = collection.aggregate([{
        '$group': {
        '_id': None,
        'total':{'$sum': 1}    # Cada gender com seu count
        }
    }
    ])
  
    return jsonify({'Media IMDB' : list(medianIMDB)}, {'Media Duration' : list(medianDuration)}, {'Total Filmes' : list(totalFilme)} )


# Diretores que fizeram mais filmes feitos
@app.route('/movie/stats_diretor', methods=['GET'])
def get_stats_diretor():
    collection = client.imdb.stats
    output = []
    for q in collection.find():
        output.append(  {'_id' : q['_id'], 'count' : q['count']  })
    return jsonify({'film' : output})



# prob. de um filme ser escolhido ter avaliação maior do que 8 dado que um filme tem avaliaçaõ >8
@app.route('/movie/stats_prob1', methods=['GET'])
def get_stats_prob1():
    collection = client.imdb.stats_prob_cond1
    output = []
    for q in collection.find():
        output.append(  {'_id' : q['_id'], 'probCond' : q['probCond']  })
    return jsonify({'film' : output})

# Inserindo na collection a prob. de um filme ser escolhido ter avaliação maior do que 8
@app.route('/movie/stats_prob2', methods=['GET'])
def get_stats_prob2():
    collection = client.imdb.stats_prob_cond2
    output = []
    for q in collection.find():
        output.append(  {'_id' : q['_id'], 'probCond' : q['probCond']  })
    return jsonify({'film' : output})


#    P(A|B) = P(A) x P(B|A) /  P(B) Teorema de Bayes. 
#    P(A|B) = P(A∩B) / P(B) Probabilidade Condicional.
'''
Sendo P(A) a probabilidade do evento A, P(B) a probabilidade do evento B
 e P(A,B) a probabilidade de ocorrerem os eventos A e B:
P(A,B) = P(A) × P(B)
'''


#------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
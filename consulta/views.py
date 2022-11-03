from types import NoneType
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests as req
from googletrans import Translator

# from pokemontcgsdk import RestClient, Card
# API Cartas Pokemon
# RestClient.configure('4ed58568-348b-49ea-945f-d430e5d5e49e')
# carta = Card.where(q='name:blissey')[0]
# print(carta.images)

# nome = 'calyrex'
#     try:
#         pokedex = req.get(f'https://pokeapi.co/api/v2/pokemon/{nome}')
#         pokedex = pokedex.json()
#         pokedex2 = pokedex['sprites']['other']['official-artwork']['front_default']
#         pokedex1 = pokedex['sprites']['other']['dream_world']['front_default']
#         if type(pokedex1) == NoneType:
#             print(pokedex2)
#             return  render(request, 'index.html', {'pokedex': pokedex2}) 
#         else:
#             print(pokedex1)
#             return  render(request, 'index.html', {'pokedex': pokedex1})   
#     except:
#         return  render(request, 'index.html')  

trans = Translator() 

def calc_altura(altura):
    if '"' in altura:
        altura = str(altura).replace('"', '').split("'")
        altura = round((int(altura[0])/3.281) + (int(altura[1])/39.37), 1)    
    else:
        altura = str(altura).replace("'", '')
        altura = round((int(altura[0])/3.281), 1)
    return altura

def traduzir_descricao(descricao):
    if descricao == '-':
        descricao_traduzido = 'Sem informações sobre esse Pokémon'
        return descricao_traduzido
    else:
        descricao_traduzido = trans.translate(descricao, dest='pt').text
        return descricao_traduzido
    
def traduzir_tipo(tipos):
    traduzir = ''
    tipo_traduzido = ''
    for tipo in tipos:
        if tipo == 'Electric':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Elétrico'  
        elif tipo == 'Psychic':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Psíquico'
        elif tipo =='Dark':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Escuridão'
        elif tipo == 'Bug':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Inseto'
        elif tipo == 'Fighting':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Lutador'
        elif tipo == 'Fire':
            tipo_traduzido = f'{tipo_traduzido}' + ' ' +'Fogo'
        else:
            traduzir = trans.translate(tipo, dest='pt').text  
            tipo_traduzido = f'{tipo_traduzido}' + ' ' + f'{traduzir}'
    return (tipo_traduzido)

def traduzir_especie(especie):
    especie_traduzido = ''
    if especie == 'Cocoon':
        especie_traduzido = 'Casulo'
    elif especie == 'Painter':
        especie_traduzido = 'Pintor'
    elif especie == 'Wolf':
        especie_traduzido = 'Lobo'
    elif especie == 'Puppy':
        especie_traduzido = 'Cachorro' 
    elif especie == 'Genetic':
        especie_traduzido = 'Genético' 
    elif especie == 'Tender':
        especie_traduzido = 'Místico'
    elif especie == 'Seafaring':
        especie_traduzido = 'Fada do Mar'
    elif especie == 'Duck':
        especie_traduzido = 'Pato'
    elif especie == 'Paleozoic':
        especie_traduzido = 'Paleozóico'    
    elif especie =='Kitten':
        especie_traduzido = 'Gato'
    elif especie == 'Magnet':
        especie_traduzido = 'Magnético'
    else: 
        especie_traduzido = trans.translate(especie, dest='pt').text
    return especie_traduzido
    
def pesquisa_pokedex(request):
    nome = request.GET.get('nome_pokemon')
    status = []
    try:
        pokedex = req.get(f'https://pokeapi.co/api/v2/pokemon/{nome}')
        pokedex = pokedex.json()
        id = pokedex['id']
        info = req.get(f'https://pokeapi.glitch.me/v1/pokemon/{id}/')
        info = info.json()
        for i in range(6):
            stat = pokedex['stats'][i]['base_stat']
            status.append(stat)
        altura = info[0]['height']  
        especie = info[0]['species']
        tipos = info[0]['types']
        descricao = info[0]['description']
        shiny = pokedex['sprites']['front_shiny']
        peso = pokedex['weight']
        peso = str(peso)[:-1]   
        evolucoes = info[0]['family']['evolutionLine']
        altura = calc_altura(altura)
        descricao_traduzido = traduzir_descricao(descricao)
        tipo_traduzido = traduzir_tipo(tipos) 
        especie_traduzido = traduzir_especie(especie) 
        imagem2 = pokedex['sprites']['other']['official-artwork']['front_default']
        imagem1 = pokedex['sprites']['other']['dream_world']['front_default']
        nome = str(pokedex['name'])
        nome = nome.capitalize
        if type(imagem1) == NoneType:
            return  render(request, 'index.html', {'imagem': imagem2,
                                                   'pokemon_nome': nome,
                                                   'descricao': descricao_traduzido,
                                                   'tipo': tipo_traduzido,
                                                   'especie': especie_traduzido,
                                                   'altura': altura,
                                                   'id': id,
                                                   'shiny': shiny,
                                                   'status': status,
                                                   'peso': peso,
                                                   'evolucoes': evolucoes})
        else:
            return  render(request, 'index.html', {'imagem': imagem1,
                                                   'pokemon_nome': nome,
                                                   'descricao': descricao_traduzido,
                                                   'tipo': tipo_traduzido,
                                                   'especie': especie_traduzido,
                                                   'altura': altura,
                                                   'id': id,
                                                   'shiny': shiny,
                                                   'status': status,
                                                   'peso': peso,
                                                   'evolucoes': evolucoes})       
    except:
        return  render(request, 'index.html')       
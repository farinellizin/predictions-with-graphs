# from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import webScraping
import networkx as nx
import matplotlib.pyplot as plt

def Menu():
    print('\n\n\t\t   ~ Selecione os times desejados ~\n\n')
    print('\t\t1 - Palmeiras \t\t11 - Fortaleza\n\t\t2 - Internacional\t12 - Santos')
    print('\t\t3 - Fluminense \t\t13 - Goiás\n\t\t4 - Corinthians\t\t14 - Bragantino')
    print('\t\t5 - Flamengo \t\t15 - Coritiba\n\t\t6 - Atlético-PR\t\t16 - Cuiabá')
    print('\t\t7 - Atlético-MG \t17 - Ceará\n\t\t8 - América-MG\t\t18 - Atlético-GO')
    print('\t\t9 - São Paulo \t\t19 - Avaí\n\t\t10 - Botafogo\t\t20 - Juventude')

    team1 = 0
    team2 = 0

    while team1 < 1 or team1 > 20:
        team1 = int(input('\n\n\tInforme o número do primeiro time: '))
    
    while team2 < 1 or team2 > 20:
        team2 = int(input('\tInforme o número do segundo time: '))

    return team1, team2

team_codes = {1: 'palmeiras', 2: 'internacional', 3: 'fluminense', 4: 'corinthians' , 5: 'flamengo', 6: 'atletico_pr', 7: 'atletico_mg', 8: 'america_MG', 9: 'sao_paulo',
10: 'botafogo', 11: 'fortaleza', 12: 'santos', 13: 'goias', 14: 'bragantino', 15: 'coritiba', 16: 'cuiaba', 17: 'ceara', 18: 'atletico_go', 19: 'avai', 20: 'juventude'}

team_output_names = {1: 'Palmeiras', 2: 'Internacional', 3: 'Fluminense', 4: 'Corinthians' , 5: 'Flamengo', 6: 'Atlético-PR', 7: 'Atlético-MG', 8: 'América-MG', 9: 'São Paulo',
10: 'Botafogo', 11: 'Fortaleza', 12: 'Santos', 13: 'Goiás', 14: 'Bragantino', 15: 'Coritiba', 16: 'Cuiabá', 17: 'Ceará', 18: 'Atlético-GO', 19: 'Avaí', 20: 'Juventude'}

graph_names = ['palmeiras', 'internacional', 'fluminense', 'corinthians', 'flamengo', 'atletico_pr', 'atletico_mg',
'america_MG', 'sao_paulo', 'botafogo', 'fortaleza', 'santos', 'goias', 'bragantino', 'coritiba', 'cuiaba', 'ceara', 
'atletico_go', 'avai', 'juventude']

print('\n\n\t\t\t~ Aguarde... Inicializando programa ~\n\n')
average_position = {}

for i in graph_names:
    x = webScraping.webScraping_position(i)
    average_position[i] = x

graph = nx.DiGraph()
graph.add_nodes_from(graph_names)

for i in range(len(graph_names)-1, 0, -1):
    for j in range(i):
        if (average_position[graph_names[i]] < average_position[graph_names[j]]):
            graph.add_edge(graph_names[i], graph_names[j])
        else:
            graph.add_edge(graph_names[j], graph_names[i])

while True:
    t1, t2 = Menu()

    namewinner1 = team_output_names[t1]
    namewinner2 = team_output_names[t2]

    t1 = team_codes[t1]
    t2 = team_codes[t2]

    if graph.has_edge(t1, t2):
        print(f'\n\t\t~ Há maior chances de vitória para o {namewinner1} ~\n\n\n')
    else:
        print(f'\n\t\t~ Há maior chances de vitória para o {namewinner2} ~\n\n\n')

# print(graph.edges())        
# pos = nx.spring_layout(graph)
# nx.draw_networkx_nodes(graph, pos, node_size=500)
# nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='black')
# nx.draw_networkx_labels(graph, pos)
# plt.show()
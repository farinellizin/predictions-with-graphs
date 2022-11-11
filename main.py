import webScraping
import networkx as nx

team_names = ["palmeiras", "internacional", "fluminense", "corinthians", "flamengo", "atletico_pr", "atletico_mg",
"america_MG", "sao_paulo", "botafogo", "fortaleza", "santos", "goias", "bragantino", "coritiba", "cuiaba", "ceara", 
"atletico_go", "avai", "juventude"]

# média posições

average_position = {}

# palmeiras': '1023', 'internacional': '6600', 'fluminense': '2462', 'corinthians': '199', 'flamengo': '614', 'atletico_pr': '679', 'atletico_mg': '330', 
# 	'america_MG': '2863', 'sao_paulo': '585', 'botafogo': '537','fortaleza': '10870', 'santos': '221', 'goias': '3197', 'bragantino': '8793', 'coritiba': '776', 
# 	'cuiaba': '28022', 'ceara': '2029', 'atletico_go': '15172', 'avai': '2035', 'juventude': '10492'}

for i in team_names:
    x = webScraping.webScraping_position(i)
    print(f'TIME: {i} // MÉDIA: {x}')
    average_position[i] = x


graph = nx.DiGraph()
graph.add_nodes_from(team_names)

graph_names = ['palmeiras', 'internacional', 'fluminense', 'corinthians', 'flamengo', 'atletico_pr', 'atletico_mg',
'america_MG', 'sao_paulo', 'botafogo', 'fortaleza', 'santos', 'goias', 'bragantino', 'coritiba', 'cuiaba', 'ceara', 
'atletico_go', 'avai', 'juventude']

for i in range(len(graph_names)-1, 0, -1):
    print(i)
    for j in range(i):
        if (average_position[graph_names[i]] < average_position[graph_names[j]]):
            print(f'Posição I: {average_position[graph_names[i]]} // Posição J: {average_position[graph_names[j]]} // ENTROU IF')
            winner = [{graph_names[i], graph_names[j]}]
        else:
            print(f'Posição I: {average_position[graph_names[i]]} // Posição J: {average_position[graph_names[j]]} // ENTROU ELSE')
            # print('entrou else')
            winner = [{graph_names[j], graph_names[i]}]

        graph.add_edges_from(winner)

print(graph.edges)
        

        
        




# # E = [{'palmeiras', 'avai'}]

# # string1 = 'palmeiras'
# # string2 = 'galao da massa'

# # E = [{string1, string2}]

# G = nx.DiGraph()
# G.add_nodes_from(graph_names)
# G.add_edges_from(E)

# print(G.nodes)
# print("\n\n\n")
# print(G.edges)
# nx.draw(G, with_labels=True, node_size = 1000, node_color='b', edge_color='w', arrowsize=125)


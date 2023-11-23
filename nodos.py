from graphviz import Digraph
from OtaCopilotProject.algorithms.bfs import G_nx
import os

dot = Digraph(comment='Grafo de Animes y Usuarios')

# os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
os.environ["PATH"] += os.pathsep + 'C:\\Archivos de programa\\Graphviz\\bin'

for node, data in G_nx.nodes(data=True):
    if data.get("tipo") == "usuario":
        dot.node(str(node), data["nombre_perfil"], color='green', fontcolor='white', style='filled', fillcolor='green')
    elif data.get("tipo") == "anime":
        dot.node(str(node), data["title"], color='red', fontcolor='white', style='filled', fillcolor='red')

for u, v, data in G_nx.edges(data=True):
    if G_nx.nodes[u].get("tipo") == "usuario" and G_nx.nodes[v].get("tipo") == "anime":
        dot.edge(str(u), str(v))
        dot.edge(str(v), str(u))

dot.render('grafo_animes_usuarios', format='svg', view=True)

dot.attr('graph', dpi='1000', engine='dot')

dot.attr(size='100,100')
dot.attr('graph', rankdir='LR')

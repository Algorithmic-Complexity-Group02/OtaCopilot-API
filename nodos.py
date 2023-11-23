from graphviz import Digraph
from OtaCopilotProject.algorithms.bfs import G_nx  # Ajusta la ruta según la estructura de tu proyecto
import os

# Crear un grafo dirigido con Graphviz
dot = Digraph(comment='Grafo de Animes y Usuarios')

# Establecer la ruta al ejecutable de Graphviz
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

# Agregar nodos y aristas al grafo de Graphviz
for node, data in G_nx.nodes(data=True):
    if data.get("tipo") == "usuario":
        dot.node(str(node), data["nombre_perfil"], color='green', fontcolor='white', style='filled', fillcolor='green')
    elif data.get("tipo") == "anime":
        dot.node(str(node), data["title"], color='red', fontcolor='white', style='filled', fillcolor='red')

for u, v, data in G_nx.edges(data=True):
    dot.edge(str(u), str(v))

# Configurar el formato de salida a SVG
dot.render('grafo_animes_usuarios', format='svg', view=True)

# Configurar la resolución
dot.attr('graph', dpi='1000')

# Configurar el tamaño y la orientación
dot.attr(size='10,10')  # Ajusta el tamaño del área de dibujo del gráfico
dot.attr('graph', rankdir='LR')

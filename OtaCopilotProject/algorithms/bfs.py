import pandas as pd
import networkx as nx
from collections import deque
from .ufds import DSU


import numpy as np

#TERRIBLE

urlProfileTest = "./OtaCopilotProject/static/profileTest.csv"
urlAnimeTest = "./OtaCopilotProject/static/animeTest.csv"

def create_graph(df_animes, df_usuarios):
    nodos = {}
    bordes = []

    for _, row in df_animes.iterrows():
        anime_uid = row["uid"]
        nodos[anime_uid] = {"tipo": "anime", "data": row, "title": row["title"]}

    for _, row in df_usuarios.iterrows():
        user_profile = row["profile"]
        nodos[user_profile] = {"tipo": "usuario", "data": row, "nombre_perfil": user_profile}

        favorite_animes_str = row["favorites_anime"]
        favorite_animes = [anime_id.strip(" '[]") for anime_id in favorite_animes_str.split(',')]

        for anime_uid in favorite_animes:
            if anime_uid:
                try:
                    anime_uid = int(anime_uid)
                    bordes.append((user_profile, anime_uid, {"tipo_interaccion": "favorito"}))
                except ValueError as e:
                    print(f"Error al convertir a entero el valor '{anime_uid}' para el usuario {user_profile}: {e}")

    G = {"nodos": nodos, "bordes": bordes}
    G_nx = nx.DiGraph()

    node_id_mapping = {}
    current_id = 1

    for node, data in G["nodos"].items():
        if isinstance(node, (int, np.integer)):
            node_id_mapping[node] = node
        else:
            node_id_mapping[node] = current_id
            current_id += 1

    G_nx.add_nodes_from((node_id_mapping[node], data) for node, data in G["nodos"].items())

    #  UFDS
    ufds = DSU(map(str, node_id_mapping.keys()))
    for u, v, data in G["bordes"]:
        if ufds.union(str(u), str(v)):
            G_nx.add_edge(node_id_mapping[u], node_id_mapping[v], **data)
            G_nx.add_edge(node_id_mapping[v], node_id_mapping[u], **data)

    return G_nx, node_id_mapping


df_animes = pd.read_csv(urlAnimeTest, nrows=1500)
print(df_animes.columns)

df_usuarios = pd.read_csv(urlProfileTest, nrows=1500)

G_nx, node_id_mapping = create_graph(df_animes, df_usuarios)

def get_anime_uid(anime_title, graph, node_id_mapping):
    for node, data in graph.nodes(data=True):
        if data.get("tipo") == "anime" and data.get("title", "").lower() == anime_title.lower():
            return node_id_mapping[node]
    return None

def recommend_animes_bfs(graph, source_anime_title, node_id_mapping):
    source_anime_uid = get_anime_uid(source_anime_title, graph, node_id_mapping)

    if source_anime_uid is None:
        print(f"No se encontró el anime con el título '{source_anime_title}' en el grafo.")
        return [], []

    queue = deque([(source_anime_uid, 0)])
    visited = set([source_anime_uid])
    recommended_animes = []


    while queue:
        node, distance = queue.popleft()

        if node not in node_id_mapping:
            continue

        successors = list(G_nx.successors(node_id_mapping[node]))
        if not successors:
            continue

        for neighbor in successors:

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

                node_data = G_nx.nodes[neighbor]

                if "tipo" in node_data:
                    if node_data["tipo"] == "usuario":
                        # Expandir a los animes favoritos de este usuario
                        favorites_animes = list(G_nx.successors(neighbor))
                        for anime_node in favorites_animes:
                            if anime_node not in visited:
                                visited.add(anime_node)
                                queue.append((anime_node, distance + 1))
                               # recommended_animes.append((anime_node, distance + 1))

                    elif node_data["tipo"] == "anime":
                        recommended_animes.append((neighbor, distance + 1))
                else:
                    print(f"Atributo 'tipo' no encontrado para el nodo {neighbor}")
    recommended_animes.sort(key=lambda x: x[1])
    return recommended_animes

def get_recommended_animes(anime_title):
    recommended_animes = recommend_animes_bfs(G_nx, anime_title, node_id_mapping)
    print_animes(anime_title, recommended_animes)
    return recommended_animes

def handle_float_values(data):
    for key, value in data.items():
        if isinstance(value, float):
            if value == float('inf') or value == float('-inf') or value != value:
                data[key] = None  # Reemplazar infinitos y NaN por None
    return data

def print_animes(title, recommended_animes):
    print(f"Animes recomendados para '{title}':")
    for anime_uid, distance in recommended_animes:
        anime_data = G_nx.nodes[anime_uid]['data']
        print(f"Anime: {anime_data}, Distancia: {distance}")


# source_anime_title = "Haikyuu!! Second Season"
# recommended_animes = get_recommended_animes(source_anime_title)

# '''print(f"Animes recomendados para '{source_anime_title}':")
# for anime_uid, distance in recommended_animes:
#     anime_data = G_nx.nodes[anime_uid]['data']
#     print(f"Anime: {anime_data}, Distancia: {distance}")'''
    
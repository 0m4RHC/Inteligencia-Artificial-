import matplotlib.pyplot as plt
import osmnx as ox
from src.utils import cargar_grafo, gen_nodo_entrega

# Cargar el grafo guardado
ruta_grafo = "data/cdmx_norte_centro.graphml"
print(f"Cargando grafo desde '{ruta_grafo}'...")
G = cargar_grafo(ruta_grafo)

# Generar el almacén y las entregas aleatorias
nodo_almacen, nodos_entrega = gen_nodo_entrega(G, rango_entregas=(6, 10))
print(f"Almacén central: {nodo_almacen}")
print(f"Puntos de entrega ({len(nodos_entrega)}): {nodos_entrega}")

# Límites de las alcaldías para dibujar las fronteras
alcaldias = [
    {"county": "Cuauhtémoc", "state": "Ciudad de México", "country": "Mexico"},
    {"county": "Benito Juárez", "state": "Ciudad de México", "country": "Mexico"},
    {"county": "Coyoacán", "state": "Ciudad de México", "country": "Mexico"},
]
gdf_limites = ox.geocode_to_gdf(alcaldias)

print("\nGenerando mapa con almacén y entregas...")

# Trazar la red vial base
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_linewidth=0.3,
    edge_color="#555555",  # Calles en gris
    bgcolor="#111111",     # Fondo oscuro
    show=False,
    close=False,
)

#+ Dibujar las fronteras de las alcaldías
colores_fronteras = ["#00FFFF", "#FF00FF", "#FFFF00"]  # Cuauhtémoc, BJ, Coyoacán
for i in range(len(gdf_limites)):
    alcaldia = gdf_limites.iloc[[i]].copy()
    if i == 0:
        geometria = alcaldia.geometry.iloc[0]
        if geometria.geom_type == "MultiPolygon":
            partes = list(geometria.geoms)
            parte_principal = max(partes, key=lambda p: p.area)
            alcaldia.geometry = [parte_principal]

    alcaldia.boundary.plot(
        ax=ax,
        color=colores_fronteras[i],
        linewidth=1.8,
        linestyle="--",
        zorder=3,
    )

# Dibujar el Almacén 
x_alm = G.nodes[nodo_almacen]["x"]
y_alm = G.nodes[nodo_almacen]["y"]
ax.scatter(
    x_alm,
    y_alm,
    c="#FF3333",         
    s=180,               
    marker="*",          
    edgecolors="white",
    linewidths=1.2,
    zorder=10,
    label="Almacén Central (Xoco)",
)

# Dibujar los Nodos de Entrega
x_ent = [G.nodes[n]["x"] for n in nodos_entrega]
y_ent = [G.nodes[n]["y"] for n in nodos_entrega]
ax.scatter(
    x_ent,
    y_ent,
    c="#00FF66",          
    s=55,                 # Tamaño de punto
    marker="o",
    edgecolors="black",
    linewidths=0.8,
    zorder=9,
    label=f"Puntos de Entrega ({len(nodos_entrega)})",
)

# Agregar leyenda y guardar
ax.legend(
    loc="upper left",
    facecolor="#222222",
    edgecolor="#555555",
    labelcolor="white",
    fontsize=9,
)

nombre_salida = "mapa_almacen_entregas.png"
fig.savefig(
    nombre_salida,
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor(),
)
plt.close(fig)

print(f"¡Listo! Imagen generada exitosamente como '{nombre_salida}'.")
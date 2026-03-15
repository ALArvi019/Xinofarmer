import copy

dungeon_imagesRDO = {
    "kikuras": (
        [{"path": 1}],
        [{"path": 4}],
        [{"path": 6}],
    )
}

# Hacer una copia profunda del diccionario
copied_dict_deep = copy.deepcopy(dungeon_imagesRDO)

# Convierte la tupla a una lista para poder modificarla
copied_list = list(copied_dict_deep["kikuras"])

# Elimina el elemento en la posición 1 (segundo elemento)
del copied_list[1]

# Convierte la lista de nuevo a tupla
copied_dict_deep["kikuras"] = tuple(copied_list)



# Verifica el cambio
print("Original:")
print(dungeon_imagesRDO)

print('-------------------')

print("Copia con elemento eliminado:")
print(copied_dict_deep)

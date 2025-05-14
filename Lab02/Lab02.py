import json

# Rutas de entrada y salida
entry_route = r'C:\Users\axelg\Desktop\EDI\Proyecto2EDI\Lab02\input.jsonl'
exit_route = r'C:\Users\axelg\Desktop\EDI\Proyecto2EDI\Lab02\output.jsonl'

# Función para leer archivos JSONL
def leer_jsonl(entry_route):
    with open(entry_route, 'r') as file:
        return [json.loads(linea) for linea in file if linea.strip()]

#Esta es la funcion para filtrar construcciones segun los requisitos
def construction_filter(zone_info, requirements):
    av_svs = set()
    av_constructions = {}

    #Aqui se extraen los servicios y construcciones que estan disponibles
    for zone in zone_info:
        av_svs.update(
            service for service, available in zone.get("services", {}).items() if available
        )

        for type, list in zone.get("builds", {}).items():
            if type not in av_constructions:
                av_constructions[type] = []
            av_constructions[type].extend(list)

    construction_type = requirements.get("typeBuilder", "")
    budget = requirements.get("budget", float("inf"))
    min_danger = requirements.get("minDanger", None)
    pet_friendly = requirements.get("wannaPetFriendly", None)
    comercial_activity = requirements.get("commercialActivity", None)

    #Aqui se devuelve un arreglo vacio si no hay construcciones disponibles
    if construction_type not in av_constructions:
        return []
    #Aqui se filtran las construcciones segun los requisitos
    filtered_list = []
    for construccion in av_constructions[construction_type]:
        if construccion.get("price", float("inf")) > budget:
            continue #El "continue" se usa para saltar a la siguiente iteracion del ciclo

        if construction_type == "Houses" and min_danger:
            danger_lvls = {"Red": 0, "Orange": 1, "Yellow": 2, "Green": 3}
            if danger_lvls.get(construccion.get("zoneDangerous"), -1) > danger_lvls.get(min_danger, -1):
                continue

        if construction_type == "Apartments" and pet_friendly is not None:
            if construccion.get("isPetFriendly") != pet_friendly:
                continue

        if construction_type == "Premises" and comercial_activity:
            if comercial_activity not in construccion.get("commercialActivities", []):
                continue
        
        #Aqui se agrega la construccion a la lista filtrada
        filtered_list.append((construccion["id"], construccion["price"]))
    #Aqui se ordena la lista filtrada y se devuelve un arreglo con los ids de las construcciones
    return [item[0] for item in sorted(filtered_list, key=lambda x: x[1])]

# Leer datos de entrada
data = leer_jsonl(entry_route)

# Generar resultados y escribir en el archivo de salida
with open(exit_route, 'w') as exit_file:
    for entry_route in data:
        results = construction_filter(entry_route["input1"], entry_route["input2"])
        exit_file.write(json.dumps(results) + "\n")
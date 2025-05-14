import json

entry_route = r'C:\Users\axelg\Desktop\EDI\Proyecto2EDI\Lab01\input.jsonl'
exit_route = r'C:\Users\axelg\Desktop\EDI\Proyecto2EDI\Lab01\Output.jsonl'

def find_recommendations(input1, input2):
    recommendations = []
    min_total_distance = float('inf')
    min_max_distance = float('inf')
    n = len(input1)

    for i in range(n):
        total_distance = 0
        max_distance = 0
        valid_apartment = True
        apartment = input1[i]
        #Aqui se analiza los requerimientos del input 2 en el input1 actual
        for requirement in input2:
            if not apartment.get(requirement, False):
                distance = find_distance(input1, i, requirement, n)
                #Aqui se verifica si el apartamento es valido
                if distance == -1:
                    valid_apartment = False
                    break
                
                total_distance += distance
                max_distance = max(max_distance, distance)
        #Si el apartamento es valido, se verifica si es mejor que los anteriores
        if valid_apartment:
            if (total_distance < min_total_distance or 
                (total_distance == min_total_distance and max_distance < min_max_distance)):
                min_total_distance = total_distance
                min_max_distance = max_distance
                recommendations = [i]  
            elif total_distance == min_total_distance and max_distance == min_max_distance:
                recommendations.append(i)  
    return recommendations

#Aqui es la funcion para encontrar la distancia en el input 1 actual para el requerimiento dado
def find_distance(input1, start_index, requirement, n):
    for i in range(1, n):
        if start_index + i < n and input1[start_index + i].get(requirement, False):
            return i

        if start_index - i >= 0 and input1[start_index - i].get(requirement, False):
            return i
    return -1  

with open(entry_route, 'r') as entry_file, open(exit_route, 'w') as exit_file:
    for line in entry_file:
        if line.strip():  

            data = json.loads(line) 
            input1 = data.get("input1", [])
            input2 = data.get("input2", [])
            best_apartments = find_recommendations(input1, input2)
            exit_file.write(json.dumps(best_apartments) + "\n")
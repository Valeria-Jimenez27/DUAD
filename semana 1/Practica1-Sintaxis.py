# Pedir cantidad de notas
cantidad_notas = int(input("Ingrese la cantidad total de notas: "))

# Inicializar variables
cantidad_de_aprobadas = 0
cantidad_desaprobadas = 0
promedio_de_aprobadas = 0
promedio_de_desaprobadas = 0
promedio_total = 0

# Contador para controlar las iteraciones
contador = 1

# Bucle para ingresar las notas
while contador <= cantidad_notas:
    nota = float(input(f"Ingrese la nota número {contador}: "))

    promedio_total += nota  # Sumar al promedio total

    if nota >= 70:
        cantidad_de_aprobadas += 1
        promedio_de_aprobadas += nota
    else:
        cantidad_desaprobadas += 1
        promedio_de_desaprobadas += nota

    contador += 1  # Incrementar contador

# Calcular promedios evitando división por cero
if cantidad_de_aprobadas > 0:
    promedio_de_aprobadas /= cantidad_de_aprobadas
else:
    promedio_de_aprobadas = 0

if cantidad_desaprobadas > 0:
    promedio_de_desaprobadas /= cantidad_desaprobadas
else:
    promedio_de_desaprobadas = 0

promedio_total /= cantidad_notas  # Promedio total

# Mostrar resultados
print(f"\nCantidad de notas aprobadas: {cantidad_de_aprobadas}")
print(f"Promedio de notas aprobadas: {promedio_de_aprobadas:.2f}")
print(f"Cantidad de notas desaprobadas: {cantidad_desaprobadas}")
print(f"Promedio de notas desaprobadas: {promedio_de_desaprobadas:.2f}")
print(f"Promedio total de todas las notas: {promedio_total:.2f}")



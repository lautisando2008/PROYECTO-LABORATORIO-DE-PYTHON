# ==========================================
# TRABAJO FINAL INTEGRADOR: SISTEMA DE CINE
# ==========================================

# --- VARIABLES GLOBALES / DATOS DE PRUEBA ---
# Simulamos una base de datos pequeña usando diccionarios y listas
PELICULAS = ["Avengers", "Batman", "Inception", "Inside Out"]
HORARIOS = ["14:00", "17:30", "20:00", "22:45"]
CAPACIDAD_SALAS = [40, 50, 35, 60]  # Capacidad máxima por sala/película
asientos_vendidos = [0, 0, 0, 0]    # Acumuladores de entradas por función

# Variables para Estadísticas (Contadores y Acumuladores)
total_entradas_vendidas = 0
recaudacion_total = 0.0
PRECIO_ENTRADA = 5000.0  # Precio base de la entrada


# --- MÓDULO DE VALIDACIONES ---
def validar_opcion_menu(opcion_str, min_val, max_val):
    """Valida que la opción ingresada sea un número entero dentro del rango válido."""
    try:
        opcion = int(opcion_str)
        if min_val <= opcion <= max_val:
            return True, opcion
        else:
            print(f"Error: Por favor, ingrese un número entre {min_val} y {max_val}.")
            return False, None
    except ValueError:
        print("Error crítico: El valor ingresado debe ser un número entero.")
        return False, None


def validar_cantidad_entradas(cantidad_str, capacidad_disponible):
    """Valida la cantidad de entradas solicitadas contra la disponibilidad de la sala."""
    try:
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            print("Error: La cantidad de entradas debe ser mayor a cero.")
            return False, None
        if cantidad > capacidad_disponible:
            print(f"Error de capacidad: Solo quedan {capacidad_disponible} asientos disponibles.")
            return False, None
        return True, cantidad
    except ValueError:
        print("Error: Ingrese un número válido para la cantidad de entradas.")
        return False, None


# --- MÓDULO DE LÓGICA DE NEGOCIO ---
def mostrar_cartelera():
    """Muestra de forma limpia las películas y horarios."""
    print("\n--- CARTELERA DISPONIBLE ---")
    for i in range(len(PELICULAS)):
        disponibles = CAPACIDAD_SALAS[i] - asientos_vendidos[i]
        print(f"{i + 1}. {PELICULAS[i]} | Horario: {HORARIOS[i]} | Asientos Libres: {disponibles}")


def calcular_importe(cantidad_entradas, codigo_promocion):
    """Calcula el monto final aplicando promociones si corresponden."""
    subtotal = cantidad_entradas * PRECIO_ENTRADA
    descuento = 0.0
    
    # Estructura condicional para validar código de promoción
    if codigo_promocion.upper() == "CINE20":
        descuento = subtotal * 0.20
        print("¡Promoción aplicada con éxito! Descuento del 20%.")
    elif codigo_promocion != "":
        print("Código de promoción inválido. Se aplicará la tarifa normal.")
        
    return subtotal - descuento


def realizar_reserva():
    """Maneja el flujo completo para registrar una reserva de entradas."""
    global total_entradas_vendidas, recaudacion_total
    
    mostrar_cartelera()
    
    # 1. Selección de Película
    es_valido = False
    while not es_valido:
        opcion_input = input("\nSeleccione el número de la película que desea ver: ")
        es_valido, indice_pelicula = validar_opcion_menu(opcion_input, 1, len(PELICULAS))
    
    indice_pelicula -= 1 # Ajustamos al índice de la lista (0-indexed)
    capacidad_disponible = CAPACIDAD_SALAS[indice_pelicula] - asientos_vendidos[indice_pelicula]
    
    # Control de capacidad previa
    if capacidad_disponible == 0:
        print("Lo sentimos, la sala para esta función está completamente llena.")
        return

    # 2. Cantidad de entradas
    es_valido = False
    while not es_valido:
        cant_input = input(f"¿Cuántas entradas desea reservar? (Disponibles: {capacidad_disponible}): ")
        es_valido, cantidad = validar_cantidad_entradas(cant_input, capacidad_disponible)
        
    # 3. Promociones
    print("\nCódigos disponibles de prueba: 'CINE20' o presione Enter para omitir.")
    codigo_promo = input("Ingrese un código de promoción si posee uno: ")
    
    # 4. Cálculo de Importe
    total_pago = calcular_importe(cantidad, codigo_promo)
    print(f"\nResumen de la Operación:")
    print(f" Película: {PELICULAS[indice_pelicula]} ({HORARIOS[indice_pelicula]})")
    print(f" Entradas: {cantidad}")
    print(f" Total a pagar: ${total_pago:.2f}")
    
    confirmacion = input("\n¿Confirma la reserva? (S/N): ")
    if confirmacion.upper() == "S":
        # Modificación de acumuladores y contadores
        asientos_vendidos[indice_pelicula] += cantidad
        total_entradas_vendidas += cantidad
        recaudacion_total += total_pago
        print("¡Reserva realizada con éxito!")
    else:
        print("Reserva cancelada por el usuario.")


def mostrar_estadisticas():
    """Muestra métricas del sistema recopiladas en la sesión."""
    print("\n======================================")
    print("      ESTADÍSTICAS DEL SISTEMA        ")
    print("======================================")
    print(f"Total de entradas vendidas hoy: {total_entradas_vendidas}")
    print(f"Recaudación total de la jornada: ${recaudacion_total:.2f}")
    
    # Buscar la película más elegida utilizando bucles y condiciones
    if total_entradas_vendidas > 0:
        max_entradas = -1
        pos_max = 0
        for i in range(len(asientos_vendidos)):
            if asientos_vendidos[i] > max_entradas:
                max_entradas = asientos_vendidos[i]
                pos_max = i
        print(f"La película más demandada es: {PELICULAS[pos_max]} con {max_entradas} entradas.")
    else:
        print("Aún no se han registrado ventas en esta sesión.")
    print("======================================")


# --- MÓDULO PRINCIPAL / MENÚ ---
def menu_principal():
    """Bucle principal que interactúa con el usuario mediante consola."""
    finalizar = False
    
    while not finalizar:
        print("\n======================================")
        print("   SISTEMA DE RESERVAS DE CINE V1     ")
        print("======================================")
        print("1. Mostrar Cartelera y Disponibilidad")
        print("2. Registrar Nueva Reserva")
        print("3. Ver Estadísticas del Sistema")
        print("4. Salir")
        print("======================================")
        
        opcion_input = input("Seleccione una opción (1-4): ")
        valido, opcion = validar_opcion_menu(opcion_input, 1, 4)
        
        if valido:
            if opcion == 1:
                mostrar_cartelera()
            elif opcion == 2:
                realizar_reserva()
            elif opcion == 3:
                mostrar_estadisticas()
            elif opcion == 4:
                print("Gracias por utilizar el sistema de reservas de cine. ¡Hasta luego!")
                finalizar = True


# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()
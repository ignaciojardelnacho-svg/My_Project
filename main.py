from database import inicializar_bd, registrar_resultado_bd, obtener_partidos
from torneo import armar_grupos_aleatorios, generar_fixture_todos_contra_todos, calcular_tabla_posiciones

def menu():
    inicializar_bd()
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE TORNEO DE FÚTBOL ---")
        print("1. Cargar equipos y armar grupos aleatorios")
        print("2. Registrar resultado de un partido")
        print("3. Ver partidos / Fixture")
        print("4. Ver tabla de posiciones")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cant = int(input("Ingrese la cantidad de equipos a registrar: "))
            nombres = []
            for i in range(cant):
                nom = input(f"Nombre del equipo {i+1}: ")
                nombres.append(nom)
            
            cant_grupos = int(input("Ingrese la cantidad de grupos a formar: "))
            grupos = armar_grupos_aleatorios(nombres, cant_grupos)
            generar_fixture_todos_contra_todos(grupos)
            print("\n¡Grupos armados y fixture generado con éxito!")

        elif opcion == "2":
            partidos = obtener_partidos()
            print("\n--- PARTIDOS ---")
            for p in partidos:
                estado = f"{p['goles_local']} - {p['goles_visitante']}" if p['jugado'] else "Pendiente"
                print(f"ID: {p['id']} | {p['local']} vs {p['visitante']} [{estado}]")
            
            p_id = int(input("\nID del partido a registrar: "))
            gl = int(input("Goles del equipo local: "))
            gv = int(input("Goles del equipo visitante: "))
            registrar_resultado_bd(p_id, gl, gv)
            print("¡Resultado guardado correctamente!")

        elif opcion == "3":
            partidos = obtener_partidos()
            print("\n--- FIXTURE Y RESULTADOS ---")
            for p in partidos:
                estado = f"{p['goles_local']} - {p['goles_visitante']}" if p['jugado'] else "Pendiente"
                print(f"{p['local']} vs {p['visitante']} -> {estado}")

        elif opcion == "4":
            tabla = calcular_tabla_posiciones()
            print("\n--- TABLA DE POSICIONES ---")
            tabla_ordenada = sorted(tabla.items(), key=lambda x: (x[1]['pts'], x[1]['dg']), reverse=True)
            
            print(f"{'Equipo':<15} {'Grupo':<10} {'PTS':<5} {'PJ':<5} {'PG':<5} {'PE':<5} {'PP':<5} {'DG':<5}")
            print("-" * 60)
            for eq, stats in tabla_ordenada:
                print(f"{eq:<15} {stats['grupo']:<10} {stats['pts']:<5} {stats['pj']:<5} {stats['pg']:<5} {stats['pe']:<5} {stats['pp']:<5} {stats['dg']:<5}")

        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()

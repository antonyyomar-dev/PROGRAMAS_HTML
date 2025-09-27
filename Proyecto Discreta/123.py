
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib_venn import venn2


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

class Propuesta:
    def __init__(self, nombre= str, codigo= str, criterios=None):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__criterios = criterios if criterios else {}
        self.__votos = []
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def criterios(self):
        return self.__criterios
    
    
    @property
    def votos (self):
        return  self.__votos
    
    
    def imprimir_criterios(self):
        for c, v in self.__criterios.items():
            print(f"+ {c:<10} {v}")
    
    def votar (self, usuario):
        self.__votos.append(usuario)
        
    
class Usuario:
    def __init__(self, id, nombre):
        self.__id = id
        self.__nombre = nombre
    
    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre

class Operaciones:
    def __init__(self):
        self.__lista_usuarios = []
        self.__lista_propuestas = []
        
    def existe_id (self,id):
        for e in self.__lista_usuarios:
            if e.id == id:
                return True
        return False
    
    def guardar_usuarios (self,usuario): 
        self.__lista_usuarios.append(usuario)
        
    def guardar_propuesta(self, propuesta):
        # Verificar que el código no se repita
        for p in self.__lista_propuestas:
            if p.codigo == propuesta.codigo:
                print(f"⚠️ Ya existe una propuesta con el código {propuesta.codigo}. No se puede agregar.")
                return False
        self.__lista_propuestas.append(propuesta)
        return True
    
    def imprimir_propuestas(self):
        print("-"*50)
        print("VER DETALLES DE VOTOS Y PROPUESTAS".center(50))
        print("-"*50)
        
        if not self.__lista_propuestas:
            print("No hay propuestas registradas.")
            input("Presione una tecla para continuar...")
            return

        tabla = []
        for e in self.__lista_propuestas:
            tabla.append([ e.codigo, e.nombre, len(e.votos)])
            
        cabezales = ["Código", "Nombre", "N° de Votos"]
        print(tabulate(tabla, headers=cabezales, tablefmt="grid"))
    
    def existe_propuesta(self, codigo):
        for p in self.__lista_propuestas:
            if p.codigo == codigo:
                return True
        return False
    
    def crear_propuesta(self):
        limpiar()
        print("-"*50)
        print("CREAR PROPUESTA".center(50))
        print("-"*50)
        
        cantidad = int(input("Ingresar la cantidad de propuestas a crear (3, 4 o 5): "))
        
        for i in range(cantidad):
            print("-"*50)
            nombre = input(f"Nombre de la propuesta {i+1}: ")
            while True:
                codigo = input("Código (4 dígitos): ")
                if len(codigo) != 4:
                    print("⚠️ El código debe tener 4 dígitos")
                    continue
                
                if any(p.codigo == codigo for p in self.__lista_propuestas):
                    print(f"⚠️ Ya existe una propuesta con el código {codigo}. Ingrese otro.")
                    continue
                
                break
            
            criterios = {}
            print("1. Tecnológico\n2. Politico\n3. Educativo\n4. Salir")
            while True:
                opcion = input("Seleccione criterio: ")
                if opcion == "1":
                    criterios["Tecnológico"] = []
                elif opcion == "2":
                    criterios["Politico"] = []
                elif opcion == "3":
                    criterios["Educativo"] = []
                elif opcion == "4":
                    break
                else:
                    print("⚠️ Opción inválida")
                print("AGREGADO.......")
            propuesta = Propuesta(nombre, codigo, criterios)
            self.guardar_propuesta(propuesta)
            
    def votar_propuesta(self):

        print("-"*50)
        print("REGISTRE SU IDENTIDAD ANTES DE VOTAR".center(50))
        print("-"*50)
        try:
            while True:
                id = input("Ingrese su DNI: ")
                if len(id) == 8 and id.isdigit():
                    break
        except ValueError:
            print("Error en el ingreso de datos........")
            return
        try:
            nombre = input("Nombre de Usuario: ").title()
        except ValueError:
            print("Error en el ingreso de datos .......")
            return
        usuario = Usuario(id, nombre)
        self.guardar_usuarios(usuario)
        contador = 0
        
        self.imprimir_propuestas()
        print("-"*40)
        
        while True: 
            codigo = input("Ingrese el código de la propuesta a votar: ")
            for p in self.__lista_propuestas:
                if p.codigo == codigo:
                    encontrado = True

                    ya_voto = False
                    for criterio in p.criterios.keys():
                        if usuario.nombre in p.criterios[criterio]:
                            ya_voto = True
                            break
                    if ya_voto:
                        print("⚠️ Usted ya ha votado por esta propuesta.")
                        break
                    for criterio in p.criterios.keys():
                        p.criterios[criterio].append(usuario.nombre)
                    voto = f"{usuario.id}-->{usuario.nombre}"
                    p.votar(voto)
                    print("✅ Voto registrado")
                    
                    salir = input("¿Desea seguir votando? (SI/NO): ").strip().upper()
                    if salir == "NO":
                        return  
                    elif salir == "SI":
                        continue 
                    else:
                        print("⚠️ Responda SI o NO")
                        continue
            
            if not encontrado:
                print("⚠️ Propuesta no encontrada")
            
            
        
#! ---------------------------------------------------INTERSECCION UNION COMPLEMENTO - CONSENSO
    def calcular_interseccion_votantes(self):
        print("-"*70)
        print("CALCULAR INTERSECCIÓN".center(70))
        print("-"*70)

        if not self.__lista_propuestas:
            print("No hay propuestas registradas.")
            input("Presione una tecla para continuar...")
            return 

        print("PROPUESTAS DISPONIBLES")
        print("-"*70)
        for p in self.__lista_propuestas:
            print(f"{p.codigo} - {p.nombre}")
        print("-"*70)

        codigos_seleccionados = []
        print("Seleccione las propuestas para calcular la intersección (mínimo 2).")
        print("Escriba 'NO' cuando ya no desee seleccionar más.\n")

        while True:
            codigo = input("Ingrese el código de la propuesta: ").strip().upper()

            if codigo == "NO":
                if len(codigos_seleccionados) < 2:
                    print("⚠️ Debe seleccionar al menos 2 propuestas antes de salir.")
                    continue
                else:
                    break

            existe = False
            for p in self.__lista_propuestas:
                if p.codigo == codigo:
                    existe = True
                    break

            if existe:
                if codigo not in codigos_seleccionados:
                    codigos_seleccionados.append(codigo)
                    print(f"✅ Propuesta {codigo} agregada.")
                else:
                    print("⚠️ Ya seleccionó esa propuesta.")
            else:
                print("⚠️ Código de propuesta no válido.")

        propuestas_filtradas = []
        for p in self.__lista_propuestas:
            if p.codigo in codigos_seleccionados:
                propuestas_filtradas.append(p)

        print("\n" + "="*70)
        print("INTERSECCIÓN DE VOTANTES POR PROPUESTAS".center(70))
        print("="*70)

        conjuntos_votantes = []
        for p in propuestas_filtradas:
            nombres_votantes = set([v.split("-->")[1] for v in p.votos])
            conjuntos_votantes.append(nombres_votantes)
            print(f"{p.nombre} = {{{', '.join(nombres_votantes) if nombres_votantes else ''}}}")

        if conjuntos_votantes: 
            interseccion_propuestas = conjuntos_votantes[0]   
            for conjunto in conjuntos_votantes[1:]:           
                interseccion_propuestas = interseccion_propuestas.intersection(conjunto)
        else:
            interseccion_propuestas = set()
            
        print("-"*70)
        if interseccion_propuestas:
            print("Personas que han votado en TODAS las propuestas seleccionadas:")
            print(", ".join(interseccion_propuestas))
        else:
            print("Nadie ha votado en todas las propuestas seleccionadas.")

        print("\n" + "="*70)
        print("INTERSECCIÓN DE VOTANTES POR CRITERIOS".center(70))
        print("="*70)

        criterios_globales = {}
        for p in propuestas_filtradas:
            for criterio, votantes in p.criterios.items():
                if criterio not in criterios_globales:
                    criterios_globales[criterio] = set()
                criterios_globales[criterio].update(votantes)

        for criterio, votantes in criterios_globales.items():
            print(f"{criterio} = {{{', '.join(votantes) if votantes else ''}}}")

        if criterios_globales:  
            interseccion_criterios = list(criterios_globales.values())[0]
            
            for conjunto in list(criterios_globales.values())[1:]:
                interseccion_criterios = interseccion_criterios.intersection(conjunto)
        else:
            interseccion_criterios = set()
        print("-"*70)
        
        if interseccion_criterios:
            print("Personas que cumplen con TODOS los criterios de las propuestas seleccionadas:")
            print(", ".join(interseccion_criterios))
        else:
            print("Nadie cumple con todos los criterios de las propuestas seleccionadas.")

        input("\nPresione una tecla para continuar...")

            
    def calcular_union_votantes(self):
        print("-"*70)
        print("CALCULAR UNIÓN".center(70))
        print("-"*70)

        if not self.__lista_propuestas:
            print("No hay propuestas registradas.")
            input("Presione una tecla para continuar...")
            return 

        print("PROPUESTAS DISPONIBLES")
        print("-"*70)
        for p in self.__lista_propuestas:
            print(f"{p.codigo} - {p.nombre}")
        print("-"*70)

        codigos_seleccionados = []
        print("Seleccione las propuestas para calcular la unión (mínimo 2).")
        print("Escriba 'NO' cuando ya no desee seleccionar más.\n")

        while True:
            codigo = input("Ingrese el código de la propuesta: ").strip().upper()

            if codigo == "NO":
                if len(codigos_seleccionados) < 2:
                    print("⚠️ Debe seleccionar al menos 2 propuestas antes de salir.")
                    continue
                else:
                    break

            existe = False
            for p in self.__lista_propuestas:
                if p.codigo == codigo:
                    existe = True
                    break

            if existe:
                if codigo not in codigos_seleccionados:
                    codigos_seleccionados.append(codigo)
                    print(f"Propuesta {codigo} agregada.")
                else:
                    print("Ya seleccionó esa propuesta.")
            else:
                print("Código de propuesta no válido.")

        propuestas_filtradas = []
        for p in self.__lista_propuestas:
            if p.codigo in codigos_seleccionados:
                propuestas_filtradas.append(p)

        print("\n" + "="*70)
        print("UNIÓN DE VOTANTES POR PROPUESTAS".center(70))
        print("="*70)

        conjuntos_votantes = []
        for p in propuestas_filtradas:
            nombres_votantes = set([v.split("-->")[1] for v in p.votos])
            conjuntos_votantes.append(nombres_votantes)
            print(f"{p.nombre} = {{{', '.join(nombres_votantes) if nombres_votantes else ''}}}")

        if conjuntos_votantes: 
            union_propuestas = conjuntos_votantes[0]   
            for conjunto in conjuntos_votantes[1:]:           
                union_propuestas = union_propuestas.union(conjunto)
        else:
            union_propuestas = set()
            
        print("-"*70)
        if union_propuestas:
            print("Todas las personas que votaron al menos en una de las propuestas seleccionadas:")
            print(", ".join(union_propuestas))
        else:
            print("Nadie ha votado en las propuestas seleccionadas.")

        print("\n" + "="*70)
        print("UNIÓN DE VOTANTES POR CRITERIOS".center(70))
        print("="*70)

        criterios_globales = {}
        for p in propuestas_filtradas:
            for criterio, votantes in p.criterios.items():
                if criterio not in criterios_globales:
                    criterios_globales[criterio] = set()
                criterios_globales[criterio].update(votantes)

        for criterio, votantes in criterios_globales.items():
            print(f"{criterio} = {{{', '.join(votantes) if votantes else ''}}}")

        if criterios_globales:  
            valores = list(criterios_globales.values())
            union_criterios = valores[0]
            for conjunto in valores[1:]:
                union_criterios = union_criterios.union(conjunto)
        else:
            union_criterios = set()
        print("-"*70)
        
        if union_criterios:
            print("Todas las personas que votaron en al menos un criterio de las propuestas seleccionadas:")
            print(", ".join(union_criterios))
        else:
            print("Nadie cumple con algún criterio de las propuestas seleccionadas.")

        input("\nPresione una tecla para continuar...")
            

    def contar_votantes_por_criterio(self):
        #limpiar()
        print("-"*50)
        print("CONTAR VOTANTES POR CRITERIO".center(50))
        print("-"*50)
        
        conteo = {"Tecnológico": set(), "Politico": set(), "Educativo": set()} 
        
        for p in self.__lista_propuestas:
            for criterio, votantes in p.criterios.items(): 
                conteo[criterio].update(votantes) 
        
        tabla = [] 
        for criterio, votantes in conteo.items():
            tabla.append([criterio, len(votantes), ', '.join(votantes)])
        cabezales = ["Criterio", "Número de Votantes", "Nombres de Votantes"]
        
        print(tabulate(tabla, headers= cabezales, tablefmt="grid"))
        input("Presione una tecla para continuar...")
    
    def propuesta_mayor_consenso(self):
        #limpiar()
        if not self.__lista_propuestas:
            print("No hay propuestas disponibles.")
            return
        
        propuesta_mas_votada = max(self.__lista_propuestas, key=lambda p: len(p.votos))
        
        print(f"La propuesta con mayor consenso es '{propuesta_mas_votada.nombre}' con [ {len(propuesta_mas_votada.votos)} ] votos.")
        print()
        input("Presione una tecla para continuar...")
    

def caratula():
    limpiar()
    print("="*50)
    print("PRIMER ENTREGABLE".center(50))
    print("APLICACIÓN DE LA TEORÍA DE CONJUNTOS EN".center(50))
    print("EL ANÁLISIS DE VOTACIONES MULTICRITERIO".center(50))
    print("="*50)
    print("Curso: MATEMATICA DISCRETA".center(50))
    print("Profesor: Juan Manuel Mattos Quevedo".center(50))
    print("Seccion: 6406".center(50))
    print("-"*50)
    
    

def menu():
    limpiar()
    print("==========================================")
    print("      PROYECTO 3: TEORÍA DE CONJUNTOS")
    print("              Menu principal")
    print("==========================================")
    print("[1] Ingresar propuestas")
    print("[2] Ingresar voto")
    print("[3] Mostrar interseccion de votantes")
    print("[4] Mostrar union de votantes")
    print("[5] Mostrar complementos (diferencias)")
    print("[6] Determinar propuesta con mayor consenso")
    print("[7] Visualizar diagrama de Venn")
    print("[8] Ver detalles de votos y propuestas")
    print("[9] Ver detalles de votantes por criterio")
    print("[0] Salir")

def main():
    
    g = Operaciones()
    caratula()
    input("Presione para continuar... ")
    while True:
        while True:
            menu()
            try:
                opcion = int(input("Ingresar opcion: "))
                if 0<= opcion <= 9: 
                    break
                else:
                    print("Opcion incorrecta")
            except ValueError:
                print("Debe ingresar una opcion valida")
                
                
        if opcion == 0:
            break
        elif opcion == 1:
            print("INGRESAR PROPUESTA")
            print("-"*30)
            g.crear_propuesta()
            
        elif opcion == 2:
            print("INGRESAR VOTO")
            print("-"*30)
            g.votar_propuesta()
        elif opcion == 3:
            print("MOSTRAR UNION DE VOTANTES SEGUN CRITERIO O PROPUESTA")
            print("-"*30)
            g.calcular_interseccion_votantes()
        elif opcion == 4:
            print("MOSTRAR INTERSECCION DE VOTANTES SEGUN CRITERIO O PROPUESTA")
            g.calcular_union_votantes()
    
        elif opcion == 5:
            print("MOSTRAR COMPLEMENTOS DE VOTANTES SEGUN CRITERIO O PROPUESTA")
            print("-"*30)
        elif opcion == 6:
            print("PROPUESTA CON MAYOR CONSENSO DE VOTANTES")
            print("-"*30)
            g.propuesta_mayor_consenso()

        elif opcion == 7:
            print("DIAGRAMA DE VENN")
            print("-"*30)
      
        elif opcion == 8: 
            g.imprimir_propuestas()
        
        elif opcion == 9: 
            g.contar_votantes_por_criterio()
            
main()

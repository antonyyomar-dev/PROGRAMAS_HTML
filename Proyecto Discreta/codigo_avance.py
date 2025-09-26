
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
        #limpiar()
        print("-"*50)
        print("VER DETALLES DE VOTOS Y PROPUESTAS".center(50))
        print("-"*50)
        
        for p in self.__lista_propuestas:
            print("-"*50)
            print(f"CODIGO: {p.codigo} - NOMBRE: {p.nombre}")
            for c, v in p.criterios.items():
                print(f"+ {c:<10} {v}")
            print("-"*50)
            print("VOTOS:", len(p.votos))
        
        input("Presione una tecla para continuar...")
    
    def existe_propuesta(self, codigo):
        for p in self.__lista_propuestas:
            if p.codigo == codigo:
                return True
        return False
    
    def crear_propuesta(self):
        #limpiar()
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
        # Un usuario no puede votar por la misma propuesta 2 veces
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
        for p in self.__lista_propuestas:
            contador += 1
            print(f"PROPUESTA N° {contador}".center(50))
            print("-"*50)
            print(f"CODIGO: {p.codigo} - NOMBRE: {p.nombre}")
            for c, v in p.criterios.items():
                print(f"+ {c:<10}")
            print("-"*50)
            print("VOTOS:", len(p.votos))
        codigo = input("Ingrese el código de la propuesta a votar: ")
        for p in self.__lista_propuestas:
            if p.codigo == codigo:
                # Revisar si el usuario ya votó por esta propuesta
                ya_voto = False
                for criterio in p.criterios.keys():
                    if usuario.nombre in p.criterios[criterio]:
                        ya_voto = True
                        break
                if ya_voto:
                    print("⚠️ Usted ya ha votado por esta propuesta.")
                    return
                for criterio in p.criterios.keys():
                    p.criterios[criterio].append(usuario.nombre)
                voto = f"{usuario.id}-->{usuario.nombre}"
                p.votar(voto)
                print("✅ Voto registrado")
                return
        print("⚠️ Propuesta no encontrada")


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
    #limpiar()
    print("==========================================")
    print("      PROYECTO 3: TEORÍA DE CONJUNTOS")
    print("              Menu principal")
    print("==========================================")
    print("[1] Ingresar propuestas")
    print("[2] Ingresar voto")
    print("[3] Mostrar unión de votantes")
    print("[4] Mostrar intersección de votantes")
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
        elif opcion == 4:
            print("MOSTRAR INTERSECCION DE VOTANTES SEGUN CRITERIO O PROPUESTA")
            print("-"*30)
    
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

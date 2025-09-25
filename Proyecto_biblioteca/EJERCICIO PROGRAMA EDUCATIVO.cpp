#include<iostream>
#include<conio.h>
#include<string>
using namespace std;
using namespace System;
struct tfecha
{
	int dia, mes, anio;
};
struct talumno
{
	string codalumno, nombre, carrera;
};
struct tcurso
{
	string codcurso, nombre;
	double creditos;
};
struct talumnoxcurso
{
	string codalumno, codcurso;
	int nota;
	tfecha fecharegistro;
};
bool anio_bisiesto(int anio)
{
	return (((anio % 4) == 0) && !((anio % 100) == 0)) || ((anio % 400) == 0);
}
bool fecha_valida(int dia, int mes, int anio)
{
	bool es_valida = false;
	if (anio > 0)
	{
		switch (mes)
		{
		case 1: case 3: case 5: case 7: case 8: case 10: case 12:
			if (dia > 0 && dia < 32)
				es_valida = true;
			break;
		case 4: case 6: case 9: case 11:
			if (dia > 0 && dia < 31)
				es_valida = true;
			break;
		case 2:
			if (anio_bisiesto(anio))
			{
				if (dia > 0 && dia < 30)
					es_valida = true;
			}
			else
				if (dia > 0 && dia < 29)
					es_valida = true;
			break;
		}
	}
	return es_valida;
}
int existe_alumno(talumno* valumnos, int nele, string codigoalu) // verificar si el codigoalu de alumno se encuentra en el arreglo de alumnos (*valumnos)
{
	int posicion = -1; // es -1 para ver si no se encuentra () no existe
	for (int i = 0; i < nele; i++)
	{
		if (valumnos[i].codalumno == codigoalu)
			posicion = i;  // si existe retornara un valor diferente a -1
	}
	return posicion;
}
int existe_curso(tcurso* vcursos, int nele, string codigocurso) // no pueden haber 2 cursos con el mismo codigo
{
	int posicion = -1;
	for (int i = 0; i < nele; i++)
	{
		if (vcursos[i].codcurso == codigocurso)
			posicion = i;
	}
	return posicion;
}
int existe_alumno_x_curso(talumnoxcurso* valumnosxcurso, int nele,
	string codalumno, string codcurso, int dia, int mes, int anio)
	// lo que estamos validad es verificar si existe el q tenga el mismo codigo de alumno, curso y fecha
{
	int posicion = -1;
	for (int i = 0; i < nele; i++)
	{
		if (valumnosxcurso[i].codalumno == codalumno &&
			valumnosxcurso[i].codcurso == codcurso &&
			valumnosxcurso[i].fecharegistro.dia == dia &&
			valumnosxcurso[i].fecharegistro.mes == mes &&
			valumnosxcurso[i].fecharegistro.anio == anio)
			posicion = i;
	}
	return posicion;
}
void menu_principal()
{
	Console::Clear();
	cout << "PROYECTO EDUCACION\n";
	cout << "===================\n";
	cout << "1. Registrar\n";
	cout << "2. Reportes\n";
	cout << "3. Salir\n";
}
void menu_registrar()
{
	Console::Clear();
	cout << "REGISTRAR DATOS\n";
	cout << "================\n";
	cout << "1. Registrar alumno\n";
	cout << "2. Registrar curso\n";
	cout << "3. Registrar nota final del alumno\n";
	cout << "4. Salir\n";
}
void menu_reportes()
{
	Console::Clear();
	cout << "REPORTES\n";
	cout << "========\n";
	cout << "1. Listado de cursos aprobados por un alumno\n";
	cout << "2. Cantidad de alumnos por carrera\n";
	cout << "3. Total de creditos aprobados de un alumno\n";
	cout << "4. Salir\n";
}
void registrar_alumno(talumno* valumnos, int& nalumnos)
{
	string codigo, nombre;
	int opcion;
	string vcarreras[4] = { "Ing. Sistemas","Ing. Civil","Ing.Industrial","Ing.Software" };
	cout << "Registrar alumno\n";// el codigo no se puede repetir
	do
	{										    
		cout << "Ingrese el codigo del alumno: "; cin >> codigo;
		if (existe_alumno(valumnos, nalumnos, codigo) != -1)
			cout << "El codigo ya existe, vuelva a ingresar un nuevo codigo\n";
	} while (existe_alumno(valumnos, nalumnos, codigo) != -1);
	cin.ignore();
	cout << "Ingrese nombre del alumno: ";
	getline(cin, nombre);
	do
	{
		cout << "Seleccione la carrera del alumno\n";
		cout << "1. Ing. Sistemas\n";
		cout << "2. Ing. Civil\n";
		cout << "3. Ing. Industrial\n";
		cout << "4. Ing. Software\n";
		cout << "Ingrese su opcion: "; cin >> opcion;
	} while (opcion < 1 || opcion >4);
	valumnos[nalumnos].codalumno = codigo;
	valumnos[nalumnos].nombre = nombre;
	valumnos[nalumnos].carrera = vcarreras[opcion - 1]; //opcion -1 porque.. el rango del vector es de (0,3) por eso se resta uno para que llege al rango
	nalumnos++;
	cout << "alumno registrado\n";
}
void registrar_curso(tcurso* vcursos, int& ncursos)
{
	string codigo, nombre;
	double creditos;
	cout << "Registrar curso\n"; // el codigo no se puede repetir
	do
	{
		cout << "Ingrese codigo del curso: "; cin >> codigo;
		if (existe_curso(vcursos, ncursos, codigo) != -1)
			cout << "El codigo ya existe, vuelva a ingresar un nuevo codigo\n";
	} while (existe_curso(vcursos, ncursos, codigo) != -1);
	cin.ignore();
	cout << "Ingrese nombre del curso: "; cin >> nombre;
	do
	{
		cout << "Ingrese la cantidad de creditos del curso: "; cin >> creditos;
	} while (creditos <= 0);
	vcursos[ncursos].nombre = nombre;
	vcursos[ncursos].creditos = creditos;
	vcursos[ncursos].codcurso = codigo;
	ncursos++;
	cout << "curso registrado\n";
}
void registrar_alumnoxcurso(talumnoxcurso* valumnosxcursos, int& nalumnosxcursos, talumno* valumnos, int nalumnos, tcurso* vcursos, int ncursos)
{
	string codigoalu, codcurso;
	int dia, mes, anio, nota;
	if (nalumnos > 0 && ncursos > 0)
	{
		cout << "Registrar nota de un alumno\n";
		do
		{
			do
			{
				cout << "Ingrese codigo de alumno: "; cin >> codigoalu;
				if (existe_alumno(valumnos, nalumnos, codigoalu) == -1) // es == porq vamos a analizar un alumno que ya existe
					cout << "el codigo no existe, vuelva a ingresar el codigo\n";
			} while (existe_alumno(valumnos, nalumnos, codigoalu) == -1);
			cin.ignore();
			do
			{
				cout << "Ingrese codigo del curso: "; cin >> codcurso;
				if (existe_curso(vcursos, ncursos, codcurso) == -1)
					cout << "el curso no existe, vuelva a ingresar el codigo\n";
			} while (existe_curso(vcursos, ncursos, codcurso) == -1);
			do
			{
				cout << "Ingrese el dia, mes y anio del registro: "; cin >> dia >> mes >> anio;
				if (fecha_valida(dia, mes, anio) == false)
					cout << "Fecha invalida, fuelva a ingresar la fecha\n";
			} while (fecha_valida(dia, mes, anio) == false);
			if (existe_alumno_x_curso(valumnosxcursos, nalumnosxcursos, codigoalu, codcurso, dia, mes, anio) != -1)
				cout << "La nota ya fue registrada, vuelva a ingresar los datos\n";
		} while (existe_alumno_x_curso(valumnosxcursos, nalumnosxcursos, codigoalu, codcurso, dia, mes, anio) != -1);
		do
		{
			cout << "Ingrese la nota del alumno: "; cin >> nota;
		} while (nota < 0 || nota > 20);
		valumnosxcursos[nalumnosxcursos].codalumno = codigoalu;
		valumnosxcursos[nalumnosxcursos].codcurso = codcurso;
		valumnosxcursos[nalumnosxcursos].fecharegistro.mes = mes;
		valumnosxcursos[nalumnosxcursos].fecharegistro.dia = dia;
		valumnosxcursos[nalumnosxcursos].fecharegistro.anio = anio;
		valumnosxcursos[nalumnosxcursos].nota = nota;
		nalumnosxcursos++;
		cout << "nota del alumno registrada\n";
	}
}
void listado_cursos_aprobados_de_un_alumno(talumnoxcurso* valumnosxcursos, int nalumnosxcursos, talumno* valumnos, int nalumnos, tcurso* vcursos, int ncursos)
{
	string codigoalu;
	talumno auxalumno;
	tcurso auxcurso;
	Console::Clear();
	cout << "Listado de cursos aprobados por un alumno\n";
	do
	{
		cout << "Ingrese codigo de alumno: "; cin >> codigoalu;
		if (existe_alumno(valumnos, nalumnos, codigoalu) == -1)
			cout << "el codigo del alumno no existe, ingrese de nuevo el codigo\n";
	} while (existe_alumno(valumnos, nalumnos, codigoalu) == -1);
	cin.ignore();
	auxalumno = valumnos[existe_alumno(valumnos, nalumnos, codigoalu)];
	cout << "codigo: " << auxalumno.codalumno << endl;
	cout << "nombre: " << auxalumno.nombre << endl;
	cout << "Curso\tNota\n";
	for (int i = 0; i < nalumnosxcursos; i++)
	{
		if (valumnosxcursos[i].codalumno == codigoalu)
		{
			if (valumnosxcursos[i].nota > 12)
			{
				auxcurso = vcursos[existe_curso(vcursos, ncursos, valumnosxcursos[i].codcurso)];
				cout << auxcurso.nombre << "\t" << valumnosxcursos[i].nota << endl;
			}
		}
	}
	cout << "Presione una tecla para continuar...\n";
	_getch();
}
int total_alumnos_en_una_carrera(talumno* valumnos, int nalumnos, string carrera)
{
	int total = 0;
	for (int i = 0; i < nalumnos; i++)
	{
		if (valumnos[i].carrera == carrera)
			total++;
	}
	return total;
}
void cantidad_de_alumnos_por_carrera(talumno* valumnos, int nalumnos)
{
	string vcarreras[4] = { "Ing. Sistemas", "Ing. Civil", "Ing. Industrial", "Ing. Software" };
	Console::Clear();
	cout << "Reporte de cantidad de alumnos por carrera\n";
	cout << "Carrera\tTotal\n";
	for (int i = 0; i < nalumnos; i++)
	{
		cout << vcarreras[i] << "\t" << total_alumnos_en_una_carrera(valumnos, nalumnos, vcarreras[i]) << endl;
	}
	cout << "Presione una tecla para continuar...\n";
	_getch();
}
void creditos_aprorbados_de_un_alumno(talumnoxcurso* valumnosxcursos, int nalumnosxcursos, talumno* valumnos, int nalumnos, tcurso* vcursos, int ncursos)
{
	string codigoalu;
	talumno auxalumno;
	tcurso auxcurso;
	double total = 0;
	Console::Clear();
	cout << "total de creditos aprobados de un alumno¿:\n";
	do
	{
		cout << "ingrese codigo del alumno:"; cin >> codigoalu;
		if (existe_alumno(valumnos, nalumnos, codigoalu) == -1)
			cout << "el codido del alumno mo existe , ingrese el nuevo codigo\n";
	} while (existe_alumno(valumnos, nalumnos, codigoalu) == -1);
	cin.ignore();
	auxalumno = valumnos[existe_alumno(valumnos, nalumnos, codigoalu) == -1];
	cout << "cdigo: " << auxalumno.codalumno << endl;
	cout << "nombre:" << auxalumno.nombre << endl;
	cout << "curso\tnot\tcreditos\n";
	for (int i = 0; i < nalumnosxcursos; i++)
	{
		if (valumnosxcursos[i].codalumno == codigoalu)
		{
			if (valumnosxcursos[i].nota > 12)
			{
				auxcurso = vcursos[existe_curso(vcursos, ncursos, valumnosxcursos[i].codcurso)];
				total = total + auxcurso.creditos;
				cout << auxcurso.nombre << "\t" << valumnosxcursos[i].nota << "\t" << auxcurso.creditos << endl;
			}
		}
	}
	cout << "total de creditos aprobados = " << total << endl;
	cout << "presione una tecla para continuar..\n";
	_getch();                   
}
void submenu_registrar(talumno* valumnos, tcurso* vcursos, talumnoxcurso* valumnosxcursos, int& nalumnos, int& ncursos, int& nalumnosxcursos)
{
	int opcion;
	do
	{
		menu_registrar();
		do
		{
			cout << "Ingrese la opcion: "; cin >> opcion;
		} while (opcion < 1 || opcion > 4);
		switch (opcion)
		{
		case 1:registrar_alumno(valumnos, nalumnos); break;
		case 2:registrar_curso(vcursos, ncursos); break;
		case 3:registrar_alumnoxcurso(valumnosxcursos, nalumnosxcursos, valumnos, nalumnos, vcursos, ncursos); break;
		}
		if (opcion != 4)
		{
			cout << "presione una tecla para continuar ....\n";
			_getch();
		}
	} while (opcion != 4);
}
void submenu_reportes(talumno* valumnos, tcurso* vcursos, talumnoxcurso* valumnosxcursos, int nalumnos, int ncursos, int& nalumnosxcursos)
{
	int opcion;
	do
	{
		menu_reportes();
		do
		{
			cout << "Ingrese opcion: "; cin >> opcion;
		} while (opcion < 1 || opcion > 4);
		switch (opcion)
		{
		case 1: listado_cursos_aprobados_de_un_alumno(valumnosxcursos, nalumnosxcursos, valumnos, nalumnos, vcursos, ncursos); break;
		case 2: cantidad_de_alumnos_por_carrera(valumnos, nalumnos); break;
		case 3: creditos_aprorbados_de_un_alumno(valumnosxcursos, nalumnosxcursos, valumnos, nalumnos, vcursos, ncursos); break;
		}
	} while (opcion != 4);

}
void main()
{
	talumno* valumnos = new talumno[50];
	tcurso* vcursos = new tcurso[50];
	talumnoxcurso* valumnosxcursos = new talumnoxcurso[50];
	int nalumnos = 0, ncursos = 0, nalumnosxcursos = 0;
	int opcion;
	do
	{
		menu_principal();
		do
		{
			cout << "Ingrese opcion: "; cin >> opcion;
		} while (opcion < 1 || opcion > 3);
		switch (opcion)
		{
		case 1: submenu_registrar(valumnos, vcursos, valumnosxcursos, nalumnos, ncursos, nalumnosxcursos); break;
		case 2: submenu_reportes(valumnos, vcursos, valumnosxcursos, nalumnos, ncursos, nalumnosxcursos); break;
		}
	} while (opcion != 3);
}
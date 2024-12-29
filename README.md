#include <iostream>
#include <conio.h>
#include <string>
#include <ctype.h>  
using namespace std;
using namespace System;
struct Tdias {
    int dia, mes, anio;
};

struct Tdireccion {
    string calle, ciudad, distrito;
    int numero;
};

struct Tlectores {
    int edad;
    string nombre, apellido, dni, celular;
    char sexo;
    Tdireccion direccion;
};
struct Tpublicaciones {
    string codigopublica, titulo;
    int tipo, local, disponible;
};
struct Tprestamos {
    string dnilector, codigopubli;
    Tdias fechaprestamo, fechadevolucion;
    int tipopubli;
};
struct Tdevoluciones {
    Tdias fechadevolucion;
    string dnilector,nombre, nlector, codigopubli;
};
bool anio_biciesto_prestamo(Tprestamos* vprestamos, int n)
{
    return (((vprestamos[n].fechaprestamo.anio % 4) == 0) && !((vprestamos[n].fechaprestamo.anio % 100) == 0)) || ((vprestamos[n].fechaprestamo.anio % 400) == 0);
}
bool anio_biciesto_actual(Tdias fechaactual)
{
    return (((fechaactual.anio % 4) == 0) && !((fechaactual.anio % 100) == 0)) || ((fechaactual.anio % 400) == 0);
}
int comparar_fechas(Tdias fecha1, Tdias fecha2)
{
    int dato = 0; // fechas iguales
    if (fecha2.anio < fecha1.anio)
    {
        dato = 1; // fecha 1 es mas actual
    }
    else
    {
        if (fecha2.anio > fecha1.anio)
        {
            dato = 2; // fecha 2 es mas actual
        }
    }
    if (fecha2.mes < fecha1.mes)
    {
        dato = 1;
    }
    else
    {
        if (fecha2.mes > fecha1.mes)
        {
            dato = 2;
        }
    }
    if (fecha2.dia < fecha1.dia)
    {
        dato = 1;
    }
    else
    {
        if (fecha2.dia > fecha1.dia)
            dato = 2;
    }
    return dato;
}
int fecha_valida_actual(Tdias fechaactual)
{
    int esvalida = -1;
    if (fechaactual.anio > 0)
    {
        switch (fechaactual.mes)
        {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            if (fechaactual.dia > 0 && fechaactual.dia < 32)
                esvalida = 0; break;
        case 4: case 6: case 9: case 11:
            if (fechaactual.dia > 0 && fechaactual.dia < 31)
                esvalida = 0; break;
        case 2:
            if (anio_biciesto_actual(fechaactual))
            {
                if (fechaactual.dia > 0 && fechaactual.dia < 30)
                {
                    esvalida = 0;
                }
            }
            else
            {
                if (fechaactual.dia > 0 && fechaactual.dia < 29)
                    esvalida = 0; break;
            }
        }
    }
    return esvalida;
}
int devolucion_fuera_de_fecha(Tdias fechaactual, Tprestamos* vprestamos, int n)
{
    int dato = 0; // devolucion fuera de fecha

    if (fechaactual.anio < vprestamos[n].fechadevolucion.anio)
        dato = 1;
    else
        if (fechaactual.anio > vprestamos[n].fechadevolucion.anio)
            dato = 2;
    if (fechaactual.mes < vprestamos[n].fechadevolucion.mes)
        dato = 1;
    else
        if (fechaactual.mes > vprestamos[n].fechadevolucion.mes)
            dato = 2;
    if (fechaactual.dia < vprestamos[n].fechadevolucion.dia)
        dato = 1;
    else
        if (fechaactual.dia > vprestamos[n].fechadevolucion.dia)
            dato = 2;
    return dato;
}
void observacion_devolucion_fuera_de_fecha(Tprestamos* vprestamos, int nprestamos, Tdevoluciones* vdevoluciones, int ndevoluciones)
{
    int aux;
    for (int i = 0; i < nprestamos; i++)
    {
        if (vdevoluciones[ndevoluciones].codigopubli == vprestamos[i].codigopubli)
        {
            Tdias fechadevolucion, fechalimite;
            fechadevolucion.dia = vdevoluciones[ndevoluciones].fechadevolucion.dia;
            fechadevolucion.mes = vdevoluciones[ndevoluciones].fechadevolucion.mes;
            fechadevolucion.anio = vdevoluciones[ndevoluciones].fechadevolucion.anio;
            fechalimite.dia = vprestamos[i].fechadevolucion.dia;
            fechalimite.mes = vprestamos[i].fechadevolucion.mes;
            fechalimite.anio = vprestamos[i].fechadevolucion.anio;
            aux = 0;
                if (comparar_fechas(fechadevolucion, fechalimite) == 1)
                {
                    cout << "\nObservacion: Devolucion atrasada, no puede hacer prestamos en un mes";
                }
        }
    }
}
int lector_registrado(Tlectores* vlectores, Tprestamos* vprestamos, int n)
{
    int dato = -1;// no existe el lector 
    for (int i = 0; i < n; i++)
    {
        if (vlectores[i].dni == vprestamos[n].dnilector)
        {
            dato = i; // el dni ya existe
        }
    }
    return dato;
}
int estado_prestamo(Tprestamos* vprestamos, Tdevoluciones* vdevoluciones, int n)
{
    int prestado = -1; // la publicacion no ha sido devuelta
    for (int i = 0; i < n; i++)
    {
        if (vprestamos[i].codigopubli == vdevoluciones[n].codigopubli)
        {
            for (int j = 0; j < n; n++)
            {
                if (vprestamos[i].codigopubli == vdevoluciones[j].codigopubli)
                {
                    prestado = 1; // la publicacion ha sido devuelta 
                }
            }
        }

    }
    return prestado;
}
int publicacion_disponible(Tpublicaciones* vpublicaciones, Tprestamos* vprestamos, int n, int npublicaciones)
{
    int dato = -1; // publicacion no disponible
    string codigopublicacion = vprestamos[n].codigopubli;
    for (int i = 0; i < npublicaciones; i++)
    {
        if ((codigopublicacion == vpublicaciones[i].codigopublica) && (vpublicaciones[i].disponible == 1))
            dato = i; // publicacion disponible
    }
    return dato;
}
void publicacion_prestar(Tpublicaciones* vpublicaciones, Tprestamos* vprestamos, int n, int npublicaciones)
{
    for (int i = 0; i < npublicaciones; i++)
    {
        if (vprestamos[n].codigopubli == vpublicaciones[i].codigopublica)
        {
            vpublicaciones[i].disponible = 2;
        }
    }
}
void mostrar_publicaciones_disponibles(Tpublicaciones* vpublicaciones, Tprestamos* vprestamos, int npublicaciones, int nprestamos)
{
    string tipos[3] = { "REVISTA", "PERIODICO", "LIBRO" };
    string locales[3] = { "LOS OLIVOS", "SAN JUAN DE LURIGANCHO", "CHORRILLOS" };
    int tipopublicacion = vprestamos[nprestamos].tipopubli;
    cout << "Publicaciones  de tipo " << tipos[tipopublicacion - 1] << " disponibles:\n\n";
    for (int i = 0; i < npublicaciones; i++)
    {
        if ((vpublicaciones[i].tipo == tipopublicacion) && (vpublicaciones[i].disponible == 1))
        {
            cout << "Publicacion " << i + 1 << ":" << endl;
            cout << "Local :\t\t" << locales[vpublicaciones[i].local - 1] << endl;
            cout << "Codigo :\t" << vpublicaciones[i].codigopublica << endl;
            cout << "Titulo :\t\t" << vpublicaciones[i].titulo << endl;
        }
    }
}      
void contar_por_tipo(Tpublicaciones* vpublicaciones, int n)
{
    int contp = 0, contr = 0, contl = 0;
    for (int i = 0; i < vpublicaciones; i++)
    {
        if (vpublicaciones[i].tipo == 1)
        {
            contr++;
        }
        if (vpublicaciones[i].tipo == 2)
        {
            contp++;
        }
        else
            contl++;
    }
    cout << "cantidad de revistas : " << contr << endl;
    cout << "cantidad de periodicos : " << contp << endl;
    cout << "cantidad de libros: " << contl << endl;
}
void menu_principal()
{
    Console::Clear();
    cout << "Menu principal\n";
    cout << "------------------\n";
    cout << "1. Registrar\n";
    cout << "2. Reportes\n";
    cout << "3. Presentacion\n";
    cout << "5. Salir\n";
}
void submenu_registrar(int opcion)
{

    Console::Clear();
    cout << "Registrar\n";
    cout << "------------------\n";
    cout << "1. Publicacion\n";
    cout << "2. Lector\n";
    cout << "3. Prestamo\n";
    cout << "4. Devolucion\n";
    cout << "5. Salir\n";
}
void submenu_reportes(int opcion)
{

    Console::Clear();
    cout << "Reportes\n";
    cout << "------------------\n";
    cout << "1. Publicaciones\n";
    cout << "2. Lectores\n";
    cout << "3. Prestamos\n";
    cout << "4. Devoluciones\n";
    cout << "5. Listado de publicaciones pendientes de devolucion fuera de fecha(Reporte 1)\n";
    cout << "6. Numero de lectores por rango de edad para cada tipo de publicacion(Reporte 2)\n";
    cout << "7. graficos\n";
    cout << "8. Salir\n";
}
void presentacion()
{
    Console::Clear();
    cout << "                           .-                               \n";
    cout << "                          -*-                               \n";
    cout << "                  .      =**:           .                   \n";
    cout << "                :-      =***=           .=.                 \n";
    cout << "               ==      .*****:           .+:                \n";
    cout << "              =*.      :******=.          -*:               \n";
    cout << "             =*=       :********-         .**.              \n";
    cout << "            .**-       .*********=         +*=              \n";
    cout << "            =**-        -*********:        ***.             \n";
    cout << "            +**=         -********+       .***-             \n";
    cout << "            ****.         :+*******       =***=             \n";
    cout << "            ****+           -*****+      :****-             \n";
    cout << "            +****=           :****-     :*****:             \n";
    cout << "            -*****+:          +**+     -*****+              \n";
    cout << "             +******=:        +*=   .-+******:              \n";
    cout << "             .********+-:.   .+: .-=********=               \n";
    cout << "              .+***********+++++***********=                \n";
    cout << "               .=*************************:                 \n";
    cout << "                 :+*********************=.                  \n";
    cout << "                   :=****************+-.                    \n";
    cout << "                      :-=++*****++=:.                       \n";
    cout << "                          UPC      .                        \n";
    cout << "                  FACULTAD DE INGENIERIA                    \n\n\n";
    cout << "\tPe a Ro a Antony Yomar          (U202421102)\n";
    cout << "\tRamos Rodriguez Jose Matias     (U20241G339)\n"; 
    cout << "\tLuis Anibal Chicana Guadalupe   (U202422332)\n";
    cout << "\nPresione una tecla para regresar...";
}
void salir()
{

    Console::Clear();
    cout << "Presione una tecla para salir...\n";
    _getch();
}

void devoluciones_x_defecto(Tdevoluciones* vdevoluciones)
{
    vdevoluciones[0].codigopubli = "93827456"; vdevoluciones[0].dnilector = "78123456";
    vdevoluciones[0].fechadevolucion.dia = 13; vdevoluciones[0].fechadevolucion.mes = 11; vdevoluciones[0].fechadevolucion.anio = 2024;

    vdevoluciones[1].codigopubli = "71645328"; vdevoluciones[1].dnilector = "09781234";
    vdevoluciones[1].fechadevolucion.dia = 14; vdevoluciones[1].fechadevolucion.mes = 11; vdevoluciones[1].fechadevolucion.anio = 2024;
}
void publicaciones_x_defecto(Tpublicaciones* vpublicaciones)
{
    vpublicaciones[0].tipo = 1;
    vpublicaciones[0].local = 1;
    vpublicaciones[0].codigopublica = "93827456";
    vpublicaciones[0].titulo = "LIMA URBANA ";
    vpublicaciones[0].disponible = 1;

    vpublicaciones[1].tipo = 2;
    vpublicaciones[1].local = 1;
    vpublicaciones[1].codigopublica = "58293047";
    vpublicaciones[1].titulo = "EL DIARIO DEL PUEBLO";
    vpublicaciones[1].disponible = 2;

    vpublicaciones[2].tipo = 3;
    vpublicaciones[2].local = 2;
    vpublicaciones[2].codigopublica = "71645328";
    vpublicaciones[2].titulo = "REFLEJOS DEL PERU   ";
    vpublicaciones[2].disponible = 2;

}
void lectores_x_defecto(Tlectores* vlectores)
{
    vlectores[0].sexo = 'F'; vlectores[0].edad = 20; vlectores[0].nombre = "ANA LUISA"; vlectores[0].apellido = "FLORES QUISPE"; vlectores[0].celular = "994145013"; vlectores[0].dni = "78123456";
    vlectores[0].direccion.calle = "SAN IGNACIO"; vlectores[0].direccion.numero = 765; vlectores[0].direccion.ciudad = "LIMA"; vlectores[0].direccion.distrito = "CHORRILLOS";

    vlectores[1].sexo = 'F'; vlectores[1].edad = 40; vlectores[1].nombre = "ROSA MARIA"; vlectores[1].apellido = "AGUIRRE ESPINOZA"; vlectores[1].celular = "935784294"; vlectores[1].dni = "41765432";
    vlectores[1].direccion.calle = "JIRON ANEMONAS"; vlectores[1].direccion.numero = 875; vlectores[1].direccion.ciudad = "LIMA"; vlectores[1].direccion.distrito = "SAN JUAN DE LURIGANCHO";

    vlectores[2].sexo = 'F'; vlectores[2].edad = 70; vlectores[2].nombre = "LOURDES CAMILA"; vlectores[2].apellido = "RODRIGUEZ PLATA"; vlectores[2].celular = "907540325"; vlectores[2].dni = "09781234";
    vlectores[2].direccion.calle = "MODELO"; vlectores[2].direccion.numero = 234; vlectores[2].direccion.ciudad = "LIMA"; vlectores[2].direccion.distrito = "VILLA EL SALVADOR";

    vlectores[3].sexo = 'M'; vlectores[3].edad = 70; vlectores[3].nombre = "JUAN PAULO"; vlectores[3].apellido = "RAMIREZ RAMOS"; vlectores[3].celular = "985427105"; vlectores[3].dni = "05768390";
    vlectores[3].direccion.calle = "LARCO"; vlectores[3].direccion.numero = 1234; vlectores[3].direccion.ciudad = "LIMA"; vlectores[3].direccion.distrito = "MIRAFLORES";
}
void prestamos_x_defecto(Tprestamos* vprestamos)
{
    vprestamos[0].codigopubli = "93827456"; vprestamos[0].dnilector = "78123456"; vprestamos[0].tipopubli = 1;
    vprestamos[0].fechaprestamo.dia = 8; vprestamos[0].fechaprestamo.mes = 11; vprestamos[0].fechaprestamo.anio = 2024;
    vprestamos[0].fechadevolucion.dia = 13; vprestamos[0].fechadevolucion.mes = 11; vprestamos[0].fechadevolucion.anio = 2024;

    vprestamos[1].codigopubli = "58293047"; vprestamos[1].dnilector = "41765432"; vprestamos[1].tipopubli = 2;
    vprestamos[1].fechaprestamo.dia = 10; vprestamos[1].fechaprestamo.mes = 11; vprestamos[1].fechaprestamo.anio = 2024;
    vprestamos[1].fechadevolucion.dia = 12; vprestamos[1].fechadevolucion.mes = 11; vprestamos[1].fechadevolucion.anio = 2024;

    vprestamos[2].codigopubli = "71645328"; vprestamos[2].dnilector = "09781234"; vprestamos[2].tipopubli = 3;
    vprestamos[2].fechaprestamo.dia = 11; vprestamos[2].fechaprestamo.mes = 11; vprestamos[2].fechaprestamo.anio = 2024;
    vprestamos[2].fechadevolucion.dia = 16; vprestamos[2].fechadevolucion.mes = 11; vprestamos[2].fechadevolucion.anio = 2024;

    vprestamos[3].codigopubli = "71645328"; vprestamos[3].dnilector = "05768390"; vprestamos[3].tipopubli = 3;
    vprestamos[3].fechaprestamo.dia = 17; vprestamos[3].fechaprestamo.mes = 11; vprestamos[3].fechaprestamo.anio = 2024;
    vprestamos[3].fechadevolucion.dia = 21; vprestamos[3].fechadevolucion.mes = 11; vprestamos[3].fechadevolucion.anio = 2024;
}

int existe_publicacion(Tpublicaciones* vpublicaciones, int n)
{
    int dato = -1;
    for (int i = 0; i < n; i++)
    {
        if (vpublicaciones[i].codigopublica == vpublicaciones[n].codigopublica)
        {
            dato = i;
        }
    }
    return dato;
}
int existe_lector(Tlectores* vlectores, int n)
{
    int dato = -1;
    for (int i = 0; i < n; i++)
    {
        if (vlectores[i].celular == vlectores[n].celular)
        {
            dato = i;
        }
        if (vlectores[i].dni == vlectores[n].dni)
        {
            dato = i;
        }
    }
    return dato;
}

int fecha_valida_prestamo(Tprestamos* vprestamos, int n)
{
    int esvalida = -1; // fecha no valida
    if (vprestamos[n].fechaprestamo.anio > 0)
    {
        switch (vprestamos[n].fechaprestamo.mes)
        {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            if (vprestamos[n].fechadevolucion.dia > 0 && vprestamos[n].fechadevolucion.dia < 32)
                esvalida = 0;
            break;
        case 4: case 6: case 9: case 11:
            if (vprestamos[n].fechadevolucion.dia > 0 && vprestamos[n].fechadevolucion.dia < 31)
                esvalida = 0;
            break;
        case 2:
            if (anio_biciesto_prestamo(vprestamos, n))
            {
                if (vprestamos[n].fechadevolucion.dia > 0 && vprestamos[n].fechadevolucion.dia < 30)
                {
                    esvalida = 0;
                }
            }
            else
            {
                if (vprestamos[n].fechadevolucion.dia > 0 && vprestamos[n].fechadevolucion.dia < 29)
                    esvalida = 0;
            }
            break;
        }
    }
    return esvalida;
}
int contar_diasxmes(Tprestamos* vprestamos, int n)
{
    int dias;
    switch (vprestamos[n].fechaprestamo.mes)
    {
    case 1: case 3: case 5: case 7: case 8: case 10: case 12:
        dias = 31; break;
    case 4: case 6: case 9: case 11:
        dias = 30; break;
    case 2:
        if (anio_biciesto_prestamo(vprestamos, n))
            dias = 29;
        else
            dias = 28;
        break;
    }
    return dias;
}
void fecha_devolucion(Tprestamos* vprestamos, int n)
{
    switch (vprestamos[n].tipopubli)
    {
    case 1: case 3: vprestamos[n].fechadevolucion.dia = vprestamos[n].fechaprestamo.dia + 5; break;
    case 2: vprestamos[n].fechadevolucion.dia = vprestamos[n].fechaprestamo.dia + 2; break;
    }
    vprestamos[n].fechadevolucion.mes = vprestamos[n].fechaprestamo.mes;
    vprestamos[n].fechadevolucion.anio = vprestamos[n].fechaprestamo.anio;
    while (vprestamos[n].fechadevolucion.dia > contar_diasxmes(vprestamos, n))
    {
        vprestamos[n].fechadevolucion.dia -= contar_diasxmes(vprestamos, n);
        vprestamos[n].fechadevolucion.mes++;
        if (vprestamos[n].fechadevolucion.mes > 12)
        {
            vprestamos[n].fechadevolucion.mes = 1;
            vprestamos[n].fechadevolucion.anio++;
        }
    }
}

void registrar_publicacion(Tpublicaciones* vpublicaciones, int n)
{
    do
    {
        Console::Clear();
        cout << "Registrar una publicacion:\n\n";
        cout << "Seleccione el tipo de publicacion que desea registrar: \n";
        cout << "1.REVISTAS\n";
        cout << "2.PERIODICOS\n";
        cout << "3.LIBROS\n";
        cin >> vpublicaciones[n].tipo;
    } while (vpublicaciones[n].tipo < 1 || vpublicaciones[n].tipo > 3);
    Console::Clear();
    cout << "Registrar una publicacion:\n\n";
    cout << "Titulo: ";
    cin.ignore();
    getline(cin, vpublicaciones[n].titulo);
    Console::Clear();
    cout << "Registrar una publicacion:\n\n";
    do
    {
        cout << "Codigo (8 caracteres): ";
        cin >> vpublicaciones[n].codigopublica;
        if (vpublicaciones[n].codigopublica.length() != 8)
        {
            cout << "Error, el codigo debe ser de 8 caracteres\n";
        }
        if (existe_publicacion(vpublicaciones, n) != -1)
        {
            cout << "Error, codigo ya existente\n";
        }
    } while ((vpublicaciones[n].codigopublica.length() != 8) || (existe_publicacion(vpublicaciones, n) != -1));
    do
    {
        Console::Clear();
        cout << "Registrar una publicacion:\n\n";
        cout << "Seleccione el local de registro: \n";
        cout << "1.LOS OLIVOS\n";
        cout << "2.SAN JUAN DE LURIGANCHO\n";
        cout << "3.CHORRILLOS\n";
        cin >> vpublicaciones[n].local;
    } while (vpublicaciones[n].tipo < 1 || vpublicaciones[n].tipo > 3);
    vpublicaciones[n].disponible = 1;
    cout << " \n#<<------Publicacion registrada------>>#\n";
    cout << "Presione cualquier tecla para salir\n";
    vpublicaciones++;
}
void registrar_lector(Tlectores* vlectores, int n)
{

    Console::Clear();
    cout << "Registrar Lector:\n\n";
    cout << "Nombres: ";
    cin.ignore();
    getline(cin, vlectores[n].nombre);
    cout << "Apellidos: ";
    getline(cin, vlectores[n].apellido);
    Console::Clear();
    cout << "Registrar Lector:\n\n";
    do
    {
        cout << "Edad (Minimo 12 anios): ";
        cin >> vlectores[n].edad;
        if (vlectores[n].edad < 12)
        {
            cout << "Error, la edad debe ser mayor a 12 para poder registrarse\n";
        }
    } while (vlectores[n].edad < 12);
    Console::Clear();
    cout << "Registrar Lector:\n\n";
    do
    {
        cout << "Sexo (M / F): ";
        cin >> vlectores[n].sexo;
        vlectores[n].sexo = toupper(vlectores[n].sexo);
        if (vlectores[n].sexo != 'M' && vlectores[n].sexo != 'F')
        {
            cout << "Error, sexo invalido\n";
        }
        vlectores[n].sexo = toupper(vlectores[n].sexo);
    } while (vlectores[n].sexo != 'M' && vlectores[n].sexo != 'F');
    cin.ignore();
    Console::Clear();
    cout << "Registrar Lector:\n\n";
    do
    {
        cout << "Ingrese numero de celular(9 digitos): ";
        cin >> vlectores[n].celular;
        if (vlectores[n].celular.length() != 9)
        {
            cout << "Error, el numero debe tener 9 digitos\n";
        }
        if (existe_lector(vlectores, n) != -1)
        {
            cout << "Error, numero de celular ya utilizado\n";
        }
    } while ((vlectores[n].celular.length() != 9) || (existe_lector(vlectores, n) != -1));
    Console::Clear();
    cout << "Registrar Lector\n\n";
    do
    {
        cout << "Ingrese DNI del lector  (8 digitos): ";
        cin >> vlectores[n].dni;
        if (vlectores[n].dni.length() != 8)
        {
            cout << "Error, el dni debe tener 8 digitos\n";
        }
        if (existe_lector(vlectores, n) != -1)
        {
            cout << "Error, numero de DNI ya utilizado\n";
        }
    } while ((vlectores[n].dni.length() != 8) || (existe_lector(vlectores, n) != -1));
    Console::Clear();
    cin.ignore();
    cout << "Registrar Lector:\n\n";
    cout << "Direccion:\n";
    cout << "  Calle: ";
    cin.ignore();
    getline(cin, vlectores[n].direccion.calle);
    cout << "  Distrito: ";
    getline(cin, vlectores[n].direccion.distrito);
    cout << "  Ciudad: ";
    getline(cin, vlectores[n].direccion.ciudad);
    cout << "  Numero de vivienda: ";
    cin >> vlectores[n].direccion.numero;
    Console::Clear();
    cout << "--------#<< Lector registrado >>#--------\n";
    cout << "Presione cualquier tecla para salir\n";
    vlectores++;
    _getch();
}
void registrar_prestamo(Tprestamos* vprestamos, int n, Tlectores* vlectores, Tpublicaciones* vpublicaciones, int npublicaciones)
{
    do
    {
        cout << "Ingrese DNI del lector (8 digitos): ";
        cin >> vprestamos[n].dnilector;
        if (lector_registrado(vlectores, vprestamos, n) == -1)
        {
            cout << "Error, DNI aun no ha sido registrado\n";
        }
    } while ((vlectores[n].dni.length() != 8) && (lector_registrado(vlectores, vprestamos, n) == -1));
    Console::Clear();
    cout << "Registrar prestamo\n\n";
    do
    {
        Console::Clear();
        cout << "Registrar p restamo\n\n";
        cout << "Elegir tipo de publicacion:\n";
        cout << "1.REVISTA\n2.PERIODICO\n3.LIBRO\n";
        cin.ignore();
        cin >> vprestamos[n].tipopubli;
    } while (vprestamos[n].tipopubli < 1 || vprestamos[n].tipopubli > 3);
    Console::Clear();
    cout << "Registrar prestamo\n\n";
    mostrar_publicaciones_disponibles(vpublicaciones, vprestamos, npublicaciones, n);
    do
    {
        cout << "Ingrese codigo de la publicacion (8 caracteres): ";
        cin >> vprestamos[n].codigopubli;
        if (vprestamos[n].codigopubli.length() != 8)
        {
            cout << "Error, el codigo debe contener 8 caracteres";
        }
        if (publicacion_disponible(vpublicaciones, vprestamos, n, npublicaciones) == -1)
        {
            cout << "Error, publicacion no disponible";
        }
    } while ((vprestamos[n].codigopubli.length() != 8) || (publicacion_disponible(vpublicaciones, vprestamos, n, npublicaciones) == -1));
    publicacion_prestar(vpublicaciones, vprestamos, n, npublicaciones);
    Console::Clear();
    Tdias fechaprestamo;
    do
    {
        cout << "Registrar prestamo\n\n";
        cout << "Ingrese fecha de prestamo (Dia-Mes-Anio)\n";
        cin >> vprestamos[n].fechaprestamo.dia >> vprestamos[n].fechaprestamo.mes >> vprestamos[n].fechaprestamo.anio;
        fechaprestamo.dia = vprestamos[n].fechaprestamo.dia;
        fechaprestamo.mes = vprestamos[n].fechaprestamo.mes;
        fechaprestamo.anio = vprestamos[n].fechaprestamo.anio;
        if (fecha_valida_actual(fechaprestamo) == -1)
        {
            cout << "Fecha invalida, intente de nuevo." << endl;
        }
    } while (fecha_valida_actual(fechaprestamo) == -1);
    fecha_devolucion(vprestamos, n);
    cout << endl << " #<<------Prestamo registrado----->>#\n";
    cout << "\n-------------------------------------------\n\nCOMPROBANTE DE PRESTAMO\n";
    cout << "-----------------------------\n";
    cout << "DNI: " << vprestamos[n].dnilector << endl;
    cout << "Codigo de publicacion: " << vprestamos[n].codigopubli << endl;
    cout << "Fecha de prestamo: " << vprestamos[n].fechaprestamo.dia << "-" << vprestamos[n].fechaprestamo.mes << "-" << vprestamos[n].fechaprestamo.anio << endl;
    cout << "Fecha de devolucion: " << vprestamos[n].fechadevolucion.dia << "-" << vprestamos[n].fechadevolucion.mes << "-" << vprestamos[n].fechadevolucion.anio << endl;
    vprestamos++;

    cout << "\nPresione cualquier tecla para salir\n";
}
void registrar_devolucion(Tdevoluciones* vdevolucion, int n, Tprestamos* vprestamos, int nprestamos, Tpublicaciones* vpublicaciones, int npublicaciones, Tlectores* vlectores, int nlectores)
{
    Console::Clear();
    do
    {
        cout << "Registrar devolucion\n\n";
        cout << "Ingrese DNI del lector: ";
        cin >> vdevolucion[n].dnilector;
    } while (vdevolucion[n].dnilector.length() != 8);
    do
    {
        Console::Clear();
        cout << "Registrar devolucion\n\n";
        cout << "Ingrese codigo de la publicacion: ";
        cin >> vdevolucion[n].codigopubli;
    } while (vdevolucion[n].codigopubli.length() != 8);
    Console::Clear();
    cin.ignore();
    cout << "ingrese el nombre del recurso prestado:";
    getline(cin, vpublicaciones[n].titulo);
    cout << "Ingrese fecha de devolucion (dia-mes-anio): \n";
    cin >> vdevolucion[n].fechadevolucion.dia >> vdevolucion[n].fechadevolucion.mes >> vdevolucion[n].fechadevolucion.anio;
    observacion_devolucion_fuera_de_fecha(vprestamos, nprestamos, vdevolucion, n);
    for (int i = 0; i < npublicaciones; i++)
    {
        if (vdevolucion[n].codigopubli == vpublicaciones[i].codigopublica)
        {
            vpublicaciones[i].disponible = 1;
        }
    }

    cout << endl << " #<<----Devolucion exitosa----->>#\n";
    cout << "Presione cualquier tecla para salir\n";
    vdevolucion++;
}

void mostrar_publicaciones(Tpublicaciones* vpublicaciones, int n, Tprestamos* vprestamos, Tdevoluciones* vdevoluciones)
{
    string tipos[3] = { "REVISTA", "PERIODICO", "LIBRO" };
    string locales[3] = { "LOS OLIVOS", "SAN JUAN DE LURIGANCHO", "CHORRILLOS" };
    string disponibles[2] = { "SI", "NO" };
    Console::Clear();
    cout << "===========PUBLICACIONES REGISTRADOS=====================" << endl;
    for (int i = 0; i < n; i++)
    {
        cout << "\nPublicacion " << i + 1 << ":\n" << endl;
        cout << "Tipo:\t\t" << tipos[vpublicaciones[i].tipo - 1] << endl;
        cout << "Local:\t\t" << locales[vpublicaciones[i].local - 1] << endl;
        cout << "Codigo :\t" << vpublicaciones[i].codigopublica << endl;
        cout << "Titulo:\t\t" << vpublicaciones[i].titulo << endl;
        cout << "Disponibilidad: \t" << disponibles[vpublicaciones[i].disponible - 1] << endl;
        cout << "\n---------------------------------------------\n";
    }
    cout << "\nPresione cualquier tecla para salir\n";
}
void mostrar_lectores(Tlectores* vlectores, int n, int nlectores)
{
    Console::Clear();
    cout << "=========== LECTORES REGISTRADOS ============\n";

    for (int i = 0; i < n; i++) {
        cout << "Lector " << i + 1 << ":\n\n";
        cout << "Sexo: " << vlectores[i].sexo << "\n"
            << "Edad: " << vlectores[i].edad << "\n"
            << "Nombre: " << vlectores[i].nombre << "\n"
            << "Apellido: " << vlectores[i].apellido << "\n"
            << "Celular: " << vlectores[i].celular << "\n"
            << "DNI: " << vlectores[i].dni << "\n"
            << "Calle: " << vlectores[i].direccion.calle << "\n"
            << "N mero de Vivienda: " << vlectores[i].direccion.numero << "\n"
            << "Ciudad: " << vlectores[i].direccion.ciudad << "\n"
            << "Distrito: " << vlectores[i].direccion.distrito << "\n";
        cout << "---------------------------------------------\n";
    }
    cout << "\nPresione cualquier tecla para salir\n" << endl;
  
    _getch();
}
void mostrar_prestamos(Tprestamos* vprestamos, int n, Tdevoluciones* vdevoluciones)
{
    string tiposp[3] = { "REVISTA  ", "PERIODICO", "LIBRO    " };
    Console::Clear();
    cout << "\n===========PRESTAMOS REGISTRADOS=====================\n" << endl;

    cout << "Codigo Publi\tDNI Lector\t\tTipo Publi\tFecha Prestamo\tFecha limite de devolucion" << endl;
    cout << "--------------------------------------------------------------------------------------------------" << endl;
    for (int i = 0; i < n; i++)
    {
        cout << vprestamos[i].codigopubli << "\t"
            << vprestamos[i].dnilector << "\t\t"
            << tiposp[vprestamos[i].tipopubli - 1] << "\t"
            << vprestamos[i].fechaprestamo.dia << "/"
            << vprestamos[i].fechaprestamo.mes << "/"
            << vprestamos[i].fechaprestamo.anio << "\t";
        fecha_devolucion(vprestamos, i);

        cout << vprestamos[i].fechadevolucion.dia << "/"
             << vprestamos[i].fechadevolucion.mes << "/"
             << vprestamos[i].fechadevolucion.anio << endl;
    }
    cout << "\nPresione cualquier tecla para salir\n";
}
void mostrar_devoluciones(Tdevoluciones* vdevoluciones, int n, Tpublicaciones* vpublicaciones, int npublicaciones)
{
    Console::Clear();
    cout << "===========DEVOLUCIONES REGISTRADAS=====================" << endl;

    cout << "DNI\t\tCodigo de la publicacion\tTitulo\t\t\t\tFecha de devolucion\n";
    for (int i = 0; i < n; i++)
    {
        cout << vdevoluciones[i].dnilector << "\t"
            << vdevoluciones[i].codigopubli << "\t\t\t";
        for (int j = 0; j < npublicaciones; j++)
        {
            if (vdevoluciones[i].codigopubli == vpublicaciones[j].codigopublica)
                cout << vpublicaciones[j].titulo << "\t\t";
        }
        cout << vpublicaciones[n].titulo << "-";
        cout << vdevoluciones[i].fechadevolucion.dia << "-"
            << vdevoluciones[i].fechadevolucion.mes << "-"
            << vdevoluciones[i].fechadevolucion.anio << "\n";

    }
    cout << "\nPresione cualquier tecla para salir\n";
}
void reporte_1(Tprestamos* vprestamos, int n, Tdias fechaactual, Tpublicaciones* vpublicaciones, int npublicaciones)
{
    Console::Clear();
    string tiposp[3] = { "REVISTA  ", "PERIODICO", "LIBRO    " };
    do
    {
        cout << "Reporte 1\n\n";
        cout << "Ingrese fecha actual (Dia-Mes-Anio)\n";
        cin >> fechaactual.dia >> fechaactual.mes >> fechaactual.anio;
        if (fecha_valida_actual(fechaactual) == -1)
        {
            cout << "Fecha invalida, intente de nuevo." << endl;
        }
    } while (fecha_valida_actual(fechaactual) == -1);
    Console::Clear();
    cout << "\nListado de devoluciones pendientes fuera de fecha\n";
    cout << "\n-------------------------------------\n";

    for (int i = 0; i < n; i++)
    {
        if (devolucion_fuera_de_fecha(fechaactual, vprestamos, i) == 2)
        {
            cout << "Codigo: " << vprestamos[i].codigopubli << "\n";
            cout << "DNI: " << vprestamos[i].dnilector << "\n";
            cout << "Tipo: " << tiposp[vprestamos[i].tipopubli - 1] << "\n";
            for (int j = 0; j < npublicaciones; j++)
            {
                if (vprestamos[i].codigopubli == vpublicaciones[j].codigopublica)
                    cout << "Titulo: " << vpublicaciones[j].titulo << endl;
            }
            cout << "\n-------------------------------------\n";
        }
    }
}
void reporte_lectores_por_edad(Tlectores* vlectores, Tprestamos* vprestamos, int nprestamos, int nlectores)
{
    string tipos[3] = { "REVISTAS", "PERIODICOS", "LIBROS" };
    int edad_12_18 = 0;
    int edad_18_30 = 0;
    int edad_30_60 = 0;
    int edad_60_mas = 0;
    int tipodepublicacion;
    do
    {
        Console::Clear();
        cout << "Elegir tipo de publicacion:\n";
        cout << "1.REVISTA\n2.PERIODICO\n3.LIBRO\n";
        cin.ignore();
        cin >> tipodepublicacion;
    } while (tipodepublicacion < 1 || tipodepublicacion > 3);

    for (int i = 0; i < nprestamos; i++)
    {
        if (vprestamos[i].tipopubli == tipodepublicacion) //contador de revistas 
        {
            for (int j = 0; j < nlectores; j++)
            {
                if (vlectores[j].dni == vprestamos[i].dnilector)
                {
                    if (vlectores[j].edad < 19)
                    {
                        edad_12_18++;
                    }
                    else
                    {
                        if (vlectores[j].edad < 31)
                        {
                            edad_18_30++;
                        }
                        else
                            if (vlectores[j].edad < 61)
                            {
                                edad_30_60++;
                            }
                            else
                            {
                                edad_60_mas++;
                            }
                    }
                }
            }
        }
    }
    cout << "\nReporte de Lectores por Rango de Edad para el tipo de publicaci n: \n" << tipos[tipodepublicacion = 1] << "':\n";
    cout << "12 - 18 anios: " << edad_12_18 << endl;
    for (int i = 0; i < edad_12_18; i++)
    {
        cout << "#";
    }
    cout << "(" << edad_12_18 << ")" << endl << endl;
    cout << "18 - 30 anios: " << edad_18_30 << endl;
    for (int i = 0; i < edad_18_30; i++)
    {
        cout << "#";
    }
    cout << "(" << edad_18_30 << ")" << endl << endl;
    cout << "30 - 60 anios: " << edad_30_60 << endl;
    for (int i = 0; i < edad_30_60; i++)
    {
        cout << "#";
    }
    cout << "(" << edad_30_60 << ")" << endl;
    cout << "Mas de 60 anios " << edad_60_mas << endl << endl;
    for (int i = 0; i < edad_60_mas; i++)
    {
        cout << "#";
    }
    cout << "(" << edad_60_mas << ")" << endl << endl;
    
}
 
void main()
{
    int opcion,n, nlectores = 4, npublicaciones = 3, nprestamos = 4, ndevoluciones = 2;
    char reset;
    Random r;
    Tlectores* vlectores;
    Tpublicaciones* vpublicaciones;
    Tprestamos* vprestamos;
    Tdevoluciones* vdevoluciones;
    Tdias fechaactual;
    vlectores = new Tlectores[100];
    vpublicaciones = new Tpublicaciones[100];
    vprestamos = new Tprestamos[100];
    vdevoluciones = new Tdevoluciones[100];
    publicaciones_x_defecto(vpublicaciones);
    lectores_x_defecto(vlectores);
    prestamos_x_defecto(vprestamos);
    devoluciones_x_defecto(vdevoluciones);
    do
    {
        menu_principal();
        cin >> opcion;
        switch (opcion)
        {
        case 1:
            submenu_registrar(opcion);
            cin >> opcion;
            switch (opcion)
            {
            case 1: registrar_publicacion(vpublicaciones, npublicaciones); npublicaciones++; break;
            case 2: registrar_lector(vlectores, nlectores); nlectores++;  break;
            case 3: registrar_prestamo(vprestamos, nprestamos, vlectores, vpublicaciones, npublicaciones); nprestamos++; break;
            case 4: registrar_devolucion(vdevoluciones, ndevoluciones, vprestamos, nprestamos, vpublicaciones, npublicaciones, vlectores, nlectores); ndevoluciones++; break;
            case 5: salir(); break;
            }
            break;
        case 2:
            submenu_reportes(opcion);
            cin >> opcion;
            switch (opcion)
            {
            case 1: mostrar_publicaciones(vpublicaciones, npublicaciones, vprestamos, vdevoluciones); break;
            case 2: mostrar_lectores(vlectores, nlectores,n); break;
            case 3: mostrar_prestamos(vprestamos, nprestamos, vdevoluciones); break;
            case 4: mostrar_devoluciones(vdevoluciones, ndevoluciones, vpublicaciones, npublicaciones); break;
            case 5: reporte_1(vprestamos, nprestamos, fechaactual, vpublicaciones, npublicaciones); break;
            case 6: reporte_lectores_por_edad(vlectores, vprestamos, nprestamos, nlectores); break;
            case 7: contar_por_tipo(vpublicaciones, n);
            case 8: salir(); break;
            }
            break;
        case 3: presentacion(); break;
        case 4: salir(); break;
        }
        reset = _getch();
    } while (reset != 0);
}

# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import PhotoImage
from os import path
import sqlite3
from datetime import datetime, date
from tkinter import font
from typing import Optional, Union

"""==============================================================
CRUD Programación Orientada a Objetos
Universidad Nacional de Colombia - 2024-1S
Repo: https://github.com/juan2005elpapu/CRUD-POO-4.4

Integrantes:
  - Juan David Peña                     (jupenalo@unal.edu.co)
  - Juan Sebastián Ramirez Villalobos   (juaramirezv@unal.edu.co)
  - Jesús David Sánchez Cobos           (jesanchezco@unal.edu.co)
  - Juan Camilo Vergara Tao             (juvergarat@unal.edu.co)
    =============================================================="""

class Inscripciones_2:
    def __init__(self, master=None) -> None:
        #Dirección programa
        self.dir_pro = path.dirname(__file__)
        self.db_name = 'Inscripciones.db'
        
        """Ventana principal"""
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd", height=600, width=800)
        alto=600
        ancho=800
        self.win.geometry(str(ancho)+"x"+str(alto))
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="@Adobe Heiti Std R", size=9)
        self.win.option_add("*Font", default_font)
        #Centrar Ventana
        x = self.win.winfo_screenwidth()
        y = self.win.winfo_screenheight()
        self.win.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
        self.win.resizable(False, False)
        self.win.title("Inscripción de Cursos")
        ruta_Icon = self.dir_pro + "\\img\\icon.ico"
        self.win.iconbitmap(bitmap=ruta_Icon)
        #Crea el frame
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        self.estilo_labels = ttk.Style()
        self.estilo_labels.configure("Labels", font="Arial Narrow 11")
        #Label No. Inscripción
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}", justify="center",state="normal", takefocus=False,text='No. Inscripción')
        #Combobox No. Inscripción
        self.cmbx_No_Inscripcion = ttk.Combobox(self.frm_1, name="cmbxnoincripcion", state="readonly")
        self.cmbx_No_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        self.actualizacion_Numeros_Inscripcion()
        self.cmbx_No_Inscripcion.bind("<<ComboboxSelected>>", lambda _:self.crear_Treeview("No_Inscripcion"))
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha")
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        self.fecha.bind("<BackSpace>", lambda _:self.fecha.delete(0,"end"))
        self.fecha.bind("<KeyRelease>", self.valida_Fecha)
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno", state="readonly")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=90, y=80)
        self.ids_Alumnos = self.correr_Query("SELECT Id_Alumno FROM Alumnos")
        self.lista_Ids_Alumnos = []
        for tupla in self.ids_Alumnos:
            self.lista_Ids_Alumnos.append(tupla[0])
        self.cmbx_Id_Alumno['values'] = self.ids_Alumnos
        # Adición automática de nombres y apellidos al seleccionar un ID
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.cambiar_Nombre_Completo)
        #Label Nombres
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)
        #Entry Nombres
        self.nombres = ttk.Entry(self.frm_1, name="nombres")
        self.nombres.place(anchor="nw", width=200, x=90, y=130)
        self.nombres.configure(state = "readonly")
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos")
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)
        self.apellidos.configure(state = "readonly")
        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=185)
        #Combobox Curso
        self.cmbx_Id_Curso = ttk.Combobox(self.frm_1, name="cmbx_id_curso", state="readonly")
        self.cmbx_Id_Curso.place(anchor="nw", width=100, x=90, y=185)
        self.ids_Cursos = self.correr_Query("SELECT Código_Curso FROM Cursos")
        self.lista_Ids_Cursos = []
        for tupla in self.ids_Cursos:
            self.lista_Ids_Cursos.append(tupla[0])
        self.cmbx_Id_Curso['values'] = self.ids_Cursos
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.cambiar_Curso)
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=200, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso", state = "readonly")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=250, x=240, y=185)
        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="labelhora")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Horario:')
        self.lblHorario.place(anchor="nw", x=500, y=185)
        #Entrys del Horario
        self.cmbx_Dias = ttk.Combobox(self.frm_1, name="cmbx_Dias", state="readonly")
        self.cmbx_Dias.configure(justify="left", width=166)
        self.cmbx_Dias.place(anchor="nw", width=110, x=550, y=185)
        self.cmbx_Horario = ttk.Combobox(self.frm_1, name="hora", state="readonly")
        self.cmbx_Horario.configure(justify="left", width=166)
        self.cmbx_Horario.place(anchor="nw", width=110, x=670, y=185)
        self.horarios_Dias = ["lun. y miérc.", "mar. y juev."]
        self.cmbx_Dias['values'] = self.horarios_Dias
        self.horarios_Horas = ["7:00 - 9:00", "9:00 - 11:00", "11:00 - 13:00", "14:00 - 16:00", "16:00 - 18:00"]
        self.cmbx_Horario['values'] = self.horarios_Horas
        
        """Botones  de la interfaz"""
        #Estilo botones
        self.estilo_botones = ttk.Style()
        self.estilo_botones.configure("TButton")
        self.estilo_botones.map("TButton", foreground=[("active", "purple")], background=[("active", "purple")])
        self.estilo_boton_can_el = ttk.Style()
        self.estilo_boton_can_el.configure("Can_El.TButton")
        self.estilo_boton_can_el.map("Can_El.TButton", foreground=[("active", "red")], background=[("active", "red")])  
        #Botón Consultar
        ruta_Lupa  = self.dir_pro + "\\img\\lupa.png"
        self.img = PhotoImage(file=ruta_Lupa)
        self.btnConsultar = ttk.Button(self.frm_1, name="btnconsultar", image=self.img)
        self.btnConsultar.place(anchor="nw", x=20, y=15)
        self.btnConsultar.bind("<1>", self.accion_Consultar)
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=260)
        self.btnGuardar.bind("<1>", lambda _:self.accion_Boton('G'))
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)
        self.btnEditar.bind("<1>", lambda _:self.accion_Boton('Ed'))
        self.id = -1 # Bandera para saber si el programa está guardando (INSERT) o editando (UPDATE)
        self.curso_Anterior = "" # Variable para guardar el curso original al oprimir el botón Editar
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar', style="Can_El.TButton")
        self.btnEliminar.place(anchor="nw", x=400, y=260)
        self.btnEliminar.bind("<1>", lambda _:self.accion_Boton('El'))
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar', style="Can_El.TButton")
        self.btnCancelar.place(anchor="nw", x=500, y=260)
        self.btnCancelar.bind("<1>", lambda _:self.accion_Boton('C'))
        #Separador
        separador1 = ttk.Separator(self.frm_1)
        separador1.configure(orient="horizontal")
        separador1.place(anchor="nw", width=796, x=2, y=245)

        """Treeview inicial de la Aplicación"""
        self.crear_Treeview("Inscritos")

        """Main widget"""
        self.mainwindow = self.win

        '''Ventana información'''
        self.ventana_info = tk.Toplevel()
        self.ventana_info.configure(background="#f7f9fd", height=400, width=400)
        alto=400
        ancho=400
        self.ventana_info.geometry(str(ancho)+"x"+str(alto))
        #Centrar Ventana
        x = self.ventana_info.winfo_screenwidth()
        y = self.ventana_info.winfo_screenheight()
        self.ventana_info.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
        self.ventana_info.resizable(False, False)
        self.ventana_info.title("Información inicial")
        ruta_Icon = self.dir_pro + "\\img\\icon.ico"
        self.ventana_info.iconbitmap(bitmap=ruta_Icon)
        #Crea el frame
        #self.frm_3 = tk.Frame(self.ventana_info, name="frm_3")
        #self.frm_3.configure(background="#f7f9fd", height=400, width=400)
        #Label titulo ventana info
        self.lblInfo = ttk.Label(self.ventana_info, name="lblinfo") 
        self.lblInfo.configure(background="#f7f9fd", text='Proyecto POO 2024 - 2')
        self.lblInfo.place(anchor="c", relx=0.5, y=25)
 
        self.textInfo = tk.Text(self.ventana_info, name="textInfo", height = 5, width = 52) 
        self.informacion = """La Segunda Guerra Mundial (también escrito II Guerra Mundial)1​ fue un conflicto militar global que se desarrolló entre 1939 y 1945. 
        En ella se vieron implicadas la mayor parte de las naciones del mundo —incluidas todas las grandes potencias, así como prácticamente todas las naciones europeas— agrupadas en dos alianzas militares enfrentadas: los Aliados, por un lado, y las Potencias del Eje, por otro. Fue la mayor contienda bélica en la historia de la humanidad, con más de 100 millones de militares movilizados y un estado de guerra total en que los grandes contendientes destinaron"""
        self.textInfo.insert(tk.END, self.informacion)
        self.textInfo.place(anchor="c", relx=0.5, y=100)
        self.textInfo.configure(background="#f7f9fd", borderwidth=0, state="disabled")

    def run(self) -> None:
        self.mainwindow.mainloop()    

    """========== Funciones para validar información =========="""
    def registro_Existente(self, id_Alumno : str, codigo_Curso : str) -> bool:
        """
        Verifica si el registro de un estudiante en un curso ya existe.

            Parámetros:
                id_Alumno (str): El ID del Alumno
                codigo_Curso (str) : El código del curso

            Devoluciones: 
                (bool): True si el registro ya existe en la tabla Inscritos; False de lo contrario
        """
        query = f"SELECT COUNT(*) FROM Inscritos WHERE Id_Alumno = '{id_Alumno}' AND Código_Curso = '{codigo_Curso}'"
        resultado = self.correr_Query(query)
        contador = resultado[0][0]
        return contador > 0
    
    def horario_Existente(self, alumno : str, dias : str, horario : str) -> bool:
        """
        Verifica si un estudiante ya tiene un curso registrado en el horario especificado.

            Parámetros:
                alumno (str): El ID del alumno
                dias (str): El horario del alumno (los días)
                horario (str): El horario del alumno (las horas)
            
            Devoluciones:
                (bool): True si el estudiante ya tiene un curso registrado en dicho horario; False de lo contrario
        """
        query = f"SELECT COUNT(*) FROM Inscritos WHERE Id_Alumno = '{alumno}' AND Horario = '{dias} {horario}'"
        resultado = self.correr_Query(query)
        contador = resultado[0][0]
        return contador > 0
    
    def inscrito_Existente(self, id_Alumno : str) -> Optional[int]:
        """
        Verifica si un estudiante ya tiene un número de inscripción asociado.

            Parámetros:
                id_Alumno (str): El ID del alumno
            
            Devoluciones:
                numero_Inscripcion (int): El número de inscripción asociado (si existe)
                None: Si el estudiante no ha sido registrado previamente
        """
        query = f"SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = '{id_Alumno}'"
        resultado = self.correr_Query(query)
        if len(resultado) > 0:
            numero_Inscripcion = resultado[0][0]
            return numero_Inscripcion
        else:
            return None
    
    def valida_Fecha(self, event=None) -> None:
        """
        Verifica que la fecha ingresada en el entry de fecha de la ventana principal esté bien escrita.

            Parámetros:
                (event): Evento (opcional)
            
            Devoluciones:
                None
        """
        if event.char.isdigit() or event.char == "" or event.keysym == "Return":
            fecha_Ingresada = self.fecha.get()
            if len(fecha_Ingresada) > 10:
                messagebox.showerror(message="Máximo 10 digitos", title="Error al ingresar fecha")
                self.fecha.delete(10, "end")
            num_char = 0
            for i in fecha_Ingresada:
                num_char += 1
            if num_char == 2: self.fecha.insert(2, "/")
            if num_char  == 5: self.fecha.insert(6, "/")
        else:
            self.fecha.delete(len(self.fecha.get())-1, "end")
            messagebox.showerror(message="Solo numeros", title="Fecha Erronea")

    def fecha_Valida(self, fecha : str) -> bool:
        """
        Verifica que la fecha ingresada sea válida.

            Parámetros:
                fecha (str): La fecha a verificar

            Devoluciones:
                (bool): True si la fecha es válida; False de lo contrario
        """
        try: 
            dia, mes, anio = map(int, fecha.split('/'))
            datetime(anio, mes, dia)
            return True
        except ValueError: 
            messagebox.showerror('Error!!','.. ¡Fecha equivocada! por favor corrijala ..')
            return False   

    def verificar_Entradas(self) -> bool:
        """
        Verifica si las entradas necesarias para registrar un estudiante en un curso están completas. Adicionalmente verifica que la fecha sea válida, si el estudiante ya fue registrado en ese curso y si el estudiante no tiene otro curso en el mismo horario (días y horas).
        
            Parámetros:
                None

            Devoluciones:
                (bool): False si alguna de las entradas necesarias está vacía o si alguna de las condiciones mencionadas anteriormente no se cumple; True de lo contrario
        """
        # Verifica que todos los campos estén llenos
        entradas_A_Revisar = [self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get(), self.fecha.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()]
        for entrada in entradas_A_Revisar:
            if entrada == "":
                self.mostrar_Error_Entradas_Vacias()
                return False
        # Verifica que la fecha sea válida, que el estudiante no haya sido inscrito en ese curso anteriormente y que no haya sido inscrito en otro curso con el mismo horario
        if not self.fecha_Valida(self.fecha.get()) or self.registro_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()) or self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
            return False
        return True

    def mostrar_Error_Entradas_Vacias(self) -> None:
        """
        Muestra un mensaje de error indicando las entradas que necesitan ser completadas para guardar correctamente.

            Parámetros:
                None
        
            Devoluciones:
                None
        """
        entradas = {"Id Alumno":self.cmbx_Id_Alumno.get(), "Id Curso":self.cmbx_Id_Curso.get(), "Fecha":self.fecha.get(), "Horario (Días)":self.cmbx_Dias.get(), "Horario (Hora)":self.cmbx_Horario.get()}
        entradas_Vacias = []
        for i in range(len(entradas)):
            if list(entradas.values())[i] == "":
                entradas_Vacias.append(list(entradas.keys())[i])
        mensaje = "Faltan campos por llenar: " + ", ".join(entradas_Vacias)
        messagebox.askretrycancel(title="Error al guardar", message=mensaje)

    """========== Funciones para el manejo de la base de datos =========="""
    def correr_Query(self, query : str, parametros: tuple=()) -> list[tuple]:
        """
        Ejecuta la consulta SQL dada con parámetros opcionaes y retorna el resultado.

            Parámetros:
                query (str): La consulta SQL a ejecutar
                parametros (tuple): Los parámetros de la consulta SQL (opcional)

            Devoluciones:
                resultado (list[tuple]): El resultado de la ejecución de la consulta
        """
        ruta_db = self.dir_pro + "\\db\\Inscripciones.db"
        with sqlite3.connect(ruta_db) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado.fetchall()

    def cambiar_Nombre_Completo(self, event=None) -> None:
        """
        Obtiene el nombre completo del estudiante a partir de su ID y actualiza la información en las entradas correspondientes de la interfaz.

            Parámetros:
                (event): Evento (opcional)

            Devoluciones:
                None
        """
        id_Alumno = self.cmbx_Id_Alumno.get()
        nombres_Alumno = self.correr_Query(f"SELECT Nombres FROM Alumnos WHERE Id_Alumno = '{id_Alumno}'")
        apellidos_Alumno = self.correr_Query(f"SELECT Apellidos FROM Alumnos WHERE Id_Alumno = '{id_Alumno}'")
        self.nombres.configure(state = "normal")
        self.apellidos.configure(state = "normal")
        self.nombres.delete(0, 'end')
        self.apellidos.delete(0, 'end')
        self.nombres.insert(0, nombres_Alumno[0][0])
        self.apellidos.insert(0, apellidos_Alumno[0][0])
        self.nombres.configure(state = "readonly")
        self.apellidos.configure(state = "readonly")

        numero_Inscripcion = self.inscrito_Existente(id_Alumno)
        if numero_Inscripcion == None :
            self.cmbx_No_Inscripcion.configure(state="readonly")
            self.cmbx_No_Inscripcion.set("")
        else :
            self.cmbx_No_Inscripcion.current(self.lista_No_Inscripcion.index(numero_Inscripcion))
            self.cmbx_No_Inscripcion.configure(state="disabled")

    def cambiar_Curso(self, event=None) -> None:
        """
        Obtiene el nombre del curso a partir de su código y actualiza la información en las entradas correspondientes de la interfaz.

            Parámetros:
                (event): Evento (opcional)
        
            Devoluciones:
                None
        """
        codigo_Curso = self.cmbx_Id_Curso.get()
        descripcion = self.correr_Query(f"SELECT Descrip_Curso FROM Cursos WHERE Código_Curso = '{codigo_Curso}'")
        self.descripc_Curso.configure(state = "normal")
        self.descripc_Curso.delete(0, 'end')
        self.descripc_Curso.insert(0, descripcion[0][0])
        self.descripc_Curso.configure(state = "readonly")

    def insertar_Informacion(self, num_Inscripcion : int, codigo_Curso : str) -> None:
        """
        Inserta la información del registro a partir del no. de inscripción y el código del curso en las entradas correspondientes de la interfaz.

            Parámetros:
                num_Inscripcion (int): El número de inscripción del registro
                codigo_Curso (str): El código del curso del registro
            
            Devoluciones:
                None
        """
        query= f"SELECT * FROM Inscritos WHERE No_Inscripción = {num_Inscripcion} AND Código_Curso = '{codigo_Curso}'"
        resultado = self.correr_Query(query)
        resultado = list(resultado[0])

        # Cambia valor en Fecha
        fecha = resultado[2].split("-")
        fecha_Nueva = str(fecha[2])+'/'+str(fecha[1])+'/'+str(fecha[0])
        self.fecha.configure(state="normal")
        self.fecha.delete(0, "end")
        self.fecha.insert(0,fecha_Nueva)
        resultado.pop(2)
        
        # Cambia valor en No. de Inscripción
        self.cmbx_No_Inscripcion.current(self.lista_No_Inscripcion.index(num_Inscripcion))
        self.cmbx_No_Inscripcion.configure(state="disable")

        # Cambia valor en las demás entradas
        horario=resultado[3].split(" ")
        dia = " ".join(horario[:3])
        hora = " ".join(horario[3:])
        resultado[3]=dia
        resultado.append(hora)
        entradas = [self.cmbx_Id_Alumno, self.cmbx_Id_Curso, self.cmbx_Dias, self.cmbx_Horario]
        listas = [self.lista_Ids_Alumnos, self.lista_Ids_Cursos, self.horarios_Dias, self.horarios_Horas]
        try:
            for i in range(len(entradas)):
                entradas[i].current(listas[i].index(resultado[i+1]))
            self.cambiar_Curso()
        except:
            pass
        self.cambiar_Nombre_Completo()
        
    def insertar_Estudiante(self, no_Inscripcion : int) -> None:
        """
        Inserta información del estudiante a partir del no. de inscripción en las entradas correspondientes de la interfaz.

            Parámetros:
                no_Inscripcion (int): El número de inscripción del estudiante
            
            Devoluciones:
                None
        """
        query = f"SELECT Id_Alumno FROM Inscritos WHERE No_Inscripción = {no_Inscripcion}"
        resultado = self.correr_Query(query)
        id_Alumno = resultado[0][0]
        self.cmbx_Id_Alumno.current(self.lista_Ids_Alumnos.index(id_Alumno))
        self.cmbx_Id_Alumno.configure(state="disable")
        self.cambiar_Nombre_Completo()

    def limpiar_Entradas(self, opcion : str) -> None:
        """
        Limpia las entradas de la interfaz de acuerdo a diferentes casos.

            Parámetros:
                opcion (str): El caso para limpiar las entradas (["datos_Alumno", "datos_Curso", "datos_Todo", "restaurar_Botones"])
            
            Devoluciones:
                None
        """
        match opcion:
            case "datos_Alumno":
                self.cmbx_Id_Alumno.set("")
                self.nombres.configure(state = "normal")
                self.apellidos.configure(state = "normal")
                self.nombres.delete(0, "end")
                self.apellidos.delete(0, "end")
                self.nombres.configure(state = "readonly")
                self.apellidos.configure(state = "readonly")
                self.cmbx_Id_Alumno.configure(state="readonly")
            case "datos_Curso":
                self.cmbx_Id_Curso.set("")
                self.descripc_Curso.configure(state = "normal")
                self.descripc_Curso.delete(0, "end")
                self.descripc_Curso.configure(state = "readonly")
                self.cmbx_Horario.set("")
                self.cmbx_Dias.set("")
            case "datos_Todo":
                self.cmbx_Id_Alumno.set("")
                self.cmbx_Id_Curso.set("")
                self.nombres.configure(state = "normal")
                self.apellidos.configure(state = "normal")
                self.descripc_Curso.configure(state = "normal")
                self.nombres.delete(0, "end")
                self.apellidos.delete(0, "end")
                self.descripc_Curso.delete(0, "end")
                self.cmbx_Id_Alumno.configure(state="readonly")
                self.nombres.configure(state = "readonly")
                self.apellidos.configure(state = "readonly")
                self.descripc_Curso.configure(state = "readonly")
                self.cmbx_Horario.set("")
                self.cmbx_Dias.set("")
                self.cmbx_No_Inscripcion.set("")
                self.fecha.delete(0, "end")
            case "restaurar_Botones":
                # Restaura los botones Eliminar, Guardar y Editar
                self.btnEliminar.configure(state='normal')
                self.btnEliminar.bind("<1>", lambda _:self.accion_Boton('El'))
                self.btnGuardar.configure(state='normal')
                self.btnGuardar.bind("<1>", lambda _:self.accion_Boton('G'))
                self.btnEditar.configure(state='normal')
                self.btnEditar.bind("<1>", lambda _:self.accion_Boton('Ed'))

    def actualizacion_Numeros_Inscripcion(self) -> None:
        """
        Actualiza la lista de números de inscripción para evitar duplicados y agregar la opción "Todos" al inicio de la lista.

            Parámetros:
                None
        
            Devoluciones:
                None
        """
        ids_No_Inscripcion = self.correr_Query("SELECT No_Inscripción FROM Inscritos DESC")
        self.lista_No_Inscripcion = []
        for tupla in ids_No_Inscripcion:
            self.lista_No_Inscripcion.append(tupla[0])
        set_Ids_No_Inscripcion = set(self.lista_No_Inscripcion)
        self.lista_No_Inscripcion = list(set_Ids_No_Inscripcion)
        self.lista_No_Inscripcion.sort()
        self.lista_No_Inscripcion.insert(0, "Todos")
        self.cmbx_No_Inscripcion['values'] = self.lista_No_Inscripcion
    
    """========== Funciones para manejar TreeViews =========="""
    def crear_Treeview(self, tipo : str) -> None:
        """
        Crea el TreeView de la ventana principal de acuerdo al tipo solicitado.

            Parámetros:
                tipo (str): El tipo de TreeView; las opciones disponbiles son las siguientes:
                    "Inscritos" : Para la tabla Inscritos
                    "Carreras" : Para la tabla Carreras
                    "Cursos" : Para la tabla Cursos
                    "Alumnos" : Para la tabla Alumnos
                    "No_Inscripcion" : Para la tabla Inscritos filtrando a partir de un número de inscripción
            
            Devoluciones:
                None
        """
        # Elimina ventana emergente
        if tipo in ["Carreras", "Cursos", "Alumnos"]:
            self.ventana_btnconsultar.destroy()
            self.btnConsultar.configure(state="normal")
            self.btnConsultar.bind("<1>", self.accion_Consultar)
        # Elimina TreeView anterior (si existe)
        try :
            self.borrar_Treeview()
            self.scroll_H.destroy()
        except :
            pass
        # Crear Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        self.tView.bind("<B1-Motion>", "break")
        self.tView.place(anchor="nw", height=280, width=760, x=20, y=300)
        # Verifica el tipo de tabla para crear el TreeView correspondiente
        match tipo:
            case "Inscritos":
                """
                Creates the correponding TreeView for the table Inscritos.
                """
                self.tView_cols = ['tV_id_alumno', 'tV_fecha_inscripcion', 'tV_codigo', 'tV_horario']
                self.tView_dcols = ['tV_id_alumno', 'tV_fecha_inscripcion', 'tV_codigo', 'tV_horario']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
                self.tView.column("tV_id_alumno",anchor="w",stretch=True,width=50,minwidth=50)
                self.tView.column("tV_fecha_inscripcion",anchor="w",stretch=True,width=50,minwidth=50)
                self.tView.column("tV_codigo",anchor="w",stretch=True,width=50,minwidth=50)
                self.tView.column("tV_horario", anchor="w", stretch=True, width=50, minwidth=50)
                self.tView.heading("#0", anchor="w", text='No. Inscripción')
                self.tView.heading("tV_id_alumno", anchor="w", text='Id Alumno')
                self.tView.heading("tV_fecha_inscripcion", anchor="w", text='Fecha de Inscripción')
                self.tView.heading("tV_codigo", anchor="w", text='Código de Curso')
                self.tView.heading("tV_horario", anchor="w", text='Horario')
                self.tView.bind('<ButtonRelease-1>', self.seleccionar_Dato)
                query = self.correr_Query("SELECT * FROM Inscritos ORDER BY No_Inscripción DESC")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4]))
            
            case "Carreras":
                """
                Creates the correponding TreeView for the table Carreras.
                """
                #Columnas del Treeview
                self.btnEliminar.unbind('<1>')
                self.btnEliminar.configure(state="disable")
                self.btnGuardar.unbind('<1>')
                self.btnGuardar.configure(state="disable")
                self.btnEditar.unbind('<1>')
                self.btnEditar.configure(state="disable")
                self.tView_cols = ['tV_Descripcion', 'tV_semestres']
                self.tView_dcols = ['tV_Descripcion', 'tV_semestres']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
                self.tView.column("tV_Descripcion",anchor="w",stretch=True,width=200,minwidth=200)
                self.tView.column("tV_semestres",anchor="w",stretch=True,width=100,minwidth=100)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='Código de Carrera')
                self.tView.heading("tV_Descripcion", anchor="w", text='Descripcion')
                self.tView.heading("tV_semestres", anchor="w", text='No de semestres')
                #Configura los datos de la tabla
                query = self.correr_Query("SELECT * FROM Carreras")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2],))
            
            case "Cursos":
                """
                Creates the correponding TreeView for the table Cursos.
                """
                self.btnEliminar.unbind('<1>')
                self.btnEliminar.configure(state="disable")
                self.btnGuardar.unbind('<1>')
                self.btnGuardar.configure(state="disable")
                self.btnEditar.unbind('<1>')
                self.btnEditar.configure(state="disable")
                #Columnas del Treeview
                self.tView_cols = ['tV_descripción', 'tV_horas']
                self.tView_dcols = ['tV_descripción', 'tV_horas']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
                self.tView.column("tV_descripción",anchor="w",stretch=True,width=150,minwidth=50)
                self.tView.column("tV_horas",anchor="w",stretch=True,width=50,minwidth=10)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='Curso')
                self.tView.heading("tV_descripción", anchor="w", text='Descripción')
                self.tView.heading("tV_horas", anchor="w", text='Horas')
                #Configura los datos de la tabla
                query = self.correr_Query("SELECT * FROM Cursos")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2]))
            
            case "Alumnos":
                """
                Creates the correponding TreeView for the table Alumnos.
                """
                self.btnEliminar.unbind('<1>')
                self.btnEliminar.configure(state="disable")
                self.btnGuardar.unbind('<1>')
                self.btnGuardar.configure(state="disable")
                self.btnEditar.unbind('<1>')
                self.btnEditar.configure(state="disable")
                #Columnas del Treeview
                self.tView_cols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
                self.tView_dcols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=100,minwidth=100)
                self.tView.column("tV_id_carrera",anchor="w",stretch=True,width=100,minwidth=100)
                self.tView.column("tV_nombres",anchor="w",stretch=True,width=150,minwidth=150)
                self.tView.column("tV_apellidos", anchor="w", stretch=True, width=150, minwidth=150)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='Id Alumno')
                self.tView.heading("tV_id_carrera", anchor="w", text='Id Carrera')
                self.tView.heading("tV_nombres", anchor="w", text='Nombres')
                self.tView.heading("tV_apellidos", anchor="w", text='Apellidos')
                # Columna 3 en adelante...
                self.headers = ['Fecha de Inscripción', 'Dirección', 'Tel. Celular', 'Tel. Fijo', 'Ciudad', 'Departamento']
                for i in range(0, len(self.headers)) :
                    if self.headers[i] == 'Dirección':
                        self.tView.column(self.tView_cols[i+3], anchor="w", stretch=True, width=200, minwidth=200)
                        self.tView.heading(self.tView_dcols[i+3], anchor="w", text=self.headers[i])  
                    else:    
                        self.tView.column(self.tView_cols[i+3], anchor="w", stretch=True, width=125, minwidth=125)
                        self.tView.heading(self.tView_dcols[i+3], anchor="w", text=self.headers[i])
                        
                #Configura los datos de la tabla
                query = self.correr_Query("SELECT * FROM Alumnos")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
                self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h", command=self.tView.xview)
                self.scroll_H.configure(orient="horizontal")
                self.scroll_H.place(anchor="s", height=12, width=760, x=400, y=595)
                self.tView['xscrollcommand'] = self.scroll_H.set
            
            case "No_Inscripcion" :
                self.limpiar_Entradas("restaurar_Botones")
                """
                Creates the corresponding TreeView for the selecte No_Inscripción or shows the whole Inscritos table if "Todos" is entrada_Seleccionada.
                """
                #Columnas del Treeview
                self.tView_cols = ['tV_id_alumno', 'tV_fecha_inscripcion', 'tV_codigo', 'tV_horario']
                self.tView_dcols = ['tV_id_alumno', 'tV_fecha_inscripcion', 'tV_codigo', 'tV_horario']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
                self.tView.column("tV_id_alumno",anchor="w",stretch=True,width=50,minwidth=50)
                self.tView.column("tV_fecha_inscripcion",anchor="w",stretch=True,width=50,minwidth=10)
                self.tView.column("tV_codigo",anchor="w",stretch=True,width=50,minwidth=10)
                self.tView.column("tV_horario", anchor="w", stretch=True, width=50, minwidth=25)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='No. Inscripción')
                self.tView.heading("tV_id_alumno", anchor="w", text='Id Alumno')
                self.tView.heading("tV_fecha_inscripcion", anchor="w", text='Fecha de Inscripción')
                self.tView.heading("tV_codigo", anchor="w", text='Código de Curso')
                self.tView.heading("tV_horario", anchor="w", text='Horario')
                self.tView.bind('<ButtonRelease-1>', self.seleccionar_Dato)
                #Configura los datos de la tabla
                no_Inscripcion = self.cmbx_No_Inscripcion.get()
                # Para volver a mostrar todos los inscritos
                if no_Inscripcion == "Todos":
                    query = self.correr_Query("SELECT * FROM Inscritos ORDER BY No_Inscripción DESC")
                    self.limpiar_Entradas("datos_Alumno")
                    self.cmbx_No_Inscripcion.set("") # Borra el texto "Todos" del combobox
                # Para mostrar solo un número de inscripción
                else:
                    query = self.correr_Query(f"SELECT * FROM Inscritos WHERE No_Inscripción = {no_Inscripcion} ORDER BY Fecha_Inscripción DESC")
                    # Función para insertar información del alumno
                    self.insertar_Estudiante(no_Inscripcion)
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4]))

        #Scrollbars
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y", command=self.tView.yview)
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=280, width=12, x=789, y=580)
        self.tView['yscrollcommand'] = self.scroll_Y.set
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

    def borrar_Treeview(self) -> None:
        """
        Borra el TreeView existente en el frame de la ventana principal.

            Parámetros:
                None
            
            Devoluciones:
                None
        """
        self.tView.delete(*self.tView.get_children())
        self.tView.destroy()

    def seleccionar_Dato(self, event, todos : bool=False) -> Union[int, list[str]]:
        """
        Selecciona un registro del TreeView de la ventana principal y retorna el número de inscripción asociado.
        
        Parámetros:
            todos (bool): Opción para retornar el ID del alumno y el código del curso del registro (opcional, por defecto False)

        Devoluciones:
            numero_Inscripcion (int): El número de inscripción asociado al registro seleccionado (si todos = False)
            [alumno, código_curso] (list[str]): Lista con el ID del alumno y el código del curso del registro (si todos = True)
        """
        try:
            item_Seleccionado = self.tView.item(self.tView.focus()) 
            numero_Inscripcion = item_Seleccionado["text"]
            if todos == True:
                alumno=item_Seleccionado["values"][0]
                codigo_curso=item_Seleccionado["values"][2]
                return [alumno, codigo_curso]
            else:
                return numero_Inscripcion
        except IndexError:
            messagebox.showerror(title="Error al eliminar", message="No escogió ningún dato de la tabla")
    
    """========== Funciones para el uso de los botones =========="""      
    def accion_Boton(self, opcion : str) -> None:
        """
        Manejar la funcionalidad de los botones Guardar, Editar, Eliminar y Cancelar de la ventana principal.

            Parámetros:
                opcion (str): El botón del cual se quiere hace uso; las opciones disponibles son las siguientes:
                    'G' : Guardar
                    'Ed' : Editar
                    'El' : Eliminar
                    'C' : Cancelar

            Devoluciones:
                None
        """
        match  opcion:
            #Boton Guardar
            case 'G':
                self.btnEliminar.configure(state='disabled')
                # Para guardar nueva entrada...
                if self.id == -1:
                    if self.verificar_Entradas():
                        dia, mes, anio = map(str, self.fecha.get().split('/'))
                        # Verifica si debe crear un nuevo No. de Inscripción
                        if self.inscrito_Existente(self.cmbx_Id_Alumno.get()) == None:
                            self.lista_No_Inscripcion.pop(0)
                            num_Inscripcion = max(self.lista_No_Inscripcion) + 1
                            self.lista_No_Inscripcion.insert(0, "Todos")
                        # Si ya existe el No. de Inscripción...
                        else:
                            num_Inscripcion = self.inscrito_Existente(self.cmbx_Id_Alumno.get())
                            # Verifica si al estudiante se le habían eliminado los cursos para borrar ese registro
                            if self.registro_Existente(self.cmbx_Id_Alumno.get(), "[Sin cursos]"):
                                self.correr_Query(f"DELETE FROM Inscritos WHERE No_Inscripción = {num_Inscripcion}")
                        self.correr_Query(f"INSERT INTO Inscritos VALUES ({num_Inscripcion}, '{self.cmbx_Id_Alumno.get()}', '{anio}-{mes}-{dia}', '{self.cmbx_Id_Curso.get()}', '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}')")
                        self.crear_Treeview("Inscritos")
                        self.actualizacion_Numeros_Inscripcion()
                        messagebox.showinfo(title="guardar", message="Guardado con éxito")
                        self.limpiar_Entradas("datos_Todo")
                    else:
                        if self.registro_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()):
                            messagebox.askretrycancel(title="Error al intentar guardar", message="Ya existe una inscripción con esos datos")
                        elif self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
                            messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                # Para editar...
                else :
                    # Para editar solo el horario...
                    if str(self.curso_Anterior) == self.cmbx_Id_Curso.get():
                        if not(self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get())):
                            self.correr_Query(f"UPDATE Inscritos SET Código_Curso = '{self.cmbx_Id_Curso.get()}', Horario = '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}' WHERE No_Inscripción = {self.id} AND Código_Curso = '{self.curso_Anterior}'")
                            self.crear_Treeview("Inscritos")
                            messagebox.showinfo(title="Confirmación", message="Se ha editado la entrada con éxito.")
                            # Para volver a la normalidad...
                            self.cmbx_No_Inscripcion.configure(state="readonly")
                            self.cmbx_Id_Alumno.configure(state='readonly')
                            self.fecha.configure(state='normal')
                            self.limpiar_Entradas("datos_Todo")
                            # Restaura banderas     
                            self.id = -1
                            self.curso_Anterior = ""
                        else:
                            messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                    # Para editar curso (y horario)...
                    else:           
                        if not(self.registro_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get())) or not(self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get())):
                            self.correr_Query(f"UPDATE Inscritos SET Código_Curso = '{self.cmbx_Id_Curso.get()}', Horario = '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}' WHERE No_Inscripción = {self.id} AND Código_Curso = '{self.prev_Course}'")
                            self.create_Treeview("Inscritos")
                            messagebox.showinfo(title="Confirmación", message="Se ha editado la entrada con éxito.")
                            # Para volver a la normalidad...
                            self.cmbx_No_Inscripcion.configure(state="readonly")
                            self.cmbx_Id_Alumno.configure(state='readonly')
                            self.fecha.configure(state='normal')
                            self.limpiar_Entradas("datos_Todo")
                            # Restaura banderas 
                            self.id = -1
                            self.curso_Anterior = ""
                        else:
                            if self.registro_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()):
                                messagebox.askretrycancel(title="Error al intentar guardar", message="Ya existe una inscripción con esos datos")
                            elif self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
                                messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                
                # Restaura estilo del botón
                self.btnGuardar.after(100, lambda: self.btnGuardar.state(["!pressed"]))
                # Restaura el botón Eliminar
                self.btnEliminar.configure(state='normal')
                self.btnEliminar.bind("<1>", lambda _:self.accion_Boton('El'))

            #Boton Editar
            case 'Ed':
                entrada_Seleccionada = self.tView.focus()
                clave = self.tView.item(entrada_Seleccionada,'text')
                if clave == '':
                    messagebox.showwarning("Editar", 'Debes selecccionar un elemento.')
                else:
                    respuesta = messagebox.askyesno(title="Editar", message="¿Desea editar el elemento seleccionado?")
                    if respuesta:
                        self.btnEliminar.configure(state='disabled')
                        self.btnEliminar.unbind('<1>')
                        info = self.tView.item(entrada_Seleccionada)
                        self.limpiar_Entradas("datos_Curso")
                        self.insertar_Informacion(info['text'],info['values'][2])
                        self.id = clave
                        self.curso_Anterior = info['values'][2]
                        self.cmbx_Id_Alumno.configure(state='disabled')
                        self.fecha.configure(state='readonly')
                self.btnEditar.after(100, lambda: self.btnEditar.state(["!pressed"]))

            #Boton Eliminar
            case 'El':
                entrada_Seleccionada = self.tView.focus()
                info = self.tView.item(entrada_Seleccionada)
                if info['text'] == '':
                    messagebox.showwarning("Eliminar", 'Debes selecccionar un elemento.')
                elif info['values'][2] == '[Sin cursos]':
                    messagebox.showwarning("Error", 'Ya fueron eliminados los cursos de este estudiante.')
                else:
                    # Ventana eliminar
                    self.ventana_btneliminar = tk.Toplevel()
                    self.ventana_btneliminar.configure(background="#f7f9fd", height=165, width=260)
                    alto=165
                    ancho=260
                    self.ventana_btneliminar.geometry(str(ancho)+"x"+str(alto))

                    #Centrar Ventana eliminar
                    x = self.ventana_btneliminar.winfo_screenwidth()
                    y = self.ventana_btneliminar.winfo_screenheight()
                    self.ventana_btneliminar.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
                    self.ventana_btneliminar.resizable(False, False)
                    self.ventana_btneliminar.title('Eliminar')
                    ruta_ventana_btneliminar = self.dir_pro + "\\img\\basura.ico"
                    self.ventana_btneliminar.iconbitmap(bitmap=ruta_ventana_btneliminar)

                    # Radiobuttons
                    self.cuadro = tk.LabelFrame(self.ventana_btneliminar, background="#f7f9fd")
                    self.opcion_seleccionada = tk.IntVar()
                    self.opcion1 = tk.Radiobutton (self.cuadro, background="#f7f9fd", text= 'Borrar curso de este estudiante', width=220, anchor=tk.W, variable = self.opcion_seleccionada, value=1) 
                    self.opcion1.pack()
                    self.opcion2 = tk.Radiobutton (self.cuadro, background="#f7f9fd", text= 'Borrar estudiantes de este curso', width=220, anchor=tk.W, variable = self.opcion_seleccionada, value=2) 
                    self.opcion2.pack()
                    self.opcion3 = tk.Radiobutton (self.cuadro, background="#f7f9fd", text= 'Borrar cursos de este estudiante', width=220, anchor=tk.W, variable = self.opcion_seleccionada, value=3) 
                    self.opcion3.pack()
                    self.cuadro.pack(padx=20, pady=20)
                    
                    # Botón eliminar
                    self.btneliminar_opcion = ttk.Button(self.ventana_btneliminar, name="btneliminar_opcion")
                    self.btneliminar_opcion.configure(text='Confirmar')
                    self.btneliminar_opcion.place(anchor="nw", x=90, y=120)
                    self.btneliminar_opcion.bind("<1>", lambda _:self.accion_Eliminar())  
                    self.btnEliminar.config(state='disabled')  # Deshabilitamos el botón
                    self.btnEliminar.unbind('<1>')
                self.btnEliminar.after(100, lambda: self.btnEliminar.state(["!pressed"]))
                try:
                    def despues_Cerrar() -> None: 
                        """Función que se llama cuando se pulsa el botón de cierre de la ventana con las opciones de eliminación."""        
                        self.ventana_btneliminar.destroy()  # Destruimos la ventana secundaria
                        self.btnEliminar.config(state='normal')  # habilitamos el botón
                        self.btnEliminar.bind("<1>", lambda _:self.accion_Boton('El'))
                    self.ventana_btneliminar.protocol("WM_DELETE_WINDOW", despues_Cerrar) #Protocolo que se activa cuando se intenta cerrar la ventana
                except: pass
            
            #Boton Cancelar
            case 'C':
                respuesta = messagebox.askyesno(title="Cancelar", message="Desea cancelar")
                if respuesta:
                    self.crear_Treeview("Inscritos")
                    self.cmbx_No_Inscripcion.configure(state="readonly")
                    self.cmbx_Id_Alumno.configure(state='readonly')
                    self.fecha.configure(state='normal')
                    self.limpiar_Entradas("restaurar_Botones")
                    self.limpiar_Entradas("datos_Todo")
                self.btnCancelar.after(100, lambda: self.btnCancelar.state(["!pressed"]))

    def accion_Eliminar(self) -> None:
        """
        Maneja la funcionalidad de las diferentes opciones de eliminación disponibles en la ventana mostrada el presionar el botón Eliminar.

            Parámetros:
                None
            
            Devoluciones:
                None
        """
        opcion_borrar = self.opcion_seleccionada.get()
        numero_Inscrito = self.seleccionar_Dato(event=None)
        informacion_Inscrito = self.seleccionar_Dato(event=None, todos=True)
        alumno_Inscrito = informacion_Inscrito[0]
        codigo_Curso = informacion_Inscrito[1]
        # Borrar este curso del estudiante
        if opcion_borrar == 1:
            respuesta = messagebox.askyesno(title="Eliminar", message=f"¿Desea eliminar el curso con código {codigo_Curso} del estudiante con Id No. {alumno_Inscrito}?")
            if respuesta:
                contador=self.correr_Query(f"SELECT COUNT (*) FROM Inscritos WHERE No_Inscripción = {numero_Inscrito}")
                self.correr_Query(f"DELETE FROM Inscritos WHERE No_Inscripción = {numero_Inscrito} AND Código_Curso = '{codigo_Curso}'")
                if contador[0][0] == 1:
                    anio, mes, dia = map(str, str(date.today()).split('-'))
                    self.correr_Query(f"INSERT INTO Inscritos VALUES ({numero_Inscrito}, '{alumno_Inscrito}', '{anio}-{mes}-{dia}', '[Sin cursos]', '')")
                self.eliminacion_Exitosa()
            else:
                self.ventana_btneliminar.destroy()
        # Borrar todos los estudiantes de un curso
        elif opcion_borrar == 2:
            respuesta = messagebox.askyesno(title="Eliminar", message=f"¿Desea eliminar todos los estudiantes del curso con código {codigo_Curso}?")
            if respuesta:
                estudiantes = self.correr_Query(f"SELECT * FROM Inscritos WHERE Código_Curso = {codigo_Curso}")
                self.correr_Query(f"DELETE FROM Inscritos WHERE Código_Curso = '{codigo_Curso}'")
                for estudiante in estudiantes:
                    contador = self.correr_Query(f"SELECT COUNT (*) FROM Inscritos WHERE No_Inscripción = {estudiante[0]}")
                    # Por si alguno solo tenía ese curso inscrito...
                    if contador[0][0] == 0:
                        anio, mes, dia = map(str, str(date.today()).split('-'))
                        self.correr_Query(f"INSERT INTO Inscritos VALUES ({estudiante[0]}, {estudiante[1]}, '{anio}-{mes}-{dia}', '[Sin cursos]', '')")
                self.eliminacion_Exitosa()
            else:
                self.ventana_btneliminar.destroy()
        # Borrar todos los cursos de un estudiante
        elif opcion_borrar == 3:
            respuesta = messagebox.askyesno(title="Eliminar", message=f"¿Desea eliminar todos los cursos del estudiante con Id No. {alumno_Inscrito}?")
            if respuesta:
                self.correr_Query(f"DELETE FROM Inscritos WHERE No_Inscripción = {numero_Inscrito}")     
                anio, mes, dia = map(str, str(date.today()).split('-'))
                self.correr_Query(f"INSERT INTO Inscritos VALUES ({numero_Inscrito}, '{alumno_Inscrito}', '{anio}-{mes}-{dia}', '[Sin cursos]', '')")
                self.eliminacion_Exitosa()
            else:
                self.ventana_btneliminar.destroy()

    def eliminacion_Exitosa(self) -> None:
        """
        Secuencia de acciones a realizar después de una eliminación exitosa (e.g. restaurar el botón Eliminar).

            Parámetros:
                None

            Devoluciones:
                None
        """
        self.ventana_btneliminar.destroy()
        self.crear_Treeview("Inscritos")
        self.actualizacion_Numeros_Inscripcion()
        messagebox.showinfo(title="Confirmación", message="Eliminado con éxito.")
        self.btnEliminar.configure(state='normal')
        self.btnEliminar.bind("<1>", lambda _:self.accion_Boton('El'))        
    
    """========== Funciones para el botón Consultar (<Lupa>) =========="""
    def accion_Consultar(self, event) -> None:
        """
        Maneja la funcionalidad del botón Consultar (<Lupa>); abre una ventana con el menú de consulta.

            Parámetros:
                (event): Evento
            
            Devoluciones:
                None
        """
        self.ventana_btnconsultar = tk.Toplevel()
        self.ventana_btnconsultar.configure(background="#f7f9fd", height=335, width=325)
        alto=335
        ancho=325
        self.ventana_btnconsultar.geometry(str(ancho)+"x"+str(alto))
        #Centrar Ventana consultar
        x = self.ventana_btnconsultar.winfo_screenwidth()
        y = self.ventana_btnconsultar.winfo_screenheight()
        self.ventana_btnconsultar.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
        self.ventana_btnconsultar.resizable(False, False)
        self.ventana_btnconsultar.title('Consultar')
        ruta_ventana_btnconsultar = self.dir_pro + "\\img\\lupa.ico"
        self.ventana_btnconsultar.iconbitmap(bitmap=ruta_ventana_btnconsultar)

        #Label listados
        self.lblListados = ttk.Label(self.ventana_btnconsultar, name="lblListados")
        self.lblListados.configure(background="#f7f9fd", text='Consultar listados')
        self.lblListados.place(anchor="nw", x=20, y=20)

        #Botones de la ventana consultar

        self.btnconsultar_alumnos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_alumnos")
        self.btnconsultar_alumnos.configure(text='Alumnos')
        self.btnconsultar_alumnos.place(anchor="nw", x=20, y=50)
        self.btnconsultar_alumnos.bind("<1>", lambda _:self.crear_Treeview("Alumnos"))

        self.btnconsultar_carreras = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_carreras")
        self.btnconsultar_carreras.configure(text='Carreras')
        self.btnconsultar_carreras.place(anchor="nw", x=125, y=50)
        self.btnconsultar_carreras.bind("<1>", lambda _:self.crear_Treeview("Carreras"))

        self.btnconsultar_cursos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_cursos")
        self.btnconsultar_cursos.configure(text='Cursos')
        self.btnconsultar_cursos.place(anchor="nw", x=230, y=50)
        self.btnconsultar_cursos.bind("<1>", lambda _:self.crear_Treeview("Cursos"))

        #Separador
        separador1 = ttk.Separator(self.ventana_btnconsultar)
        separador1.configure(orient="horizontal")
        separador1.place(anchor="nw", width=285, x=20, y=90)

        #Label filtros
        self.lblFiltros = ttk.Label(self.ventana_btnconsultar, name="lblFiltros")
        self.lblFiltros.configure(background="#f7f9fd", text='Filtrar')
        self.lblFiltros.place(anchor="nw", x=20, y=110)

        #Label filtro 1
        self.lblFiltro1 = ttk.Label(self.ventana_btnconsultar, name="lblFiltro1")
        self.lblFiltro1.configure(background="#f7f9fd", text=' ●   Cursos de un alumno')
        self.lblFiltro1.place(anchor="nw", x=20, y=140)

        #Label seleccione alumno
        self.lblSlcalumno = ttk.Label(self.ventana_btnconsultar, name="lblSlcalumno")
        self.lblSlcalumno.configure(background="#f7f9fd", text='Seleccione alumno:')
        self.lblSlcalumno.place(anchor="nw", x=40, y=170)

        #Definir path de la lupa 2 para los botones de los filtros
        ruta_Lupa2  = self.dir_pro + "\\img\\lupa2.png"
        self.img2 = PhotoImage(file=ruta_Lupa2)

        #Botón confirmar consulta alumno
        self.btnFiltrar_alumno = ttk.Button(self.ventana_btnconsultar, name="btnfiltrar_alumno", image=self.img2)
        self.btnFiltrar_alumno.place(anchor="nw", x=270, y=168)
        self.btnFiltrar_alumno.configure(state='disabled')      

        #Combobox Alumno de ventana consulta
        self.cmbx_Id_Alumno_Consulta = ttk.Combobox(self.ventana_btnconsultar, name="cmbx_id_alumno", state="readonly")
        self.cmbx_Id_Alumno_Consulta.place(anchor="nw", width=95, x=160, y=170)
        self.ids_Alumnos = self.correr_Query("SELECT Id_Alumno FROM Alumnos")
        self.lista_Ids_Alumnos = []
        for tupla in self.ids_Alumnos:
            self.lista_Ids_Alumnos.append(tupla[0])
        self.cmbx_Id_Alumno_Consulta['values'] = self.ids_Alumnos
        self.cmbx_Id_Alumno_Consulta.bind("<<ComboboxSelected>>", lambda _:self.habilitar_Filtros(1))
        #Label filtro 2
        self.lblFiltro2 = ttk.Label(self.ventana_btnconsultar, name="lblFiltro2")
        self.lblFiltro2.configure(background="#f7f9fd", text=' ●   Alumnos en un curso')
        self.lblFiltro2.place(anchor="nw", x=20, y=200)

        #Label seleccione curso
        self.lblSlccurso = ttk.Label(self.ventana_btnconsultar, name="lblSlccurso")
        self.lblSlccurso.configure(background="#f7f9fd", text='Seleccione curso:')
        self.lblSlccurso.place(anchor="nw", x=40, y=230)

        #Botón confirmar consulta curso
        self.btnFiltrar_curso = ttk.Button(self.ventana_btnconsultar, name="btnfiltrar_curso", image=self.img2)
        self.btnFiltrar_curso.place(anchor="nw", x=270, y=228)
        self.btnFiltrar_curso.configure(state='disabled')

        #Combobox Curso  de ventana consulta
        self.cmbx_Id_Curso_Consulta = ttk.Combobox(self.ventana_btnconsultar, name="cmbx_id_curso", state="readonly")
        self.cmbx_Id_Curso_Consulta.place(anchor="nw", width=95, x=160, y=230)
        self.ids_Cursos = self.correr_Query("SELECT Código_Curso FROM Cursos")
        self.lista_Ids_Cursos = []
        for tupla in self.ids_Cursos:
            self.lista_Ids_Cursos.append(tupla[0])
        self.cmbx_Id_Curso_Consulta['values'] = self.ids_Cursos
        self.cmbx_Id_Curso_Consulta.bind("<<ComboboxSelected>>", lambda _:self.habilitar_Filtros(2))

        #Label filtros 3
        self.lblFiltro3 = ttk.Label(self.ventana_btnconsultar, name="lblFiltro3")
        self.lblFiltro3.configure(background="#f7f9fd", text=' ●   Inscripciones por fecha')
        self.lblFiltro3.place(anchor="nw", x=20, y=260)

        #Label ingrese una fecha
        self.lblIgfecha = ttk.Label(self.ventana_btnconsultar, name="lblIgfecha")
        self.lblIgfecha.configure(background="#f7f9fd", text='Ingrese fecha:')
        self.lblIgfecha.place(anchor="nw", x=40, y=290)

        #Botón confirmar consulta fecha
        self.btnFiltrar_fecha = ttk.Button(self.ventana_btnconsultar, name="btnfiltrar_Fecha", image=self.img2)
        self.btnFiltrar_fecha.place(anchor="nw", x=270, y=288)
        self.btnFiltrar_fecha.configure(state='disabled')

        #Entry Fecha de ventana consulta
        self.Fecha_Consulta = ttk.Entry(self.ventana_btnconsultar, name="fechaconsulta")
        self.Fecha_Consulta.configure(justify="center")
        self.Fecha_Consulta.place(anchor="nw", width=95, x=160, y=290)
        self.Fecha_Consulta.bind("<BackSpace>", lambda _:self.Fecha_Consulta.delete(0,"end"))
        self.Fecha_Consulta.bind("<KeyRelease>", self.valida_Fecha_Consulta)
        self.btnConsultar.configure(state='disabled')  # Deshabilitamos el botón
        self.btnConsultar.unbind('<1>')
        try:
            def despues_Cerrar() -> None: 
                """Función que se llama cuando se pulsa el botón de cierre de la ventana con las opciones de consulta."""      
                self.ventana_btnconsultar.destroy()  # Destruimos la ventana secundaria
                self.btnConsultar.config(state='normal')  # habilitamos el botón
                self.btnConsultar.bind("<1>", self.accion_Consultar)
            self.ventana_btnconsultar.protocol("WM_DELETE_WINDOW", despues_Cerrar) #Protocolo que se activa cuando se intenta cerrar la ventana
        except: pass

    def habilitar_Filtros(self, opcion : int) -> None:
        """
        Habilita los distintos filtros según la opción ingresada.

            Parámetros:
                opcion (int): El filtro que se desea habilitar; las opciones son las siguientes:
                    1 : Filtro a partir del ID del alumno
                    2 : Filtro a partir del código del curso
                    3 : Filtro a partir de la fecha
            
            Devoluciones:
                None
        """
        match opcion:
            case 1:
                self.btnFiltrar_alumno.configure(state='normal')
                self.btnFiltrar_alumno.bind("<1>", lambda _:self.accion_Filtrar('Alumno'))
            case 2:
                self.btnFiltrar_curso.configure(state='normal')
                self.btnFiltrar_curso.bind("<1>", lambda _:self.accion_Filtrar('Curso'))
            case 3:
                self.btnFiltrar_fecha.configure(state='normal')
                self.btnFiltrar_fecha.bind("<1>", lambda _:self.accion_Filtrar('Fecha'))
    
    def valida_Fecha_Consulta(self, event=None) -> None:
        """
         Verifica que la fecha ingresada en el entry de fecha de la ventana de consulta esté bien escrita.

            Parámetros:
                (event): Evento (opcional)
            
            Devoluciones:
                None
        """
        if event.char.isdigit() or event.char == "" or event.keysym == "Return":
            self.habilitar_Filtros(3)  
            fecha_Ingresada = self.Fecha_Consulta.get()
            if len(fecha_Ingresada) > 10:
                messagebox.showerror(message="Máximo 10 digitos", title="Error al ingresar fecha")
                self.Fecha_Consulta.delete(10, "end")
            num_char = 0
            for i in fecha_Ingresada:
                num_char += 1
            if num_char == 2: self.Fecha_Consulta.insert(2, "/")
            if num_char  == 5: self.Fecha_Consulta.insert(6, "/")
        else:
            self.Fecha_Consulta.delete(len(self.Fecha_Consulta.get())-1, "end")
            respuesta_mensaje=messagebox.showerror(message="Solo numeros", title="Fecha Erronea")
            if respuesta_mensaje:
                self.ventana_btnconsultar.deiconify()

    def accion_Filtrar(self, filtro : str) -> None:
        """
        Crea la ventana correspondiente al filtro seleccionado con un label indicando el título de la tabla (TreView) a presentar.

            Parámetros:
                filtro (str): El tipo de filtro seleccionado; las opciones son las siguientes:
                    'Alumno' : Filtro a partir del ID del alumno
                    'Curso' : Filtro a partir del código del curso
                    'Fecha' : Filtro a partir de la fecha
            
            Devoluciones:
                None
        """
        match  filtro:
            case 'Alumno':
                try:
                    self.ventana_btnfiltrar_curso.destroy()
                    self.ventana_btnfiltrar_fecha.destroy()
                except: pass
                #Crear ventana filtrar alumno
                self.ventana_btnfiltrar_alumno = tk.Toplevel()
                self.ventana_btnfiltrar_alumno.configure(background="#f7f9fd", height=295, width=640)
                alto = 295
                ancho = 640
                self.ventana_btnfiltrar_alumno.geometry(str(ancho)+"x"+str(alto))
                #Centrar Ventana filtrar alumno
                x = self.ventana_btnfiltrar_alumno.winfo_screenwidth()
                y = self.ventana_btnfiltrar_alumno.winfo_screenheight()
                self.ventana_btnfiltrar_alumno.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
                self.ventana_btnfiltrar_alumno.resizable(False, False)
                self.ventana_btnfiltrar_alumno.title('Filtrar cursos de un alumno')
                ruta_ventana_btnfiltrar_alumno = self.dir_pro + "\\img\\lupa.ico"
                self.ventana_btnfiltrar_alumno.iconbitmap(bitmap=ruta_ventana_btnfiltrar_alumno)
                #Frame filtro alumno
                self.frm_2 = tk.Frame(self.ventana_btnfiltrar_alumno, name="frm_2")
                self.frm_2.configure(background="#f7f9fd", height=500, width=700)
                #Label filtar alumno
                datos = self.correr_Query(f"SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno='{self.cmbx_Id_Alumno_Consulta.get()}'")
                self.lblFilalumno = ttk.Label(self.frm_2, name="lblFilalumno")
                self.lblFilalumno.configure(background="#f7f9fd",font="{Arial} 11 {bold}",takefocus=False, text='Cursos del alumno '+ datos[0][0] + ' ' + datos[0][1] +' (' + self.cmbx_Id_Alumno_Consulta.get() + ')')
                self.lblFilalumno.place(anchor="c", relx=0.5, y=25)
                #Treeview filtrar alumno
                self.crear_Treeview_Filtro(1)
                self.btnFiltrar_alumno.config(state='disabled')  # Deshabilitamos el botón
                self.btnFiltrar_alumno.unbind('<1>')
                self.cmbx_Id_Alumno_Consulta.configure(state='disabled')
                try:
                    def despues_Cerrar(): 
                        """Función que se llama cuando se pulsa el botón de cierre de la ventana con la tabla tras el filtro a partir del ID del alumno."""    
                        self.ventana_btnfiltrar_alumno.destroy()  # Destruimos la ventana secundaria
                        self.btnFiltrar_alumno.config(state='normal')  # habilitamos el botón
                        self.btnFiltrar_alumno.bind("<1>", lambda _:self.accion_Filtrar('Alumno'))
                        self.cmbx_Id_Alumno_Consulta.configure(state='readonly')

                    self.ventana_btnfiltrar_alumno.protocol("WM_DELETE_WINDOW", despues_Cerrar) #Protocolo que se activa cuando se intenta cerrar la ventana
                except: pass
            
            case 'Curso':
                try:
                    self.ventana_btnfiltrar_alumno.destroy()
                    self.ventana_btnfiltrar_fecha.destroy()
                except: pass
                #Crear ventana filtrar curso
                self.ventana_btnfiltrar_curso = tk.Toplevel()
                self.ventana_btnfiltrar_curso.configure(background="#f7f9fd", height=295, width=640)
                alto=295
                ancho=640
                self.ventana_btnfiltrar_curso.geometry(str(ancho)+"x"+str(alto))
                #Centrar Ventana filtrar curso
                x = self.ventana_btnfiltrar_curso.winfo_screenwidth()
                y = self.ventana_btnfiltrar_curso.winfo_screenheight()
                self.ventana_btnfiltrar_curso.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
                self.ventana_btnfiltrar_curso.resizable(False, False)
                self.ventana_btnfiltrar_curso.title('Filtrar alumnos en un curso')
                ruta_ventana_btnfiltrar_curso = self.dir_pro + "\\img\\lupa.ico"
                self.ventana_btnfiltrar_curso.iconbitmap(bitmap=ruta_ventana_btnfiltrar_curso)
                #Frame filtro
                self.frm_2 = tk.Frame(self.ventana_btnfiltrar_curso, name="frm_2")
                self.frm_2.configure(background="#f7f9fd", height=500, width=700)
                #Label filtar curso
                datos=self.correr_Query(f"SELECT Descrip_Curso FROM Cursos WHERE Código_Curso='{self.cmbx_Id_Curso_Consulta.get()}'")
                self.lblFilcurso = ttk.Label(self.frm_2, name="lblFilcurso")
                self.lblFilcurso.configure(background="#f7f9fd",font="{Arial} 11 {bold}",takefocus=False, text=f"Alumnos del curso {datos[0][0]} ({self.cmbx_Id_Curso_Consulta.get()})")
                self.lblFilcurso.place(anchor="c", relx=0.5, y=25)
                #Treeview filtrar curso
                self.crear_Treeview_Filtro(2)
                self.btnFiltrar_curso.config(state='disable')  # Deshabilitamos el botón
                self.btnFiltrar_curso.unbind('<1>')
                self.cmbx_Id_Curso_Consulta.configure(state='disabled')
                try:
                    def despues_Cerrar(): 
                        """Función que se llama cuando se pulsa el botón de cierre de la ventana con la tabla tras el filtro a partir del código del curso."""     
                        self.ventana_btnfiltrar_curso.destroy()  # Destruimos la ventana secundaria
                        self.btnFiltrar_curso.config(state='normal')  # habilitamos el botón
                        self.btnFiltrar_curso.bind("<1>", lambda _:self.accion_Filtrar('Curso'))
                        self.cmbx_Id_Curso_Consulta.configure(state="readonly")
                    self.ventana_btnfiltrar_curso.protocol("WM_DELETE_WINDOW", despues_Cerrar) #Protocolo que se activa cuando se intenta cerrar la ventana
                except: pass
            
            case 'Fecha':
                if self.fecha_Valida(self.Fecha_Consulta.get()):
                    try:
                        self.ventana_btnfiltrar_alumno.destroy()
                        self.ventana_btnfiltrar_curso.destroy()
                    except: pass
                    #Crear ventana filtrar fecha
                    self.ventana_btnfiltrar_fecha = tk.Toplevel()
                    self.ventana_btnfiltrar_fecha.configure(background="#f7f9fd", height=295, width=640)
                    alto=295
                    ancho=640
                    self.ventana_btnfiltrar_fecha.geometry(str(ancho)+"x"+str(alto))
                    #Centrar Ventana filtrar fecha
                    x = self.ventana_btnfiltrar_fecha.winfo_screenwidth()
                    y = self.ventana_btnfiltrar_fecha.winfo_screenheight()
                    self.ventana_btnfiltrar_fecha.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
                    self.ventana_btnfiltrar_fecha.resizable(False, False)
                    self.ventana_btnfiltrar_fecha.title('Filtrar inscripciones por fecha')
                    ruta_ventana_btnfiltrar_fecha = self.dir_pro + "\\img\\lupa.ico"
                    self.ventana_btnfiltrar_fecha.iconbitmap(bitmap=ruta_ventana_btnfiltrar_fecha)
                    #Frame filtro
                    self.frm_2 = tk.Frame(self.ventana_btnfiltrar_fecha, name="frm_2")
                    self.frm_2.configure(background="#f7f9fd", height=500, width=700)
                    #Label filtar fecha
                    self.lblFilfecha = ttk.Label(self.frm_2, name="lblFilfecha")
                    self.lblFilfecha.configure(background="#f7f9fd",font="{Arial} 11 {bold}",takefocus=False, text=f"Alumnos inscritos el {self.Fecha_Consulta.get()}")
                    self.lblFilfecha.place(anchor="c", relx=0.5, y=25)
                    #Treeview filtrar fecha
                    self.crear_Treeview_Filtro(3)
                    self.btnFiltrar_fecha.config(state='disabled')  # Deshabilitamos el botón
                    self.btnFiltrar_fecha.unbind('<1>')
                    self.Fecha_Consulta.configure(state='disabled')
                    try:
                        def despues_Cerrar(): 
                            """Función que se llama cuando se pulsa el botón de cierre de la ventana con la tabla tras el filtro a partir de la fecha."""    
                            self.ventana_btnfiltrar_fecha.destroy()  # Destruimos la ventana secundaria
                            self.btnFiltrar_fecha.config(state='normal')  # habilitamos el botón
                            self.btnFiltrar_fecha.bind("<1>", lambda _:self.accion_Filtrar('Fecha'))
                            self.Fecha_Consulta.configure(state='normal')
                        self.ventana_btnfiltrar_fecha.protocol("WM_DELETE_WINDOW", despues_Cerrar) #Protocolo que se activa cuando se intenta cerrar la ventana
                    except: pass                    

    def crear_Treeview_Filtro(self, tipo : int) -> None:
        """
        Crea el TreeView en la ventana de filtro correspondiente de acuerdo al tipo solicitado.

            Parámetros:
                tipo (int): El tipo de TreeView; las opciones disponibles son las siguientes:
                    1 : Filtro a partir del ID del alumno
                    2 : Filtro a partir del código del curso
                    3 : Filtor a partir de la fecha
            
            Devoluciones:
                None
        """
        # Crear TreeView
        self.tView_Filtro = ttk.Treeview(self.frm_2, name="filter_tview")
        self.tView_Filtro.configure(selectmode="extended")
        self.tView_Filtro.place(anchor="nw", x=20, y=50, height=225, width=600)
        self.tView_Filtro.bind("<B1-Motion>", "break")
        match tipo:
            case 1:
                id_Alumno = self.cmbx_Id_Alumno_Consulta.get()
                #Columnas del Treeview
                self.tView_cols = ['ftV_codigo', 'ftV_nombre_curso', 'ftV_horario']
                self.tView_dcols = ['ftV_codigo', 'ftV_nombre_curso', 'ftV_horario']
                self.tView_Filtro.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView_Filtro.column("#0",anchor="w",width=100,minwidth=100, stretch=False)
                self.tView_Filtro.column("ftV_codigo",anchor="w",width=100,minwidth=100, stretch=False)
                self.tView_Filtro.column("ftV_nombre_curso",anchor="w",width=230,minwidth=230, stretch=False)
                self.tView_Filtro.column("ftV_horario", anchor="w", width=168, minwidth=168, stretch=False)
                #Cabeceras
                self.tView_Filtro.heading("#0", anchor="w", text='No. Inscripción')
                self.tView_Filtro.heading("ftV_codigo", anchor="w", text='Código Curso')
                self.tView_Filtro.heading("ftV_nombre_curso", anchor="w", text='Nombre Curso')
                self.tView_Filtro.heading("ftV_horario", anchor="w", text='Horario')
                #Configura los datos de la tabla
                query = self.correr_Query(f"SELECT Inscritos.No_Inscripción, Inscritos.Código_Curso, Cursos.Descrip_Curso, Inscritos.Horario FROM Cursos INNER JOIN (Inscritos INNER JOIN Alumnos ON Inscritos.Id_Alumno=Alumnos.Id_Alumno) ON Inscritos.Código_Curso = Cursos.Código_Curso WHERE Inscritos.Id_Alumno = '{id_Alumno}' ORDER BY Cursos.Descrip_Curso ASC")
                for i in query:
                    self.tView_Filtro.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3]))
        
            case 2:
                codigo_Curso = self.cmbx_Id_Curso_Consulta.get()
                #Columnas del Treeview
                self.tView_cols = ['ftV_id_alumno', 'ftV_nombre', 'ftV_apellidos', 'ftV_fecha']
                self.tView_dcols = ['ftV_id_alumno', 'ftV_nombre', 'ftV_apellidos', 'ftV_fecha']
                self.tView_Filtro.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView_Filtro.column("#0",anchor="w",stretch=False,width=100,minwidth=100)
                self.tView_Filtro.column("ftV_id_alumno",anchor="w",stretch=False,width=100,minwidth=100)
                self.tView_Filtro.column("ftV_nombre",anchor="w",stretch=False,width=115,minwidth=115)
                self.tView_Filtro.column("ftV_apellidos", anchor="w", stretch=False, width=115, minwidth=115)
                self.tView_Filtro.column("ftV_fecha", anchor="w", stretch=False, width=168, minwidth=168)
                #Cabeceras
                self.tView_Filtro.heading("#0", anchor="w", text='No. Inscripción')
                self.tView_Filtro.heading("ftV_id_alumno", anchor="w", text='Id Alumno')
                self.tView_Filtro.heading("ftV_nombre", anchor="w", text='Nombres')
                self.tView_Filtro.heading("ftV_apellidos", anchor="w", text='Apellidos')
                self.tView_Filtro.heading("ftV_fecha", anchor="w", text='Fecha Inscripción')
                #Configura los datos de la tabla
                query = self.correr_Query(f"SELECT Inscritos.No_Inscripción, Inscritos.Id_Alumno, Alumnos.Nombres, Alumnos.Apellidos, Inscritos. Horario FROM Inscritos INNER JOIN Alumnos ON Inscritos.Id_Alumno=Alumnos.Id_Alumno WHERE Inscritos.Código_Curso = '{codigo_Curso}' ORDER BY Inscritos.No_Inscripción DESC")
                for i in query:
                    self.tView_Filtro.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4]))
            
            case 3:
                dia, mes, anio = map(str, self.Fecha_Consulta.get().split('/'))
                #Columnas del Treeview
                self.tView_cols = ['ftV_id_alumno', 'ftV_nombre', 'ftV_apellidos', 'ftV_codigo', 'ftV_nombre_curso']
                self.tView_dcols = ['ftV_id_alumno', 'ftV_nombre', 'ftV_apellidos', 'ftV_codigo', 'ftV_nombre_curso']
                self.tView_Filtro.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView_Filtro.column("#0",anchor="w",stretch=False,width=100,minwidth=100)
                self.tView_Filtro.column("ftV_id_alumno",anchor="w",stretch=False,width=100,minwidth=100)
                self.tView_Filtro.column("ftV_nombre",anchor="w",stretch=False,width=115,minwidth=115)
                self.tView_Filtro.column("ftV_apellidos", anchor="w", stretch=False, width=115, minwidth=115)
                self.tView_Filtro.column("ftV_codigo", anchor="w", stretch=False, width=100, minwidth=100)
                self.tView_Filtro.column("ftV_nombre_curso", anchor="w", stretch=False, width=230, minwidth=230)
                #Cabeceras
                self.tView_Filtro.heading("#0", anchor="w", text='No. Inscripción')
                self.tView_Filtro.heading("ftV_id_alumno", anchor="w", text='Id Alumno')
                self.tView_Filtro.heading("ftV_nombre", anchor="w", text='Nombres')
                self.tView_Filtro.heading("ftV_apellidos", anchor="w", text='Apellidos')
                self.tView_Filtro.heading("ftV_codigo", anchor="w", text='Código Curso')
                self.tView_Filtro.heading("ftV_nombre_curso", anchor="w", text='Nombre Curso')
                #Configura los datos de la tabla
                query = self.correr_Query(f"SELECT Inscritos.No_Inscripción, Inscritos.Id_Alumno, Alumnos.Nombres, Alumnos.Apellidos, Inscritos.Código_Curso, Cursos.Descrip_Curso FROM Cursos INNER JOIN (Inscritos INNER JOIN Alumnos ON Inscritos.Id_Alumno=Alumnos.Id_Alumno) ON Inscritos.Código_Curso = Cursos.Código_Curso WHERE Inscritos.Fecha_Inscripción = '{anio}-{mes}-{dia}' ORDER BY Inscritos.No_Inscripción DESC;")
                for i in query:
                    self.tView_Filtro.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4], i[5]))
                self.filter_scroll_H = ttk.Scrollbar(self.frm_2, name="filter_scroll_h", command=self.tView_Filtro.xview)
                self.filter_scroll_H.configure(orient="horizontal")
                self.filter_scroll_H.place(anchor="s", height=10, width=600, x=320, y=289)
                self.tView_Filtro['xscrollcommand'] = self.filter_scroll_H.set
        
        #Scrollbars
        self.scroll_Y_Filtro = ttk.Scrollbar(self.frm_2, name="filter_scroll_y", command=self.tView_Filtro.yview)
        self.scroll_Y_Filtro.configure(orient="vertical")
        self.scroll_Y_Filtro.place(anchor="s", height=225, width=12, x=629, y=275)
        self.tView_Filtro['yscrollcommand'] = self.scroll_Y_Filtro.set
        self.frm_2.pack(side="top")
        self.frm_2.pack_propagate(0)

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import PhotoImage
from os import path
import sqlite3
from datetime import datetime

class Inscripciones_2:   
    def __init__(self, master=None):
        self.dir_pro = path.dirname(__file__)
        self.db_name = 'Inscripciones.db'
        # Ventana principal    
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd", height=600, width=800)
        alto=600
        ancho=800
        self.win.geometry(str(ancho)+"x"+str(alto))
        #Centrar Ventana
        x = self.win.winfo_screenwidth()
        y = self.win.winfo_screenheight()
        self.win.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2))-30)))
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        ruta_Icon = self.dir_pro + "\\img\\icon.ico"
        self.win.iconbitmap(bitmap=ruta_Icon)
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        #Label No. Inscripción
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="center",state="normal",
                                        takefocus=False,text='No. Inscripción')
        #Combobox No. Inscripción
        self.cmbx_No_Inscripcion = ttk.Combobox(self.frm_1, name="cmbxnoincripcion", state="readonly")
        self.cmbx_No_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        ids_No_Inscripcion = self.run_Query("SELECT No_Inscripción FROM Inscritos DESC")
        self.cmbx_No_Inscripcion['values'] = ids_No_Inscripcion
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
        self.ids_Alumnos = self.run_Query("SELECT Id_Alumno FROM Alumnos")
        self.lista_Ids_Alumnos = []
        for tupla in self.ids_Alumnos:
            self.lista_Ids_Alumnos.append(tupla[0])
        self.cmbx_Id_Alumno['values'] = self.ids_Alumnos
        #self.cmbx_Id_Alumno.DropDownStyle=ComboBoxStyle.DropDownList
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
        self.ids_Cursos = self.run_Query("SELECT Código_Curso FROM Cursos")
        self.lista_Ids_Cursos = []
        for tupla in self.ids_Cursos:
            self.lista_Ids_Cursos.append(tupla[0])
        self.cmbx_Id_Curso['values'] = self.ids_Cursos
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

        # Adición automática de nombres y apellidos al seleccionar un ID
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.change_Full_Name)
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.change_Course)

        ''' Botones  de la Aplicación'''
        #Botón Consultar
        ruta_Lupa  = self.dir_pro + "\\img\\lupa.png"
        self.img = PhotoImage(file=ruta_Lupa)
        self.btnConsultar = ttk.Button(self.frm_1, name="btnconsultar", image=self.img)
        self.btnConsultar.place(anchor="nw", x=20, y=15)
        self.btnConsultar.bind("<1>", lambda _:self.action_btnconsultar())
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=260)
        self.btnGuardar.bind("<1>", lambda _:self.action_Button('G'))
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)
        self.btnEditar.bind("<1>", lambda _:self.action_Button('Ed'))
        self.id = -1 # Índice para saber si el programa está guardando (INSERT) o editando (UPDATE)
        self.prev_Course = "" # Variable para guardar el curso original al oprimir el botón Editar
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=260)
        self.btnEliminar.bind("<1>", lambda _:self.action_Button('El'))
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=260)
        self.btnCancelar.bind("<1>", lambda _:self.action_Button('C'))
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        self.create_Treeview("Inscritos")

        # Main widget
        self.mainwindow = self.win

    '''A partir de este punto se deben incluir las funciones para el manejo de la base de datos...'''
    def run(self):
        self.mainwindow.mainloop()    

    '''================================================================================================================'''      
    '''Funciones para validar información en la base de datos'''
    def campo_Existente(self, tabla, campo_1, campo_2):
        """
        Checks if a given field value already exists in a specified table.

        Args:
            campo (str): The field value to check.
            tabla (str): The table to search in.

        Returns:
            bool: True if the field value exists in the table, False otherwise.
        """
        query = f"SELECT COUNT(*) FROM {tabla} WHERE Id_Alumno = '{campo_1}' AND Código_Curso = '{campo_2}'"
        result = self.run_Query(query)
        count = result[0][0]
        return count > 0
    
    def horario_Existente(self, alumno, dias, horario):
        """
        Checks if a given student already has a given scheduel (days + times).
        
        Args:
            alumno (str): The student id.
            dias (str): The schedule days.
            horario (str): The schedule time.
        
        Returns:
            bool: True if the student already has a course with the given schedule, False otherwise.
        """
        query = f"SELECT COUNT(*) FROM Inscritos WHERE Id_Alumno = '{alumno}' AND Horario = '{dias + " " + horario}'"
        result = self.run_Query(query)
        count = result[0][0]
        return count > 0
    
    # To be checked... (NOT IN USE)
    def inscrito_Existente(self, id_Alumno):
        query = f"SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = '{id_Alumno}'"
        result = self.run_Query(query)
        if len(result) > 0:
            numero_inscripcion = result[0][0]
            return numero_inscripcion
        else:
            return None

    def valida_Fecha(self, event=None):     
            if event.char.isdigit() or event.char == '':
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

    def fecha_Valida(self):
        try: 
            day, month, year = map(int, self.fecha.get().split('/'))
            datetime(year, month, day)
            return True
        except ValueError: 
            messagebox.showerror('Error!!','.. ¡Fecha equivocada! por favor corrijala ..')
            return False   

    '''================================================================================================================'''      
    '''Funciones relacionadas al manejo de base de datos y la información mostrada en la interfaz del programa'''
    def run_Query(self, query, parameters=()):
        """
        Executes the given SQL query with optional parameters and returns the result.

        Args:
            query (str): The SQL query to execute.
            parameters (tuple): Optional parameters to be used in the query.

        Returns:
            result: The result of the query execution.
        """
        ruta_db = self.dir_pro + "\\db\\Inscripciones.db"
        with sqlite3.connect(ruta_db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result.fetchall()

    def change_Full_Name(self, event=None):
        """
        Retrieves the full name of a student based on their ID and updates the corresponding entry fields.

        Args:
            event: The event object triggered by the user action.

        Returns:
            None
        """
        id_Alumno = self.cmbx_Id_Alumno.get()
        nombres_Alumno = self.run_Query(f"SELECT Nombres FROM Alumnos WHERE Id_Alumno = '{id_Alumno}'")
        apellidos_Alumno = self.run_Query(f"SELECT Apellidos FROM Alumnos WHERE Id_Alumno = '{id_Alumno}'")
        self.nombres.configure(state = "normal")
        self.apellidos.configure(state = "normal")
        self.nombres.delete(0, 'end')
        self.apellidos.delete(0, 'end')
        self.nombres.insert(0, nombres_Alumno[0][0])
        self.apellidos.insert(0, apellidos_Alumno[0][0])
        self.nombres.configure(state = "readonly")
        self.apellidos.configure(state = "readonly")

    def change_Course(self, event=None):
        """
        Retrieves the full name of a student based on their ID and updates the corresponding entry fields.

        Args:
            event: The event object triggered by the user action.

        Returns:
            None
        """
        id_Curso = self.cmbx_Id_Curso.get()
        descripcion = self.run_Query(f"SELECT Descrip_Curso FROM Cursos WHERE Código_Curso = '{id_Curso}'")
        hora = self.run_Query(f"SELECT Num_Horas FROM Cursos WHERE Código_Curso = '{id_Curso}'")
        self.descripc_Curso.configure(state = "normal")
        self.descripc_Curso.delete(0, 'end')
        self.descripc_Curso.insert(0, descripcion[0][0])
        self.descripc_Curso.configure(state = "readonly")
    
    '''================================================================================================================'''      
    '''Función para botón Consultar (<Lupa>)'''
    def action_btnconsultar(self):
        self.ventana_btnconsultar = tk.Tk()
        self.ventana_btnconsultar.configure(background="#f7f9fd", height=200, width=300)
        alto=200
        ancho=250
        self.ventana_btnconsultar.eval('tk::PlaceWindow . center')
        self.ventana_btnconsultar.geometry(str(ancho)+"x"+str(alto))
        self.ventana_btnconsultar.resizable(False,False)
        self.ventana_btnconsultar.title('Consultar')
        ruta_ventana_btnconsultar = path.dirname(__file__)
        ruta_ventana_btnconsultar += "\\img\\lupa.ico"
        self.ventana_btnconsultar.iconbitmap(bitmap=ruta_ventana_btnconsultar)

        #Botones de la ventana consultar

        self.btnconsultar_alumnos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_alumnos")
        self.btnconsultar_alumnos.configure(text='Listado de alumnos')
        self.btnconsultar_alumnos.place(anchor="nw", x=75, y=25)
        self.btnconsultar_alumnos.bind("<1>", lambda _:self.create_Treeview("Alumnos"))

        self.btnconsultar_carreras = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_carreras")
        self.btnconsultar_carreras.configure(text='Listado de carreras')
        self.btnconsultar_carreras.place(anchor="nw", x=75, y=75)
        self.btnconsultar_carreras.bind("<1>", lambda _:self.create_Treeview("Carreras"))

        self.btnconsultar_cursos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_cursos")
        self.btnconsultar_cursos.configure(text='Listado de cursos')
        self.btnconsultar_cursos.place(anchor="nw", x=75, y=125)
        self.btnconsultar_cursos.bind("<1>", lambda _:self.create_Treeview("Cursos"))

    '''================================================================================================================'''      
    '''Funciones auxiliares al botón Guardar (G)'''
    def check_Entries(self):
        """
        Checks if the needed entries to sign up a student are filled. Furthermore, it checks is the date is valid, if the student hasn't
        already been signed up in a course and if the student doesn't have any other course at the same schedule (days + hours).

        Args:
            None
        
        Returns:
            bool: False if any of the needed entries is empty or the previous mentioned conditions aren't met; True if everything is
            alright in order to sign up the student.
        """
        # Verifica que todos los campos estén llenos
        entries_To_Check = [self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get(), self.fecha.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()]
        for entry in entries_To_Check:
            if entry == "":
                self.show_Error_Empty_Entries()
                return False
        # Verifica que la fecha sea válida, que el estudiante no haya sido inscrito en ese curso anteriormente y que no haya sido inscrito en otro curso con el mismo horario
        if not self.fecha_Valida() or self.campo_Existente("Inscritos", self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()) or self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
            return False
        return True

    def show_Error_Empty_Entries(self):
        """
        Shows an error message indicating the empty entries that need to be filled in order to save correctly.

        Args:
            None
        
        Returns:
            None
        """
        entries = {"Id Alumno":self.cmbx_Id_Alumno.get(), "Id Curso":self.cmbx_Id_Curso.get(), "Fecha":self.fecha.get(), "Horario (Días)":self.cmbx_Dias.get(), "Horario (Hora)":self.cmbx_Horario.get()}
        missing_entries = []
        for i in range(len(entries)):
            if list(entries.values())[i] == "":
                missing_entries.append(list(entries.keys())[i])
        mensaje = "Faltan campos por llenar: " + ", ".join(missing_entries)
        messagebox.askretrycancel(title="Error al guardar", message=mensaje)
    
    '''================================================================================================================'''      
    '''Función para manejar botones Guardar (G), Cancelar (C), Eliminar (El) y Editar (Ed)'''
    def action_Button(self, option) :
        match  option:
            case 'G':
                # Para guardar nueva entrada...
                if self.id == -1:
                    if self.check_Entries():
                        day, month, year = map(str, self.fecha.get().split('/'))
                        self.run_Query(f"INSERT INTO Inscritos (Id_Alumno, Fecha_Inscripción, Código_Curso, Horario) VALUES ('{self.cmbx_Id_Alumno.get()}', '{year}-{month}-{day}', '{self.cmbx_Id_Curso.get()}', '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}')")
                        self.create_Treeview("Inscritos")
                        ids_No_Inscripcion = self.run_Query("SELECT No_Inscripción FROM Inscritos DESC")
                        self.cmbx_No_Inscripcion['values'] = ids_No_Inscripcion
                        messagebox.showinfo(title="Bueno", message="Guardado con éxito")
                    else:
                        if self.campo_Existente("Inscritos", self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()):
                            messagebox.askretrycancel(title="Error al intentar guardar", message="Ya existe una inscripción con esos datos")
                        elif self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
                            messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                # Para editar...
                else :
                    # Para editar solo el horario...
                    if str(self.prev_Course) == self.cmbx_Id_Curso.get():
                        if not(self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get())):
                            self.run_Query(f"UPDATE Inscritos SET Código_Curso = '{self.cmbx_Id_Curso.get()}', Horario = '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}' WHERE No_Inscripción = {self.id}")
                            self.create_Treeview("Inscritos")
                            messagebox.showinfo(title="Confirmación", message="Se ha editado la entrada con éxito.")
                        else:
                            messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                    # Para editar curso (y horario)...
                    else:           
                        if not(self.campo_Existente("Inscritos", self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get())) or not(self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get())):
                            #day, month, year = map(str, self.fecha.get().split('/'))
                            self.run_Query(f"UPDATE Inscritos SET Código_Curso = '{self.cmbx_Id_Curso.get()}', Horario = '{self.cmbx_Dias.get() + ' ' + self.cmbx_Horario.get()}' WHERE No_Inscripción = {self.id}")
                            self.create_Treeview("Inscritos")
                            messagebox.showinfo(title="Confirmación", message="Se ha editado la entrada con éxito.")
                        else:
                            if self.campo_Existente("Inscritos", self.cmbx_Id_Alumno.get(), self.cmbx_Id_Curso.get()):
                                messagebox.askretrycancel(title="Error al intentar guardar", message="Ya existe una inscripción con esos datos")
                            elif self.horario_Existente(self.cmbx_Id_Alumno.get(), self.cmbx_Dias.get(), self.cmbx_Horario.get()):
                                messagebox.askretrycancel(title="Error al intentar guardar", message="El alumno ya tiene un curso en ese horario")
                    # Para volver a la normalidad...
                    self.id = -1
                    self.prev_Course = ""
                    self.cmbx_Id_Alumno.configure(state='readonly')
                    self.fecha.configure(state='normal')
                    self.clear_Entrys("datos_Todo")
            
            case 'Ed':
                selected = self.tView.focus()
                clave = self.tView.item(selected,'text')
                if clave == '':
                    messagebox.showwarning("Editar", 'Debes selecccionar un elemento.')
                else:
                    respuesta = messagebox.askyesno(title="Editar", message="Desea editar")
                    if respuesta:
                        info = self.tView.item(selected)
                        self.clear_Entrys("datos_Curso")
                        self.insert_Course(info['text'],info['values'][2])
                        self.id = clave
                        self.prev_Course = info['values'][2]
                        self.cmbx_Id_Alumno.configure(state='disable')
                        self.fecha.configure(state='readonly')

            case 'El':
                selected = self.tView.focus()
                clave = self.tView.item(selected,'text')
                if clave == '':
                    messagebox.showwarning("Eliminar", 'Debes selecccionar un elemento.')
                else:
                    respuesta = messagebox.askyesno(title="Eliminar", message="Desea eliminar")
                    if respuesta:     
                        try:
                            numero_Inscrito = self.seleccionar_Dato(event=None)
                            self.run_Query(f"DELETE FROM Inscritos WHERE No_Inscripción = {numero_Inscrito}")
                            self.create_Treeview("Inscritos")
                            ids_No_Inscripcion = self.run_Query("SELECT No_Inscripción FROM Inscritos DESC")
                            self.cmbx_No_Inscripcion['values'] = ids_No_Inscripcion
                            messagebox.showinfo(title="Bueno", message="Eliminado con éxito")

                        except sqlite3.OperationalError:
                            None
            case 'C':
                respuesta = messagebox.askyesno(title="Cancelar", message="Desea cancelar")
                if respuesta:
                    self.cmbx_Id_Alumno.configure(state='readonly')
                    self.fecha.configure(state='normal')
                    self.clear_Entrys("datos_Todo")

    '''================================================================================================================'''      
    '''Funciones para manejar TreeViews'''
    def create_Treeview(self, type):
        if type in ["Carreras", "Cursos", "Alumnos"]: # Elimina ventana emergente y treeView anterior
            self.ventana_btnconsultar.destroy()
            self.delete_Treeview()
        
        # Crear Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        
        # Verifica el tipo de tabla para crear el TreeView correspondiente
        match type:
            case "Inscritos":
                """
                Creates the correponding TreeView for the table Inscritos.
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
                self.tView.heading("tV_codigo", anchor="w", text='Codigo de Curso')
                self.tView.heading("tV_horario", anchor="w", text='Horario')
                self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
                self.tView.bind('<ButtonRelease-1>', self.seleccionar_Dato)
                #Configura los datos de la tabla
                query = self.run_Query("SELECT * FROM Inscritos ORDER BY No_Inscripción DESC")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4]))
            
            case "Carreras":
                """
                Creates the correponding TreeView for the table Carreras.
                """
                #Columnas del Treeview
                self.tView_cols = ['tV_Descripcion', 'tV_semestres']
                self.tView_dcols = ['tV_Descripcion', 'tV_semestres']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
                self.tView.column("tV_Descripcion",anchor="w",stretch=True,width=100,minwidth=50)
                self.tView.column("tV_semestres",anchor="w",stretch=True,width=200,minwidth=50)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='Codigo de Carrera')
                self.tView.heading("tV_Descripcion", anchor="w", text='Descripcion')
                self.tView.heading("tV_semestres", anchor="w", text='No de semestres')
                self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
                #Configura los datos de la tabla
                query = self.run_Query("SELECT * FROM Carreras")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2],))
            
            case "Cursos":
                """
                Creates the correponding TreeView for the table Cursos.
                """
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
                self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
                #Configura los datos de la tabla
                query = self.run_Query("SELECT * FROM Cursos")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2]))
            
            case "Alumnos":
                """
                Creates the correponding TreeView for the table Alumnos.
                """
                #Columnas del Treeview
                self.tView_cols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
                self.tView_dcols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
                self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
                self.tView.column("#0",anchor="w",stretch=True,width=100,minwidth=10)
                self.tView.column("tV_id_carrera",anchor="w",stretch=True,width=100,minwidth=50)
                self.tView.column("tV_nombres",anchor="w",stretch=True,width=150,minwidth=50)
                self.tView.column("tV_apellidos", anchor="w", stretch=True, width=150, minwidth=50)
                #Cabeceras
                self.tView.heading("#0", anchor="w", text='Id Alumno')
                self.tView.heading("tV_id_carrera", anchor="w", text='Id Carrera')
                self.tView.heading("tV_nombres", anchor="w", text='Nombres')
                self.tView.heading("tV_apellidos", anchor="w", text='Apellidos')
                self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
                # Columna 3 en adelante...
                self.headers = ['Fecha de Inscripción', 'Dirección', 'Tel. Celular', 'Tel. Fijo', 'Ciudad', 'Departamento']
                for i in range(0, len(self.headers)) :
                    self.tView.column(self.tView_cols[i+3], anchor="w", stretch=True, width=125, minwidth=20)
                    self.tView.heading(self.tView_dcols[i+3], anchor="w", text=self.headers[i])
                #Configura los datos de la tabla
                query = self.run_Query("SELECT * FROM Alumnos")
                for i in query:
                    self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
     
        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h", command=self.tView.xview)
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=780, x=400, y=595)
        self.tView['xscrollcommand'] = self.scroll_H.set
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y", command=self.tView.yview)
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.tView['yscrollcommand'] = self.scroll_Y.set
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

    def delete_Treeview(self):
        """
        Deletes the current TreeView shown in the frame.

        Args:
            None
        
        Returns:
            None
        """
        self.tView.delete(*self.tView.get_children())
        self.tView.destroy()

    def seleccionar_Dato(self, event):
        """
        Select a data from the TViewInscritos
        
        Args:
            None
        
        Returns:
            Id_Alumno
        """
        try:
            item_Seleccionado = self.tView.item(self.tView.focus()) 
            numero_inscripcion = item_Seleccionado["text"]
            return numero_inscripcion
        except IndexError:
            messagebox.showerror(title="Error al eliminar", message="No escogió ningún dato de la tabla")

    '''Función para insertar campos curso'''
    def insert_Course(self,num_Inscripcion, id_Curso):
        query= f"SELECT * FROM Inscritos WHERE No_Inscripción = {num_Inscripcion} AND Código_Curso = '{id_Curso}'"
        result=self.run_Query(query)
        result=list(result[0])
        fecha=result[2].split("-")
        newfecha=str(fecha[2])+'/'+str(fecha[1])+'/'+str(fecha[0])
        self.fecha.insert(0,newfecha)
        result.pop(2)
        horario=result[3].split(" ")
        dia = " ".join(horario[:3])
        hora = " ".join(horario[3:])
        result[3]=dia
        result.append(hora)
        entries = [self.cmbx_Id_Alumno, self.cmbx_Id_Curso, self.cmbx_Dias, self.cmbx_Horario]
        lists = [self.lista_Ids_Alumnos, self.lista_Ids_Cursos, self.horarios_Dias, self.horarios_Horas]
        for i in range(len(entries)):
            entries[i].current(lists[i].index(result[i+1]))
        self.change_Full_Name()
        self.change_Course()
        

    '''Función para limpiar campos'''
    def clear_Entrys(self,vaciar):
        match vaciar:
            case "datos_Alumno":
                self.cmbx_Id_Alumno.set("")
                self.nombres.configure(state = "normal")
                self.apellidos.configure(state = "normal")
                self.nombres.delete(0, "end")
                self.apellidos.delete(0, "end")
                self.nombres.configure(state = "readonly")
                self.apellidos.configure(state = "readonly")
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
                self.nombres.configure(state = "readonly")
                self.apellidos.configure(state = "readonly")
                self.descripc_Curso.configure(state = "readonly")
                self.cmbx_Horario.set("")
                self.cmbx_Dias.set("")
                self.cmbx_No_Inscripcion.set("")
                self.fecha.delete(0, "end")
    '''================================================================================================================'''      
    '''Funciones archivadas'''
    #def clean_String(string):
    #    return string.replace('{', '').replace('}', '')

# ================================================================================================================
if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()

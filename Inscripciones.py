# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import PhotoImage
import os
import sqlite3

class Inscripciones_2:   
    def __init__(self, master=None):
        self.db_name = 'Inscripciones.db'
        # Renovación de tabla Inscritos al iniciar el programa
        self.run_Query("DROP TABLE IF EXISTS Inscritos")
        self.run_Query("CREATE TABLE Inscritos (No_Inscripción INTEGER PRIMARY KEY AUTOINCREMENT, Id_Alumno VARCHAR(20) NOT NULL, Fecha_Inscripción DATE NOT NULL, Código_Curso VARCHAR(20) NULL, FOREIGN KEY (Código_Curso) REFERENCES Cursos(Código_Curso))")
        # Ventana principal    
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd", height=600, width=800)
        alto=600
        ancho=800
        self.win.eval('tk::PlaceWindow . center')
        self.win.geometry(str(ancho)+"x"+str(alto))
        #x = self.win.winfo_screenwidth()
        #y = self.win.winfo_screenheight()
        #self.win.geometry(str(ancho)+"x"+str(alto)+"+"+str((round((x/2)-(ancho/2))))+"+"+str((round((y/2)-(alto/2)))))
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        ruta = os.path.dirname(__file__)
        ruta += "\\img\\icon.ico"
        self.win.iconbitmap(bitmap=ruta)
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        #Label No. Inscripción
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="center",state="normal",
                                        takefocus=False,text='No.Inscripción')
        #Botón Consultar
        ruta_Lupa = os.path.dirname(os.path.abspath(__file__))
        ruta_Lupa  += "\\img\\lupa.png"
        self.img = PhotoImage(file=ruta_Lupa)
        self.btnConsultar = ttk.Button(self.frm_1, name="btnconsultar", image=self.img)
        self.btnConsultar.place(anchor="nw", x=20, y=15)
        self.btnConsultar.bind("<1>", lambda _:self.action_btnconsultar())
        #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        #Entry No. Inscripción
        self.num_Inscripcion = ttk.Entry(self.frm_1, name="num_inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)
        #Entry Fecha
        def validar_fecha(fecha_ingresada):
            if len(fecha_ingresada) > 10:
                messagebox.showerror(message="La fecha ingresada no puede superar los 8 dígitos", title="Error al ingresar fecha")
                return False
            if fecha_ingresada.isdigit():
                return True
            else:
                messagebox.showerror(message="La fecha ingresada no puede contener letras", title="Error al ingresar fecha")
            letras = 0
            for i in fecha_ingresada:
                letras += 1
            if letras == 2:self.fecha.insert(2, '/')
            if letras == 5:self.fecha.insert(6, '/')
        self.fecha = ttk.Entry(self.frm_1, name="fecha", validate="key", validatecommand=(self.win.register(validar_fecha), "%P"))
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        ids_Alumnos = self.run_Query("SELECT Id_Alumno FROM Alumnos")
        self.cmbx_Id_Alumno['values'] = ids_Alumnos
        #Label Nombres
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)
        #Entry Nombres
        self.nombres = ttk.Entry(self.frm_1, name="nombres")
        self.nombres.place(anchor="nw", width=200, x=100, y=130)
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
        #Entry Curso
        self.id_Curso = ttk.Entry(self.frm_1, name="id_curso")
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=185)
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)
        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)
        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        # Adición automática de nombres y apellidos al seleccionar un ID
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.change_Full_Name)

        ''' Botones  de la Aplicación'''
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=260)
        self.btnGuardar.bind("<1>", lambda _:self.action_Button('G'))
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)
        #self.btnEditar.bind("<1>", self.action_Button('Ed'))
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=260)
        #self.btnEliminar.bind("<1>", self.action_Button('El'))
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=260)
        #self.btnCancelar.bind("<1>", self.action_Button('C'))
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        self.treeview_Cursos()


        # Main widget
        self.mainwindow = self.win

    def run(self):
        self.mainwindow.mainloop()

    ''' A partir de este punto se deben incluir las funciones
    para el manejo de la base de datos '''

    def run_Query(self, query, parameters=()):
        """
        Executes the given SQL query with optional parameters and returns the result.

        Args:
            query (str): The SQL query to execute.
            parameters (tuple): Optional parameters to be used in the query.

        Returns:
            result: The result of the query execution.
        """
        ruta_db = os.path.dirname(__file__)
        ruta_db += "\\db\\Inscripciones.db"
        with sqlite3.connect(ruta_db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result.fetchall()

    def change_Full_Name(self, event):
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
    
    #Metodo botón consultar
    
    def action_btnconsultar(self):
        self.ventana_btnconsultar = tk.Tk()
        self.ventana_btnconsultar.configure(background="#f7f9fd", height=200, width=300)
        alto=200
        ancho=250
        self.ventana_btnconsultar.eval('tk::PlaceWindow . center')
        self.ventana_btnconsultar.geometry(str(ancho)+"x"+str(alto))
        self.ventana_btnconsultar.resizable(False,False)
        self.ventana_btnconsultar.title('Consultar')
        ruta_ventana_btnconsultar = os.path.dirname(__file__)
        ruta_ventana_btnconsultar += "\\img\\lupa.ico"
        self.ventana_btnconsultar.iconbitmap(bitmap=ruta_ventana_btnconsultar)

        #Botones de la ventana consultar

        self.btnconsultar_alumnos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_alumnos")
        self.btnconsultar_alumnos.configure(text='Listado de alumnos')
        self.btnconsultar_alumnos.place(anchor="nw", x=75, y=25)
        self.btnconsultar_alumnos.bind("<1>", lambda _:self.treeview_Alumnos())

        self.btnconsultar_carreras = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_carreras")
        self.btnconsultar_carreras.configure(text='Listado de carreras')
        self.btnconsultar_carreras.place(anchor="nw", x=75, y=75)
        self.btnconsultar_carreras.bind("<1>", lambda _:self.treeview_Carreras())

        self.btnconsultar_cursos = ttk.Button(self.ventana_btnconsultar, name="btnconsultar_cursos")
        self.btnconsultar_cursos.configure(text='Listado de cursos')
        self.btnconsultar_cursos.place(anchor="nw", x=75, y=125)
        self.btnconsultar_cursos.bind("<1>", lambda _:self.treeview_Cursos())


    #Metodo botón

    def action_Button(self, option) :
        match  option:
            case 'G':
                self.run_Query(f"INSERT INTO Inscritos (Id_Alumno, Fecha_Inscripción, Código_Curso) VALUES ('{self.cmbx_Id_Alumno.get()}', '{self.fecha.get()}', '{self.id_Curso.get()}')")
                self.treeview_Inscritos()
            case _:
                print("Adios")


    '''================================================================================================================'''      
    '''Funciones para crear TreeViews'''
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

    def treeview_Cursos(self):
        #self.ventana_btnconsultar.destroy()
        """
        Creates the correponding TreeView to show the table Cursos.
        
        Args:
            None
        
        Returns:
            None
        """
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_id_alumno', 'tV_fecha_inscripcion']
        self.tView_dcols = ['tV_id_alumno', 'tV_fecha_inscripcion']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_id_alumno",anchor="w",stretch=True,width=150,minwidth=50)
        self.tView.column("tV_fecha_inscripcion",anchor="w",stretch=True,width=50,minwidth=10)
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Curso')
        self.tView.heading("tV_id_alumno", anchor="w", text='Descripción')
        self.tView.heading("tV_fecha_inscripcion", anchor="w", text='Horas')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        #configura los datos de la tabla
        query = self.run_Query("SELECT * FROM Cursos")
        for i in query:
            self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2]))
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
    
    def treeview_Inscritos(self):
        """
        Creates the correponding TreeView to show the table Inscritos.
        
        Args:
            None
        
        Returns:
            None
        """
        self.delete_Treeview()
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción', 'tV_horas', 'tV_codigo']
        self.tView_dcols = ['tV_descripción', 'tV_horas', 'tV_codigo']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        self.tView.column("tV_horas",anchor="w",stretch=True,width=50,minwidth=10)
        self.tView.column("tV_codigo",anchor="w",stretch=True,width=100,minwidth=10)
        
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='No. Inscripción')
        self.tView.heading("tV_descripción", anchor="w", text='Id Alumno')
        self.tView.heading("tV_horas", anchor="w", text='Fecha de Inscripción')
        self.tView.heading("tV_codigo", anchor="w", text='Codigo de Curso')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        #configura los datos de la tabla
        query = self.run_Query("SELECT * FROM Inscritos")
        for i in query:
            self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2], i[3]))
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
        
    def treeview_Carreras(self):
        self.ventana_btnconsultar.destroy()
        """
        Creates the correponding TreeView to show the table Carreras.
        
        Args:
            None
        
        Returns:
            None
        """
        self.delete_Treeview()
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
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
        #configura los datos de la tabla
        query = self.run_Query("SELECT * FROM Carreras")
        for i in query:
            self.tView.insert(parent="", index= 0, text=i[0], values=(i[1], i[2],))
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
    
    def treeview_Alumnos(self):
        self.ventana_btnconsultar.destroy()
        """
        Creates the correponding TreeView to show the table Alumnos.
        
        Args:
            None
        
        Returns:
            None
        """
        self.delete_Treeview()
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
        self.tView_dcols = ['tV_id_carrera', 'tV_nombres', 'tV_apellidos', 'tV_fecha_inscripcion', 'tV_dirección', 'tV_telef_celu', 'tV_telef_fijo', 'tV_ciudad', 'tV_departamento']
        self.headers = ['Fecha de Inscripción', 'Dirección', 'Tel. Celular', 'Tel. Fijo', 'Ciudad', 'Departamento']
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
        for i in range(0, len(self.headers)) :
            self.tView.column(self.tView_cols[i+3], anchor="w", stretch=True, width=125, minwidth=20)
            self.tView.heading(self.tView_dcols[i+3], anchor="w", text=self.headers[i])
        #configura los datos de la tabla
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

    '''Funciones archivadas'''
    #def clean_String(string):
    #    return string.replace('{', '').replace('}', '')

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()

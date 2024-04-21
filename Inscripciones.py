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
<<<<<<< HEAD
        #Botón Consultar
        ruta_Lupa = os.path.dirname(os.path.abspath(__file__))
        ruta_Lupa  += "\\img\\lupa.png"
        self.img = PhotoImage(file=ruta_Lupa)
        self.btnConsultar = ttk.Button(self.frm_1, name="btnconsultar", image=self.img)
        self.btnConsultar.place(anchor="nw", x=20, y=15)
        #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
=======
>>>>>>> d6aa4ec01dc4835b4c3a2a19b3202b0ecd14d248
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
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=260)
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=260)
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción']
        self.tView_dcols = ['tV_descripción']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Descripción')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        #configura los datos de la tabla
        query = self.run_Query("SELECT * FROM cursos")
        for i in query:
            self.tView.insert(parent="", index= 0, text=i[0], values=(i[1],))
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
    
    def delete_Treeview(self):
        for i in self.tView.get_children():
            self.tView.delete(i)

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

    #def clean_String(string):
    #    return string.replace('{', '').replace('}', '')

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()

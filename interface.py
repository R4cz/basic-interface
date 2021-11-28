import tkinter as tk
from tkinter import ttk

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface")
        self.root.config( background= "#27272a")
        self.root.resizable( 0, 0)
            
        self.users_creation()
        self.combobox_users()
        self.delivery_creation()
        self.hours_creation()
        self.buttons_creation()
        
        self.root.mainloop()
    #FRONTEND

    # Crea los usuarios que utilizaremos como ejemplo, usando la clase User.
    # Los agrupamos en una lista para, luego, crear la lista desplegable (Combobox).
    def users_creation(self):
        self.users_list = []
        for x in range(1, 10):
            user = User(f"User {x}")
            self.users_list.append(user)
    # Crea la lista desplegable para que podamos seleccionar al usuario deseado y así
    # poder demostrar el uso de la aplicación más fácilmente.
    def combobox_users(self):
        self.selected_user = tk.StringVar()
        self.combobox_users_list = ttk.Combobox( self.root, textvariable=self.selected_user, values=self.users_list, state="readonly", width=15, font="Nunito 14 normal")
        self.combobox_users_list.grid( column=0, row=5, padx=10, pady=10, columnspan=5)
        self.combobox_users_list.current(0)
        self.combobox_users_list.bind( "<<ComboboxSelected>>", self.user_selection)
    # Crea una lista que contiene la cantidad de bikes disponibles para cada horario.
    # Luego la ordenamos con el método auxiliar, y así tener la forma con la que serán
    # creados los botones.
    def delivery_creation(self):
        delivery_list = []
        for x in range( 1, 26):
            delivery = 8
            delivery_list.append(delivery)
        self.ordered_delivery_list = self.ordering(delivery_list)
    # Crea los horarios requeridos y los añade a una lista para luego ser ordenados por
    # el método auxiliar, y así tener la misma forma con la que serán creados los botones.
    def hours_creation(self):
        hours_list = []
        for x in range( 8, 21):
            hours_list.append( str(x)+":00")
            if x != 20:
                hours_list.append( str(x)+":30")
        self.ordered_hours_list = self.ordering(hours_list)
    # AUXILIARY METHOD
    # Ordena la lista brindada para que tenga la misma forma que la lista de botones.
    def ordering(self, lista):
        ordered_list = []
        list = []
        x = 0
        for row in range(5):
            for column in range(5):
                list.append(lista[x])
                x = x+1
            ordered_list.append(list)
            list = []
        return ordered_list
    # Crea: cinco filas y cada fila contiene cinco columnas, de botones.
    def buttons_creation(self):
        self.buttons_table = []
        table_row = []
        for row in range( 0, 5):
            for column in range( 0, 5):
                button = tk.Button(self.root, text=self.ordered_hours_list[row][column]+"\nAvailable bikes:\n"+str(self.ordered_delivery_list[row][column]), command=lambda fi=row, co=column: self.operate(fi,co), font="Nunito 14 normal", bg="#18181b", fg="#ffffff", relief="flat")
                button.grid( column=column, row=row, padx=6, pady=6)
                table_row.append( button)
            self.buttons_table.append( table_row)
            table_row = []
    # BACKEND

    # Permite actualizar el título de la ventana y el estado de los botones, de acuerdo
    # al usuario seleccionado.
    def user_selection(self, event):
        for x in range( 1, 10):
            if self.selected_user.get() == f"User {x}":
                self.root.title(f"Interface - User {x}")
                self.user_state(x)
    # Comprobamos cuál usuario fué seleccionado y creamos la variable "take" que nos
    # proporciona el estado del "interruptor" de un determinado botón. El botón lo
    # ubicamos con ayuda de "fi" y "co" que nos brinda la fila y columna respectivamente.
    # También enviamos la cantidad de bikes disponibles en dicho interruptor (horario).
    
    # Si el "interruptor" devuelve el valor de True; quiere decir que SI estaba encendido
    # por lo cual la acción que ejecuta el método es "liberar" el recurso tomado (liberar
    # el bike) y aumentar, en uno, el número de bikes disponibles para determinado horario.

    # Si el "interruptor" devuelve el valor de False; quiere decir que NO estaba encendido
    # por lo cual la acción que ejecuta el método es "tomar" un recurso y reducir la 
    # cantidad de bikes, de dicho horario.
    def operate( self, fi, co):
        for x in range( 1, 10):
            if self.selected_user.get() == f"User {x}":
                take = self.users_list[x-1].user_take( fi, co, self.ordered_delivery_list[fi][co])
                if take == True:
                    self.ordered_delivery_list[fi][co] = self.ordered_delivery_list[fi][co] + 1
                    self.buttons_table[fi][co].configure( text=self.ordered_hours_list[fi][co]+"\nAvailable bikes:\n"+str(self.ordered_delivery_list[fi][co]))
                    self.user_state(x)
                elif take == False:
                    self.ordered_delivery_list[fi][co] = self.ordered_delivery_list[fi][co] - 1
                    self.buttons_table[fi][co].configure( text=self.ordered_hours_list[fi][co]+"\nAvailable bikes:\n"+str(self.ordered_delivery_list[fi][co]))
                    self.user_state(x)
    # Una vez brindado el usuario, pintamos el botón de acuerdo a la cantidad de bikes
    # disponibles.

    # Si los bikes disponibles, de un determinado horario, llegan a cero; el botón se
    # pintará de rojo.

    # Si los bikes disponibles son diferentes a cero en determinado horario, se pintará
    # de color verde o gris según el estado del "interruptor" de determinado usuario.
    # Verde para encendido y gris para apagado.
    def user_state(self, x):
        for row in range( 0, 5):
            for column in range( 0, 5):
                if self.ordered_delivery_list[row][column] != 0:
                    if self.users_list[x-1].take_list[row][column] == True:
                        self.buttons_table[row][column].configure(bg="#5dc1b9", fg="#18181b")
                    elif self.users_list[x-1].take_list[row][column] == False:
                        self.buttons_table[row][column].configure(bg="#18181b", fg="#ffffff")
                elif self.ordered_delivery_list[row][column] == 0:
                    self.buttons_table[row][column].configure(bg="#cd212a")

class User:
    # Cuando creamos un Usuario, le brindamos el nombre y también se crea un "interruptor"
    # para cada horario, el cual por defecto esta en Off, que nos permite saber si el
    # usuario tomó o no la bike de dicho horario.
    def __init__(self, name):
        self.name = name
        self.take_list = []
        list = []
        for row in range( 0, 5):
            for column in range( 0, 5):
                take = False
                list.append(take)
            self.take_list.append(list)
            list = []
    # Permite que podamos acceder/identificar al objeto a través del nombre proporcionado.
    def __str__(self):
        return self.name
    # Cambia el estado del "interruptor" entre On y Off.

    # Cualquiera podrá tomar un recurso de bike, siempre y cuando el número de bikes
    # disponibles en ese horario sea diferente de cero.

    # Así mismo cualquiera podrá "liberar" el recurso tomado sin importar la cantidad de
    # bikes disponibles, siempre y cuando haya tomado uno.
    def user_take(self, fi , co, delivery):
        if self.take_list[fi][co] == False and delivery != 0:
            self.take_list[fi][co] = True
            return False
        elif self.take_list[fi][co] == True:
            self.take_list[fi][co] = False
            return True
# MAIN BLOCK
app1 = App()
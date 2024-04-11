import tkinter as tk
import threading
import tkinter.messagebox as messagebox
import scrap

def main(nombre_bd, cantidad_filas):
    try:
        scrap.crear_bd_y_tabla(nombre_bd)
        datos_nuevos = scrap.scrape_datos(cantidad_filas)
        scrap.insertar_datos(datos_nuevos, nombre_bd)
        messagebox.showinfo("Información", "Datos insertados correctamente en la base de datos. Se terminó de hacer el scraping.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def iniciar_scraping():
    nombre_bd = entry_nombre_bd.get()
    cantidad_filas = entry_cantidad_filas.get()
    cantidad_filas = int(cantidad_filas) if cantidad_filas else None
    threading.Thread(target=main, args=(nombre_bd, cantidad_filas)).start()

root = tk.Tk()
root.title("ATT-SCRAPING")

# Centrar la ventana
window_width = 500
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

root.configure(bg='white')

frame = tk.Frame(root, bg='white')
frame.pack(expand=True, padx=20, pady=20)


label_nombre_bd = tk.Label(frame, text="Nombre de la base de datos:", bg='white', font=('Arial', 20))
label_nombre_bd.pack(pady=10)
entry_nombre_bd = tk.Entry(frame, font=('Arial', 20))
entry_nombre_bd.pack()

label_cantidad_filas = tk.Label(frame, text="Cantidad de filas a insertar:", bg='white', font=('Arial', 20))
label_cantidad_filas.pack(pady=10)
entry_cantidad_filas = tk.Entry(frame, font=('Arial', 20))
entry_cantidad_filas.pack()

button = tk.Button(frame, 
                   text="Iniciar Scraping", 
                   command=iniciar_scraping,
                   bg='blue',  
                   fg='white',  
                   font=('Arial', 20)  
                   )
button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()

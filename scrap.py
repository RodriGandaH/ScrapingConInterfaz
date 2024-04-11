import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


def crear_bd_y_tabla(nombre_bd):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="asdf",
        host="localhost",
        port="5432"
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    # Verificar si la base de datos existe y crearla si no existe
    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()
    if (nombre_bd,) not in list_database:
        cur.execute(f"CREATE DATABASE {nombre_bd}")

    conn.close()

    # Conectar a la base de datos recién creada
    conn = psycopg2.connect(
        dbname=nombre_bd,
        user="postgres",
        password="asdf",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    # Crear la tabla si no existe
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tarifas_online(
        id serial not null,
        operador text, 
        departamento text, 
        nombre_tarifa text,
        velocidad_bajada float,
        precio_bs float,
        tipo_conexion text,
        UNIQUE (operador, departamento, nombre_tarifa, velocidad_bajada, precio_bs, tipo_conexion)
            );
        """)


    conn.commit()
    cur.close()
    conn.close()



def scrape_datos(cantidad_filas=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo'

    try:
        driver.get(url)
    

        select_element = driver.find_element(By.TAG_NAME, 'select')
        select = Select(select_element)
        select.select_by_value('-1')  # valor del select 
      

        tabla = driver.find_element(By.TAG_NAME, 'table')
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        datos = []
        for fila in filas[1:cantidad_filas]:
            celdas = fila.find_elements(By.TAG_NAME, 'td')
            dato1 = celdas[0].text
            dato2 = celdas[1].text
            dato3 = celdas[2].text
            dato4 = celdas[3].text
            dato5 = celdas[4].text 
            dato6 = celdas[5].text     
            datos.append((dato1, dato2, dato3, dato4, dato5, dato6))

        return datos

    finally:
        driver.quit()

def insertar_datos(datos, nombre_bd):
    conn = psycopg2.connect(
        dbname=nombre_bd,
        user="postgres",
        password="asdf",
        host="localhost",
        port="5432"
    )

    try:
        cur = conn.cursor()
        for dato in datos:
            cur.execute("""
                        INSERT INTO tarifas_online(operador, departamento, nombre_tarifa, velocidad_bajada, precio_bs, tipo_conexion) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (operador, departamento, nombre_tarifa, velocidad_bajada, precio_bs, tipo_conexion) DO NOTHING
                        """, dato)

        conn.commit()
    finally:
        cur.close()
        conn.close()

def main():
    nombre_bd = input("Ingrese el nombre de la base de datos: ")
    cantidad_filas = input("Ingrese la cantidad de filas a insertar (deje vacío para insertar todas): ")
    cantidad_filas = int(cantidad_filas) if cantidad_filas else None

    try:
        crear_bd_y_tabla(nombre_bd)
        datos_nuevos = scrape_datos(cantidad_filas)
        insertar_datos(datos_nuevos, nombre_bd)
        print("Datos insertados correctamente en la base de datos. Se terminó de hacer el scraping.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

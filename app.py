from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import pyodbc

# Inicializar la aplicación FastAPI
app = FastAPI()


# Configuración de la conexión a la base de datos
def f_conn(username):
    server = "bd-enmascaramiento.database.windows.net"
    database = "bd_prospectos"
    password = "Password123#"

    # Cadena de conexión
    conn_str = (
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    return conn_str


# Montar la ruta de los archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Asegúrate de tener un directorio llamado "templates" donde se encuentren tus archivos HTML.
templates = Jinja2Templates(directory="templates")

# Diccionario para almacenar el nombre de usuario asociado a cada sesión
session_usernames = {}


# Decorador para la ruta de inicio de sesión
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    # Renderizar la plantilla HTML login.html
    return templates.TemplateResponse("login.html", {"request": request})


# Definición de la ruta para el inicio de sesión
@app.post("/admin/login")
async def admin_login_post(
    request: Request, txtUsuario: str = Form(...), txtPassword: str = Form(...)
):
    # Verificar las credenciales ingresadas por el usuario
    if txtUsuario == "user_admin_01" and txtPassword == "user_admin_01":
        # Si las credenciales son para un administrador, establecer el nombre de usuario y el tipo de usuario
        username = "user_admin01"
        tiUsuario = "A"
    elif txtUsuario == "user_developer_01" and txtPassword == "user_developer_01":
        # Si las credenciales son para un desarrollador, establecer el nombre de usuario y el tipo de usuario
        username = "user_developer_01"
        tiUsuario = "U"
    else:
        # Manejar la autenticación fallida
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Obtener el ID de sesión del cliente desde las cookies de la solicitud
    session_id = request.cookies.get("session_id")

    # Asocia el nombre de usuario con el ID de sesión en el diccionario
    session_usernames[session_id] = {"username": username, "tiUsuario": tiUsuario}

    # Redirige al usuario a la página de menú con el parámetro tiUsuario
    return templates.TemplateResponse(
        "menu_sistema.html", {"request": request, "tiUsuario": tiUsuario}
    )


# Definición de la ruta para mostrar la lista de prospectos
@app.get("/lista_prospecto", response_class=HTMLResponse)
async def lista_prospecto(request: Request):
    # Obtener el ID de sesión del cliente desde las cookies de la solicitud
    session_id = request.cookies.get("session_id")

    # Obtener la información de la sesión del diccionario session_usernames utilizando el ID de sesión
    session_info = session_usernames.get(session_id, {})

    # Obtener los datos de sesión (nombre de usuario y tipo de usuario) del diccionario session_info
    username = session_info.get("username")
    tiUsuario = session_info.get("tiUsuario")

    # Conectar a la base de datos
    try:
        conn = pyodbc.connect(f_conn(username))
        cursor = conn.cursor()
        # Consulta SQL para obtener todos los registros de prospectos
        query = "SELECT * FROM tb_prospectos"
        cursor.execute(query)
        # Obtener todos los resultados de la consulta
        v_rs_person = cursor.fetchall()

        # Renderizar la plantilla HTML lista_prospecto.html con los datos obtenidos
        return templates.TemplateResponse(
            "lista_prospecto.html",
            {"request": request, "tiUsuario": tiUsuario, "v_rs_person": v_rs_person},
        )
    except Exception as e:
        print(f"Error connecting to the database: {e}")


# Definición de la ruta para mostrar el formulario de registro de prospecto
@app.get("/r_prospecto", response_class=HTMLResponse)
async def guardar_persona(request: Request):
    # Renderizar la plantilla HTML registro_prospecto.html
    return templates.TemplateResponse("registro_prospecto.html", {"request": request})


# Definición de la ruta para guardar los datos del formulario de registro de prospecto
@app.post("/r_prospecto")
async def guardar_persona(request: Request):
    # Obtener los datos del formulario enviado
    form_data = await request.form()
    # Obtener los valores de cada campo del formulario
    co_docide = form_data.get("co_docide")
    no_apepat = form_data.get("no_apepat")
    no_apemat = form_data.get("no_apemat")
    no_nombre = form_data.get("no_nombre")
    ti_genero = form_data.get("ti_genero")
    fe_nacimi = form_data.get("fe_nacimi")
    no_correo = form_data.get("no_correo")
    nu_telefo = form_data.get("nu_telefo")
    no_direcc = form_data.get("no_direcc")

    # Query de inserción
    query = "INSERT INTO tb_prospectos (co_docide, no_apepat, no_apemat, no_nombre, ti_genero, fe_nacimi, no_correo, nu_telefo, de_direcc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Conectar a la base de datos
    try:
        conn = pyodbc.connect(f_conn("user_admin01"))
        cursor = conn.cursor()

        # Ejecutar la consulta con los valores del formulario
        cursor.execute(
            query,
            (
                co_docide,
                no_apepat,
                no_apemat,
                no_nombre,
                ti_genero,
                fe_nacimi,
                no_correo,
                nu_telefo,
                no_direcc,
            ),
        )

        # Hacer commit para guardar los cambios en la base de datos
        conn.commit()

        # Cerrar la conexión y el cursor
        cursor.close()
        conn.close()

        return templates.TemplateResponse(
            "registro_prospecto.html", {"request": request}
        )
    except Exception as e:
        print(f"Error connecting to the database: {e}")

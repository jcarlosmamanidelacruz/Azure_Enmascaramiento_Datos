# Proyecto de Enmascaramiento de Datos con Azure SQL Database y FastAPI
[![logo-enmascaramiento-datos-Azure.png](https://i.postimg.cc/DwmBGMpD/logo-enmascaramiento-datos-Azure.png)](https://postimg.cc/XrSfSQbc)
## Introducción

Este proyecto es una aplicación web desarrollada con el objetivo de demostrar la implementación de enmascaramiento de datos dinámicos utilizando Azure SQL Database y FastAPI. El enmascaramiento de datos es una técnica crucial para proteger la privacidad y seguridad de la información sensible almacenada en bases de datos, permitiendo a los usuarios acceder solo a los datos necesarios para su función, mientras se ocultan los datos sensibles.

## Objetivo

El objetivo principal de este proyecto es mostrar cómo una aplicación web puede interactuar con usuarios con diferentes niveles de acceso y conocimientos técnicos, mientras garantiza la privacidad de los datos sensibles. Para ello, se implementará un sistema de registro de usuarios y visualización de datos, donde los usuarios prospecto podrán registrarse en la aplicación, mientras que los usuarios Admin y Desarrollador tendrán diferentes niveles de acceso a los datos.

## Herramientas Utilizadas

- Python: Se utilizará Python como lenguaje de programación principal para el desarrollo de la lógica de la aplicación y la implementación de las APIs utilizando FastAPI.

- SQL Database: Se utilizará como base de datos principal para almacenar los datos de usuarios. Se implementará el enmascaramiento dinámico de datos para proteger la privacidad de los usuarios.

- FastAPI: Se utilizará FastAPI, un framework de desarrollo web rápido (fast), para implementar las APIs que manejarán las solicitudes de registro de usuarios y la visualización de datos.

- HTML y JavaScript: Se utilizará HTML para diseñar y desarrollar los formularios web que permitirán a los usuarios prospecto registrarse en la aplicación. Además, se utilizará JavaScript para implementar la lógica de los endpoints de las APIs, incluyendo la gestión de solicitudes y respuestas.

## Caso Práctico

En este caso práctico, se simulará el registro de usuarios en adelante prospectos en una aplicación web y la visualización de datos para diferentes roles de usuario:

- Los usuarios prospecto podrán registrarse en la aplicación proporcionando sus datos personales.

- Los usuarios Admin tendrán acceso completo a todos los datos de los usuarios registrados.

- Los usuarios Desarrollador solo podrán acceder a datos enmascarados, garantizando la privacidad de los datos sensibles.

## Descripción y Desarrollo Técnico

#### Creación de la Base de Datos en Azure SQL Database

- Para crear la base de datos en Azure SQL Database, sigue estos pasos:

- Inicia sesión en el Portal de Azure.

- Crear un grupo de recursos para empaquetar nuestros servicios de azure

- Crea una nueva instancia de Azure SQL Database.

- Añadir al FireWall nuestra ip para acceder a la base de datos.

- Define la estructura de la tabla de prospectos, especificando qué campos serán enmascarados dinámicamente.

- Configura las reglas de enmascaramiento dinámico de datos según los requisitos de privacidad y seguridad de tu aplicación.

- Creación de usuarios con roles de administrador y rol de acceso a datos de solo lectura.

## Crear un grupo de recursos

En este paso, creará un grupo de recursos.

1.- En el menú de la izquierda, seleccione Grupo de recursos y luego Crear.

[![Grupo-de-Recursos.png](https://i.postimg.cc/1Xw6hnCY/Grupo-de-Recursos.png)](https://postimg.cc/zHD3TB1n)

2.- Asignamos un nombre al grupo de recursos y seleccionamos la región, para este caso será 

3.- Revisamos y damos crear.

[![creacion-grupo-recursos.png](https://i.postimg.cc/qMmvj9G1/creacion-grupo-recursos.png)](https://postimg.cc/PPwHqV9D)

## Crear una base de datos de SQL Database.

1.- Para ello nos vamos al inicio y seleccionamos SQL Database.

[![creacion-sql-database.png](https://i.postimg.cc/j2pML7Qz/creacion-sql-database.png)](https://postimg.cc/2LxQt3t6)

2.- Seleccionamos el grupo de recursos creado anteriormente.

3.- Añadimos un nombre a la base de datos para este caso se bd_prospectos

4.- Creamos un servidor, en donde le asignamos el nombre y seleccionamos la ubicación, para estos casos será: bd-enmascaramiento, US 2 respectivamente.

5.- Seleccionamos Use SQL authentication en el método de autentificación, asignamos el nombre del administrador como la contraseña que vamos a utilizar, para este caso server_admin y la contraseña de su elección, damos a ok.

[![creacion-server.png](https://i.postimg.cc/J7JfwN3r/creacion-server.png)](https://postimg.cc/F1rW3Jn8)

6.- Configuramos el tipo de almacenamiento y seleccionamos el Standard y damos a aplicar.

[![tipo-almacenamiento.png](https://i.postimg.cc/HstPdHSn/tipo-almacenamiento.png)](https://postimg.cc/svvJJFCC)

7.- Seleccionamos Locally-redundant backup storage, el mínimo nivel de redundancia.

8.- Damos a Review + create.

[![create-sql-database.png](https://i.postimg.cc/nV2PtpSz/create-sql-database.png)](https://postimg.cc/w3tVX8p8)

## Añadir al FireWall nuestra ip para acceder a la base de datos.

1.- Nos dirigimos a Overview, dentro de nuestro servicio de base de datos.

2.- Vamos a la pestaña de Ser server firewall

3.- Agregamos nuestra ip en la sección Add client IP y damos Save.

[![firewall-ip-add.png](https://i.postimg.cc/fL82hvWL/firewall-ip-add.png)](https://postimg.cc/r0tC1xrX)

## Definición de estructura de la tabla de prospectos y su enmascaramiento.

1.- Nos dirigimos a la opción Query editor.

2.- Ingresamos el usuario y password que creamos para Use SQL authentication.

3.- Damos en Ok.

[![autentificacion-sql.png](https://i.postimg.cc/QdRk1yC1/autentificacion-sql.png)](https://postimg.cc/yDyZznF8)

4.- En un Query editor copiamos el siguiente script, en el cual estamos encriptando los datos del correo, teléfono y dirección.

		CREATE TABLE [dbo].[tb_prospectos] (
			[co_prospe] INT NOT NULL IDENTITY(1,1),
			[fe_regist] DATETIME2(0) NOT NULL DEFAULT GETDATE(),
			[co_docide] VARCHAR(10) NOT NULL,
			[no_apepat] VARCHAR(200) NOT NULL,
			[no_apemat] VARCHAR(200) NOT NULL,
			[no_nombre] VARCHAR(200) NOT NULL,
			[ti_genero] VARCHAR(1) NOT NULL,
			[fe_nacimi] DATE,
			[no_correo] VARCHAR(200) MASKED WITH (FUNCTION = 'partial(1, "XXXXXXX", 0)') NOT NULL,
			[nu_telefo] VARCHAR(200) MASKED WITH (FUNCTION = 'default()') NOT NULL,
			[de_direcc] VARCHAR(200) MASKED WITH (FUNCTION = 'partial(1, "XXXXXXX", 0)') NOT NULL,
			PRIMARY KEY ([co_prospe])
		);

5.- Realizamos la inserción de un registro.

		INSERT INTO tb_prospectos (
			[co_docide],
			[no_apepat],
			[no_apemat],
			[no_nombre],
			[ti_genero],
			[fe_nacimi],
			[no_correo],
			[nu_telefo],
			[de_direcc]
		)
		VALUES (
			'44477258',
			'Mamani',
			'de la Cruz',
			'Juan Carlos',
			'M',
			'1987-03-30',
			'jmamanidelacruz@gmail.com',
			'989280804',
			'Urb. la Florida, SMP'
		);

## Crear usuarios para la base de datos

La administración de usuarios de Windows Azure es un poco complicada y, desafortunadamente, no hay forma de agregar usuarios a la base de datos existente mediante el portal de administración de Microsoft Azure.

Para agregar un nuevo usuario a la base de datos existente en windows azure haremos lo siguiente:

1.- Iniciaremos sesión a la base de datos a través de SQL Server Management Studio con el usuario y contraseña que definimos al momento de crear el servicio de Azure SQL DataBase.

- En server name copiamos el que nos brinda el servicio de Azure SQL Database al momento de crear nuestra base de datos.

[![sesion-SQL-Management.png](https://i.postimg.cc/bwsCqZkK/sesion-SQL-Management.png)](https://postimg.cc/v4wLzHPz)

2.- Procedemos a crear los usuarios, con el siguiente comando SQL, verificando que estamos en la base de datos master.

		-- BD master
		CREATE LOGIN user_admin_01  WITH PASSWORD = 'Password123#';
		CREATE USER user_admin_01  FOR LOGIN user_admin_01;

		-- BD master
		CREATE LOGIN user_developer_01  WITH PASSWORD = 'Password123#';
		CREATE USER user_developer_01  FOR LOGIN user_developer_01;


[![create-user-db-Master.png](https://i.postimg.cc/k4Q9w15F/create-user-db-Master.png)](https://postimg.cc/njh6h1BC)

3.- Ejecutamos el siguiente comando SQL en la base de datos bd_prospectos:

		-- Asignamos el rol db_owner
		EXEC sp_addrolemember N'db_owner', N'user_admin_01';
		
		-- Asignamos el rol db_datareader
		EXEC sp_addrolemember N'db_datareader', N'user_developer';

[![create-user-db-prospectos.png](https://i.postimg.cc/ncMghStR/create-user-db-prospectos.png)](https://postimg.cc/VdQD7Rvn)

4.- Ahora para efectos de verificar el enmascaramiento de los datos, ingresaremos con los usuarios creados, para realizar un select a la tabla y verificar el enmascaramiento de los datos.

- Ingresando con el usuario: user_admin_01

[![sesion-SQL-user-admin.png](https://i.postimg.cc/7ZjfWRqp/sesion-SQL-user-admin.png)](https://postimg.cc/bZHyG3DT)

- Realizamos el query con el usuario user_admin_01 y verificamos que tiene acceso a los datos desenmascarado.

		SELECT * FROM tb_prospectos;

[![sesion-SQL-user-admin-select.png](https://i.postimg.cc/QdbCmMHn/sesion-SQL-user-admin-select.png)](https://postimg.cc/TKKTYfjr)

Ingresando con el usuario: user_developer_01

[![sesion-SQL-user-developer.png](https://i.postimg.cc/VLf3MLPN/sesion-SQL-user-developer.png)](https://postimg.cc/DmNj3hZV)

- Realizamos el query con el usuario user_developer_01 y verificamos que tel resultado de la consulta devuelve los dato enmascarados.

		SELECT * FROM tb_prospectos;
[![sesion-SQL-user-developer-select.png](https://i.postimg.cc/SxzMk9N2/sesion-SQL-user-developer-select.png)](https://postimg.cc/bZpJRsnp)

## Creación de la Aplicación Web en Python

#### Estructura de carpetas del proyecto

El proyecto está estructurado en tres directorios principales:

- Static/Css: Contiene los archivos CSS de Bootstrap utilizados para dar estilo a la interfaz de usuario de la aplicación.

- Templates: Aquí se encuentran los archivos HTML que se utilizan para la interfaz de usuario de la aplicación. Estos archivos HTML renderizan la salida de las API creadas con FastAPI.

- Venv: Este directorio contiene el entorno virtual de Python utilizado para aislar las dependencias del proyecto.

- app.py: Este archivo contiene toda la lógica implementada para las API, incluyendo los métodos GET, POST para interactuar con la base de datos y manejar las solicitudes de los clientes.

- requirements.txt contiene una lista de todas las dependencias y versiones de Python necesarias para ejecutar la aplicación. Estas dependencias se instalan automáticamente utilizando la herramienta pip, lo que facilita la configuración del entorno de desarrollo.

[![estructura-proyecto.png](https://i.postimg.cc/hGB48KjZ/estructura-proyecto.png)](https://postimg.cc/JspWMVjj)

#### Descripción de Archivos HTML

En este proyecto, se utilizan varios archivos HTML para proporcionar la interfaz de usuario y la funcionalidad de registro y visualización de datos. A continuación, se describe el propósito de cada archivo HTML:

1. login.html
El archivo login.html se utiliza para la autenticación de usuarios Admin y Developer en el sistema. Proporciona un formulario de inicio de sesión donde los usuarios pueden ingresar sus credenciales para acceder a la aplicación.

2. menu_sistema.html
El archivo menu_sistema.html es responsable de mostrar el menú del sistema, que varía según el tipo de usuario que haya iniciado sesión. Dependiendo de los privilegios del usuario (Admin o Developer), este archivo determina qué opciones de menú estarán disponibles.

3. registro_prospecto.html
registro_prospecto.html es el formulario de registro que se encuentra públicamente disponible para cualquier persona que desee registrar sus datos en la aplicación. Este formulario permite a los prospectos ingresar su información personal para registrarse en el sistema.

4. lista_prospecto.html
En el archivo lista_prospecto.html, se muestra un informe que contiene la lista de prospectos registrados en el sistema. Además, este archivo se encarga de aplicar el enmascaramiento de datos según los niveles de acceso del usuario que haya iniciado sesión. Por lo tanto, los datos sensibles se muestran de forma enmascarada según los permisos del usuario.


Para iniciar el desarrollo de la aplicación, primero configuraremos el entorno de desarrollo y luego procederemos con la implementación de la lógica de la aplicación utilizando Python y FastAPI. A continuación, se detallan los pasos a seguir:

1.- Clona este repositorio en tu máquina local:

	 git clone https://github.com/jcarlosmamanidelacruz/xxx.git

2.- Activa el entorno virtual:

	 venv\Scripts\activate

3.- Instalar Dependencias

Una vez activado el entorno virtual, instala las dependencias del proyecto:

	pip install -r requirements.txt

4.- Ejecutar la Aplicación

Para ejecutar la aplicación, utiliza el siguiente comando:

	uvicorn app:app --reload

## Capturas de Código Python:

Este código implementa las rutas necesarias para el inicio de sesión de usuarios administradores y desarrolladores:

#### Método GET para la Página de Inicio de Sesión

La primera ruta, asociada al método GET en la raíz "/", se encarga de mostrar la página de inicio de sesión cuando se accede al sistema. Retorna la plantilla HTML login.html, que contiene el formulario de inicio de sesión.

#### Método POST para la Autenticación del Usuario Administrador

La segunda ruta, definida con el método POST en "/admin/login", maneja el envío del formulario de inicio de sesión por parte de los usuarios administradores. Verifica las credenciales ingresadas por el usuario. Si son correctas, se establece una sesión para el usuario y se lo redirige a la página de menú correspondiente. En caso de credenciales incorrectas, devuelve un error HTTP 401.

Este código asegura un proceso de inicio de sesión eficiente y seguro para los usuarios administradores y desarrolladores del sistema.

[![metodo-get-login.png](https://i.postimg.cc/Ssxb82gy/metodo-get-login.png)](https://postimg.cc/qtSFHRfY)

#### Método POST  de Guardado de Datos de Prospecto

Este fragmento de código define una ruta para guardar los datos de un nuevo prospecto en la base de datos cuando se envía un formulario. Recibe los datos del formulario, los procesa y los inserta en la base de datos utilizando una consulta SQL de inserción. Si la inserción es exitosa, se redirige al usuario a la página de registro de prospecto nuevamente.

[![post-registo-prospecto.png](https://i.postimg.cc/3Jjwhp0R/post-registo-prospecto.png)](https://postimg.cc/TpwxqK9M)

#### Método GET para la Lista de Prospectos

Este código define una ruta para mostrar una lista de prospectos registrados en el sistema. Utiliza la información de sesión del usuario para determinar el acceso y luego recupera los datos de la base de datos. La lista de prospectos se muestra en la página utilizando la plantilla HTML lista_prospecto.html.

[![get-lista-prospectos.png](https://i.postimg.cc/vm2FM8vD/get-lista-prospectos.png)](https://postimg.cc/sBW04rqR)

#### Capturas de Interfaz de Usuario de la Aplicación

Formulario de Inicio de Sesión (login.html)

[![sesion-SQL-user-admin-html.png](https://i.postimg.cc/kX8m8tQm/sesion-SQL-user-admin-html.png)](https://postimg.cc/zVJ6Yv2t)

Menú del Sistema (menu_sistema.html) - usuario administrador

[![menu-sistema-admin.png](https://i.postimg.cc/7ZWnkbR5/menu-sistema-admin.png)](https://postimg.cc/xXLzGjnQ)

Menú del Sistema (menu_sistema.html) - usuario desarrollador

[![menu-sistema-desarrollador.png](https://i.postimg.cc/hGwrnhfC/menu-sistema-desarrollador.png)](https://postimg.cc/XZfFcjKF)

Formulario de Registro de Prospecto (registro_prospecto.html)

[![post-registo-prospecto-html.png](https://i.postimg.cc/4dc2Ypc7/post-registo-prospecto-html.png)](https://postimg.cc/gXYH5XNm)

Lista de Prospectos Registrados (lista_prospecto.html)  - usuario administrador

[![get-lista-prospectos-administrador.png](https://i.postimg.cc/QCwMfGtn/get-lista-prospectos-administrador.png)](https://postimg.cc/ct7ZJzfQ)

Lista de Prospectos Registrados (lista_prospecto.html)  - usuario desarrollador

[![get-lista-prospectos-desarrollador.png](https://i.postimg.cc/Y094Xzxj/get-lista-prospectos-desarrollador.png)](https://postimg.cc/TLzY1mFX)

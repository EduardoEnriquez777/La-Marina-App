Sistema de Gestión LA MARINA

Plataformas:
Python 3.8 o superior | MySQL 8.0 | Interfaz gráfica desarrollada con Tkinter

---

REQUISITOS DEL SISTEMA

- Tener instalado Python 3.8 o versiones más recientes

- Contar con un servidor MySQL 8.0 funcionando correctamente

---

PASOS PARA LA INSTALACIÓN

(SE NECESITA INSTALAR LA FUENTE Genova.ttf)

1. Crea un entorno virtual con el siguiente comando:
python -m venv 23270641



2. Activa el entorno virtual de acuerdo a tu sistema operativo:
- En Windows:

  23270641\Scripts\actívate


- En Linux o MacOS:

  source 23270641/bin/activate




3. Procede a instalar las librerías necesarias con:

pip install -r extras.txt




4. Instalar Pillow para el entorno virtual:

python.exe -m pip install pillow



---

PRIMEROS PASOS PARA CONFIGURAR EL PROYECTO

Importar la base de datos llamada LaMarina_db.sql



Instalar Base de datos: Usando MySQL Workbench:

1. Abre MySQL Workbench y conéctate al servidor.
2. Selecciona la opción "Server" y luego "Data Import".
3. Escoge "Import from Self-Contained File".
4. Busca y selecciona el archivo LaMarina_db.sql.
5. Elige la base de datos padrino_db como destino.
6. Haz clic en "Start Import" para comenzar la importación.

---

EJECUTAR LA APLICACIÓN

Para iniciar el sistema, abre una terminal y ejecuta:


python main.py



---


PRINCIPALES CARACTERÍSTICAS

- Interfaz gráfica moderna y amigable desarrollada con Tkinter
- Diseño adaptable a diferentes resoluciones (responsive)
- Validación automática para asegurar la integridad de los datos
- Funcionalidad avanzada de búsqueda en todos los módulos
- Exportación de datos en formatos PDF y Excel para facilitar análisis
- Panel principal (dashboard) interactivo para monitoreo rápido

---

SOLUCIONES A PROBLEMAS FRECUENTES

Problemas al instalar o usar tkcalendar:
pip install --upgrade pip
pip install tkcalendar

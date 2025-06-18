import os
import sys
from logging.config import fileConfig

# --- SECCIÓN DE DIAGNÓSTICO DE RUTAS ---
print("DEBUG: env.py - Inicio del script.")
print(f"DEBUG: env.py - __file__ es: {__file__}")

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"DEBUG: env.py - project_root_dir calculado: {project_root_dir}")

if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)
    print(f"DEBUG: env.py - project_root_dir AÑADIDO a sys.path.")
else:
    print(f"DEBUG: env.py - project_root_dir YA ESTABA en sys.path.")

print(f"DEBUG: env.py - sys.path ACTUAL: {sys.path}")

# --- PRUEBA DE IMPORTACIÓN DIRECTA DE db.base EN env.py ---
try:
    print("DEBUG: env.py - Intentando: from db.base import Base as EnvBase")
    from app.db.base import Base as EnvBase
    print("DEBUG: env.py - ÉXITO al importar db.base como EnvBase.")
    print(f"DEBUG: env.py - EnvBase importado es: {EnvBase}")
except ImportError as e:
    print(f"DEBUG: env.py - FALLO al importar db.base directamente: {e}")
    print("DEBUG: env.py - Por favor, verifica que db/__init__.py y db/base.py existen y son accesibles.")
    raise # Detener si esto falla, ya que es fundamental

# --- IMPORTACIÓN DE app.models (QUE CAUSA EL PROBLEMA ORIGINAL) ---
try:
    print("DEBUG: env.py - Intentando: from app.models import *")
    # Aquí es donde ocurre el error según tu traceback anterior al importar app.models.currency
    # que a su vez intenta 'from db.base import Base'
    from app.models import *
    print("DEBUG: env.py - ÉXITO al importar from app.models import *")
except ImportError as e:
    print(f"DEBUG: env.py - FALLO al importar from app.models import *: {e}")
    # Si el error es 'No module named db' originado desde currency.py, es el problema central
    raise
except Exception as e:
    print(f"DEBUG: env.py - OCURRIÓ OTRO ERROR durante from app.models import *: {e}")
    raise

# --- CONFIGURACIÓN ESTÁNDAR DE ALEMBIC ---
from sqlalchemy import pool
from alembic import context
# Usa la Base importada exitosamente como EnvBase
target_metadata = EnvBase.metadata

# Interpretar el archivo de configuración para logging de Python.
# Esta línea asume que config.config_file_name ya está establecido.
config_obj = context.config # Renombrado para evitar conflicto con logging.config
if config_obj.config_file_name is not None:
    fileConfig(config_obj.config_file_name)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
        # literal_binds=True # Mantenlo comentado o elimínalo si no usas --sql
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    from sqlalchemy.ext.asyncio import create_async_engine # Importación local
    connectable = create_async_engine(
        config_obj.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    import asyncio # Importación local
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    print("DEBUG: env.py - Ejecutando en modo offline.")
    url = config_obj.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    print("DEBUG: env.py - Ejecutando en modo online.")
    run_migrations_online()

print("DEBUG: env.py - Fin del script.")
from sqlalchemy.exc import SQLAlchemyError
from model import SessionLocal

def consultar_todos(modelo):
    try:
        db = SessionLocal()
        return db.query(modelo).all()
    except SQLAlchemyError as e:
        raise e
    finally:
        db.close()

def agregar_registro(modelo, data):
    try:
        db = SessionLocal()
        nuevo = modelo(**data)
        db.add(nuevo)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()

def actualizar_registro(modelo, clave_primaria: dict, nuevos_datos: dict):
    try:
        db = SessionLocal()
        obj = db.query(modelo).filter_by(**clave_primaria).first()
        if obj:
            for clave, valor in nuevos_datos.items():
                setattr(obj, clave, valor)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()

def eliminar_registro(modelo, clave_primaria: dict):
    try:
        db = SessionLocal()
        obj = db.query(modelo).filter_by(**clave_primaria).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()

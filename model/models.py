from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Enum, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# Enums personalizados
class EstadoAlmacenEnum(enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class ActivoEnum(enum.Enum):
    Si = "Sí"
    No = "No"

# Modelo: almacen
class Almacen(Base):
    __tablename__ = 'almacen'

    idalmacen = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False, unique=True)
    ubicacion = Column(String(45), nullable=False)
    capacidad_maxima = Column(Integer, nullable=False)
    estado = Column(Enum(EstadoAlmacenEnum), nullable=False)

    def __repr__(self):
        return f"<Almacen(idalmacen={self.idalmacen}, nombre='{self.nombre}')>"

# Modelo: caja
class Caja(Base):
    __tablename__ = 'caja'

    idcaja = Column(Integer, primary_key=True, autoincrement=True)
    saldo_inicial = Column(DECIMAL(10, 2), nullable=False)
    fecha_apertura = Column(DateTime, nullable=False)
    saldo_final = Column(DECIMAL(10, 2), nullable=False)
    fecha_cierre = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Caja(idcaja={self.idcaja}, fecha_apertura='{self.fecha_apertura}', fecha_cierre='{self.fecha_cierre}')>"

# Modelo: cliente
class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    telefono = Column(String(20))
    correo = Column(String(100))
    direccion = Column(String(200))

    def __repr__(self):
        return f"<Cliente(id_cliente='{self.id_cliente}', nombre='{self.nombre}', apellido='{self.apellido}')>"

# Modelo: sucursal
class Sucursal(Base):
    __tablename__ = 'sucursal'

    id_sucursal = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    direccion = Column(String(45), nullable=False)
    ciudad = Column(String(45), nullable=False)
    estado = Column(String(45), nullable=False)
    codigo_postal = Column(String(45), nullable=False)
    telefono = Column(String(45), nullable=False, unique=True)

    empleados = relationship("Empleado", back_populates="sucursal")

    def __repr__(self):
        return f"<Sucursal(id_sucursal={self.id_sucursal}, nombre='{self.nombre}')>"

# Modelo: empleado
class Empleado(Base):
    __tablename__ = 'empleado'

    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    apellido = Column(String(45), nullable=False)
    cargo = Column(String(45), nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    salario = Column(DECIMAL(10, 0), nullable=False)
    id_sucursal = Column(Integer, ForeignKey('sucursal.id_sucursal', ondelete='CASCADE'), nullable=False)

    sucursal = relationship("Sucursal", back_populates="empleados")

    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado}, nombre='{self.nombre}', apellido='{self.apellido}')>"

# Modelo: metodo_pago
class MetodoPago(Base):
    __tablename__ = 'metodo_pago'

    idmetodo_pago = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(100))
    activo = Column(Enum('Sí','No'), nullable=False)
    
    def __repr__(self):
        return f"<MetodoPago(idmetodo_pago={self.idmetodo_pago}, nombre='{self.nombre}')>"

# Modelo: proveedor
class Proveedor(Base):
    __tablename__ = 'proveedor'

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    telefono = Column(String(45), nullable=False, unique=True)
    correo = Column(String(45), nullable=False, unique=True)
    direccion = Column(String(45), nullable=False)

    def __repr__(self):
        return f"<Proveedor(id_proveedor={self.id_proveedor}, nombre='{self.nombre}')>"
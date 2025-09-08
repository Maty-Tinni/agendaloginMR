from typing import Any, Optional
import pymysql as db
from pymysql.cursors import DictCursor
from constante import ADB

class AccesoDB:
    __coneccion : db.Connection|None = None
    
    def __init__(self, host : str, user : str, password :str, database : str) -> None:
        if AccesoDB.__coneccion is None:
            AccesoDB.__coneccion = db.connect(
                                        host=host, 
                                        user=user, 
                                        password=password, 
                                        database=database,
                                        cursorclass=DictCursor) # las consultas devuelven diccionarios

    def consulta_generica(self, consulta : str) -> list[dict[str, Any]]:
        
        cursor = self.__coneccion.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    
    def modificacion_generica(self, query: str) -> int:
        
        cursor : DictCursor = self.__coneccion.cursor()
        resultado = cursor.execute(query)
        cursor.close()
        self.__coneccion.commit()
        return resultado
    

    def obtener(self, tabla: str, columnas: list[str], filtros: Optional[dict[str, str]] = None) \
    -> list[dict[str, Any]]:
        if not columnas:
            raise ValueError("La lista de columnas no puede estar vacía")
        cols = ', '.join(columnas)
        query = f"SELECT {cols} FROM `{tabla}`"
        if filtros:
            condiciones = " AND ".join([f"`{col}` = '{val}'" for col, val in filtros.items()])
            query += f" WHERE {condiciones}"
        return self.consulta_generica(query)
          
    def borrar(self, tabla: str, filtros: dict[str, str]) -> int:
        if not filtros:
            raise ValueError("Se requiere al menos un filtro para borrar registros")
        condiciones = " AND ".join([f"`{col}` = '{val}'" for col, val in filtros.items()])
        query = f"DELETE FROM `{tabla}` WHERE {condiciones}"
        return self.modificacion_generica(query)

    def crear(self, tabla: str, data: dict[str,str]) -> int:
        
        if not data:
            raise ValueError("El diccionario está vació")
        
        columnas = ', '.join(f"`{col}`" for col in data.keys())
        values = ', '.join(f"'{val}'" for val in data.values())    
        consulta = f"INSERT INTO `{tabla}` ({columnas}) VALUES ({values})"
        return self.modificacion_generica(consulta)

    def modificar(self, tabla: str, data: dict[str,str], condicion: tuple[str,str]) -> int:
        """Modifica registros de la base de datos

        Args:
            tabla (str): tabla que contiene los registros a modificar
            data (dict[str,str]): Los datos en formato de diccionario {columna:valor}
            condicion (tuple[str,str]): condición a cumplir para modificar los registros
            del tipo (columna, valor), cuando coincidan se modifica el registro

        Raises:
            ValueError: si los datos o la condición son vacíos

        Returns:
            int: cantidad de registros modificados
        """
        pass

    def __del__(self) -> None:
        if AccesoDB.__coneccion is not None:
            AccesoDB.__coneccion.close()
            AccesoDB.__coneccion = None

if __name__ == '__main__':
    pass
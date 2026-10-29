from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    BASE_DATOS = "mydb" # Pon el nombre exacto de tu base de datos en MySQL Workbench

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password) 
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.BASE_DATOS).query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        resultado = connectToMySQL(cls.BASE_DATOS).query_db(query, data)
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': usuario_id}
        resultado = connectToMySQL(cls.BASE_DATOS).query_db(query, data)
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_registro(usuario):
        es_valido = True
        
        # Validar Nombre
        if len(usuario['nombre'].strip()) < 2 or not usuario['nombre'].isalpha():
            flash("El nombre debe tener al menos 2 letras y solo contener caracteres alfabéticos.", "registro")
            es_valido = False
            
        # Validar Apellido
        if len(usuario['apellido'].strip()) < 2 or not usuario['apellido'].isalpha():
            flash("El apellido debe tener al menos 2 letras y solo contener caracteres alfabéticos.", "registro")
            es_valido = False

        # Validar Email
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Formato de correo electrónico inválido.", "registro")
            es_valido = False
        elif Usuario.obtener_por_email(usuario['email']):
            flash("El correo electrónico ya se encuentra registrado.", "registro")
            es_valido = False

        # Validar Contraseña
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
        elif usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido
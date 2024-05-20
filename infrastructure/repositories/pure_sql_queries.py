import uuid


class PureSqlQueries:
    @staticmethod
    def check_id_in_tables(user_id: uuid.UUID):
        return """SELECT "Administrador"
        FROM ADMINISTRADORES a
        WHERE a.id  = {user_id}
        UNION ALL
        SELECT "Assistente"
        FROM ASSISTENTES a2
        WHERE a2.id = {user_id}
        UNION ALL
        SELECT "Locatario"
        FROM LOCATARIOS l
        WHERE l.d = {user_id}
        SELECT "Prestador_servico"
        FROM LOCATARIOS p
        WHERE p.id = {user_id};"""

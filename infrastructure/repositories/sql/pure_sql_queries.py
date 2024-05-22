import sqlalchemy as sa
import uuid


class PureSqlQueries:
    @staticmethod
    def check_id_in_tables(user_id: uuid.UUID):
        return sa.text(f"""SELECT 'Administrador'
        FROM ADMINISTRADORES a
        WHERE a.id  = {user_id}
        UNION ALL
        SELECT 'Assistente'
        FROM ASSISTENTES a2
        WHERE a2.id = {user_id}
        UNION ALL
        SELECT 'Locatario'
        FROM LOCATARIOS l
        WHERE l.id = {user_id}
        UNION ALL
        SELECT 'Prestador_servico'
        FROM PRESTADORES_SERVICOS p
        WHERE p.id = {user_id};""".replace('\n', ' '))

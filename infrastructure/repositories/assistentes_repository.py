from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.assistentes import Assistentes
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos
from infrastructure.mappers.UsuariosInput import UsuariosInputMapper


class AssistentesRepository:
    def get_all(self) -> list[Assistentes]:
        with Connection() as connection:
            result_user = connection.session.query(Assistentes).all()
            result_identityInfos = connection.session.query(UsuariosIdentityInfos).all()
            result = []
            for user in result_user:
                for idInfo in result_identityInfos:
                    if user.id == idInfo.id:
                        result.append((user,idInfo))
            result_mapped = [UsuariosInputMapper.map_assistente(x) for x in result]
            return result_mapped

    def get_by_id(self, id: UUID) -> Assistentes:
        with Connection() as connection:
            return connection.session.query(Assistentes)\
                .filter(Assistentes.id == id)\
                .first()

    def insert(self, assistente) -> Assistentes:
        with Connection() as connection:
            connection.session.add(assistente)
            connection.session.commit()
            return assistente
    
    def update(self, assistente: Assistentes) -> Assistentes:
        with Connection() as connection:
            connection.session.query(Assistentes).filter(Assistentes.id == str(assistente.id)).update(
                {"nome": assistente.nome,
                 "data_nascimento": assistente.data_nascimento})
            connection.session.commit()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Assistentes).filter(Assistentes.id == id).delete()

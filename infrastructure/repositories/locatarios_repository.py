from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos
from infrastructure.mappers.UsuariosInput import UsuariosInputMapper


class LocatariosRepository:
    def get_all(self) -> list[Locatarios]:
        with Connection() as connection:
            result_user = connection.session.query(Locatarios).all()
            result_identityInfos = connection.session.query(UsuariosIdentityInfos).all()
            result = []
            for user in result_user:
                for idInfo in result_identityInfos:
                    if user.id == idInfo.id:
                        result.append((user,idInfo))
            result_mapped = [UsuariosInputMapper.map_locatario(x) for x in result]
            return result_mapped

    def get_by_id(self, id: UUID) -> Locatarios:
        with Connection() as connection:
            result_user = connection.session.query(Locatarios)\
                .filter(Locatarios.id == id)\
                .first()
            result_identity = connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.id == id)\
                .first()
            locatarios_mapped = UsuariosInputMapper.map_locatario((result_user,result_identity))
            return locatarios_mapped

    def insert(self, locatario: Locatarios) -> Locatarios:
        with Connection() as connection:
            connection.session.add(locatario)
            connection.session.commit()
            return locatario

    def update(self, locatario: Locatarios) -> Locatarios:
        with Connection() as connection:
            connection.session.query(Locatarios).filter(Locatarios.id == str(locatario.id)).update(
                {"nome": locatario.nome,
                 "data_nascimento": locatario.data_nascimento,
                 "celular": locatario.celular})
            connection.session.commit()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(Locatarios).filter(Locatarios.id == str(id)).delete()

from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.mappers.UsuariosInput import UsuariosInputMapper
from infrastructure.models.prestadores_servico import PrestadoresServicos
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos


class PrestadoresServicosRepository:
    def get_all(self) -> list[PrestadoresServicos]:
        with Connection() as connection:
            result_user = connection.session.query(PrestadoresServicos).all()
            result_identityInfos = connection.session.query(UsuariosIdentityInfos).all()
            result = []
            for user in result_user:
                for idInfo in result_identityInfos:
                    if user.id == idInfo.id:
                        result.append((user,idInfo))
            result_mapped = [UsuariosInputMapper.map_prestadorServico(x) for x in result]
            print(result_mapped[0])
            return result_mapped

    def get_by_id(self, id: UUID) -> PrestadoresServicos:
        with Connection() as connection:
            return connection.session.query(PrestadoresServicos)\
                .filter(PrestadoresServicos.id == id)\
                .first()

    def insert(self, assist) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.add(assist)
            return assist

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(PrestadoresServicos.id == id).delete()

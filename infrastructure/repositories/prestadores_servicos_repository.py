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
            return result_mapped

    def get_by_id(self, id: UUID) -> PrestadoresServicos:
        with Connection() as connection:
            return connection.session.query(PrestadoresServicos)\
                .filter(PrestadoresServicos.id == id)\
                .first()

    def insert(self, assist) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.add(assist)
            connection.session.commit()
            return assist

    def update(self, prestador_servico: PrestadoresServicos) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(PrestadoresServicos.id == str(prestador_servico.id)).update(
                {"nome": prestador_servico.nome,
                 "data_nascimento": prestador_servico.data_nascimento,
                 "empresa": prestador_servico.empresa,
                 "especialidade": prestador_servico.especialidade})
            connection.session.commit()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(PrestadoresServicos.id == id).delete()

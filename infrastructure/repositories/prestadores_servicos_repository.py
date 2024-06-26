from typing import Optional
from uuid import UUID
from infrastructure.configs.connection import Connection
from infrastructure.mappers.UsuariosInput import UsuariosInputMapper
from infrastructure.models.prestadores_servico import PrestadoresServicos
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos


class PrestadoresServicosRepository:
    def get_all(self) -> list:
        with Connection() as connection:
            result_user = connection.session.query(PrestadoresServicos).all()
            result_identityInfos = connection.session.query(UsuariosIdentityInfos).all()
            result = []
            for user in result_user:
                for idInfo in result_identityInfos:
                    if user.id == idInfo.id:
                        result.append((user, idInfo))
            result_mapped = [UsuariosInputMapper.map_prestadorServico(x) for x in result]
            return result_mapped

    def __convert_to_uuid(self, id_str_or_uuid):
        if isinstance(id_str_or_uuid, str):
            return id_str_or_uuid

        if isinstance(id_str_or_uuid, UUID):
            # Remove 'UUID('...'')' wrapper and extract the UUID part
            id_str = str(id_str_or_uuid).split('UUID(')[-1].split(')')[0]
            return id_str

        raise ValueError(f"Invalid ID format: {id_str_or_uuid}")

    def get_name_by_id(self, id_str_or_uuid) -> Optional[str]:
        id_uuid = self.__convert_to_uuid(id_str_or_uuid)

        with Connection() as connection:
            prestador = connection.session.query(PrestadoresServicos).filter_by(id=id_uuid).first()
            return prestador.nome if prestador else None

    def get_by_id(self, id: UUID) -> PrestadoresServicos:
        with Connection() as connection:
            result_user = connection.session.query(PrestadoresServicos) \
                .filter(PrestadoresServicos.id == id) \
                .first()
            result_identity = connection.session.query(UsuariosIdentityInfos)\
                .filter(UsuariosIdentityInfos.id == id)\
                .first()
            prestador_servico_mapped = UsuariosInputMapper.map_prestadorServico((result_user,result_identity))
            return prestador_servico_mapped

    def insert(self, assist) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.add(assist)
            connection.session.commit()
            return assist

    def update(self, prestador_servico: PrestadoresServicos) -> PrestadoresServicos:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(
                PrestadoresServicos.id == str(prestador_servico.id)).update(
                {"nome": prestador_servico.nome,
                 "data_nascimento": prestador_servico.data_nascimento,
                 "empresa": prestador_servico.empresa,
                 "especialidade": prestador_servico.especialidade})
            connection.session.commit()

    def delete(self, id: UUID) -> None:
        with Connection() as connection:
            connection.session.query(PrestadoresServicos).filter(PrestadoresServicos.id == str(id)).delete()

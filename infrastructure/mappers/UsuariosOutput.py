from typing import Tuple
from domain.models.administrador import Administrador
from domain.models.assistente import Assistente
from domain.models.locatario import Locatario
from domain.models.prestador_servico import PrestadorServico
from infrastructure.models.administradores import Administradores
from infrastructure.models.assistentes import Assistentes
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.prestadores_servico import PrestadoresServicos
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos


class UsuariosOutputMapper:
    @staticmethod
    def map_administrador(administrador: Administrador) -> Tuple[Administradores, UsuariosIdentityInfos]:
        return (
            Administradores(
                id=administrador.id,
                data_nascimento=administrador.data_nascimento,
                nome=administrador.nome,
                e_root=administrador.e_root
            ),
            UsuariosIdentityInfos(
                id=administrador.id,
                email=administrador.email,
                senha=administrador.senha
            )
        )

    @staticmethod
    def map_assistente(assistente: Assistente) -> Tuple[Assistentes, UsuariosIdentityInfos]:
        return (
            Assistentes(
                id=assistente.id,
                nome=assistente.nome,
                data_nascimento=assistente.data_nascimento,
            ),
            UsuariosIdentityInfos(
                id=assistente.id,
                email=assistente.email,
                senha=assistente.senha
            )
        )

    @staticmethod
    def map_locatario(locatario: Locatario) -> Tuple[Locatarios, UsuariosIdentityInfos]:
        return (
            Locatarios(
                id=locatario.id,
                nome=locatario.nome,
                data_nascimento=locatario.data_nascimento,
                celular = locatario.celular
            ),
            UsuariosIdentityInfos(
                id=locatario.id,
                email=locatario.email,
                senha=locatario.senha
            )
        )

    @staticmethod
    def map_prestadores_servicos(prestadorServico: PrestadorServico) -> Tuple[PrestadoresServicos, UsuariosIdentityInfos]:
        return (
            PrestadoresServicos(
                id=prestadorServico.id,
                nome=prestadorServico.nome,
                especialidade=prestadorServico.especialidade,
                empresa=prestadorServico.empresa,
                data_nascimento=prestadorServico.data_nascimento,

            ),
            UsuariosIdentityInfos(
                id=prestadorServico.id,
                email=prestadorServico.email,
                senha=prestadorServico.senha
            )
        )

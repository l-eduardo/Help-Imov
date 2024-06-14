from uuid import UUID
from infrastructure.models.usuarios_identity_infos import UsuariosIdentityInfos
from infrastructure.models.administradores import Administradores
from infrastructure.models.assistentes import Assistentes
from infrastructure.models.locatarios import Locatarios
from infrastructure.models.prestadores_servico import PrestadoresServicos
from domain.models.administrador import Administrador
from domain.models.assistente import Assistente
from domain.models.locatario import Locatario
from domain.models.prestador_servico import PrestadorServico


class UsuariosInputMapper:
    @staticmethod
    def map_admnistrador(administrador_identity_from_db: tuple):
            usuario_from_db = administrador_identity_from_db[0]
            identity_info_from_db = administrador_identity_from_db[1]
            return Administrador(id = UUID(usuario_from_db.id),
                                 nome = usuario_from_db.nome,
                                 email = identity_info_from_db.email,
                                 senha = identity_info_from_db.senha,
                                 e_root = usuario_from_db.e_root,
                                 data_nascimento = usuario_from_db.data_nascimento)
    @staticmethod
    def map_assistente(assistente_identity_from_db: tuple):
            usuario_from_db = assistente_identity_from_db[0]
            identity_info_from_db = assistente_identity_from_db[1]
            return Assistente(id = UUID(usuario_from_db.id),
                              nome = usuario_from_db.nome,
                              email = identity_info_from_db.email,
                              senha = identity_info_from_db.senha,
                              data_nascimento = usuario_from_db.data_nascimento)
    @staticmethod     
    def map_locatario(locatario_identity_from_db: tuple):
            usuario_from_db = locatario_identity_from_db[0]
            identity_info_from_db = locatario_identity_from_db[1]
            return Locatario(id = UUID(usuario_from_db.id),
                             nome = usuario_from_db.nome,
                             email = identity_info_from_db.email,
                             senha = identity_info_from_db.senha,
                             celular = usuario_from_db.celular,
                             data_nascimento = usuario_from_db.data_nascimento)
    @staticmethod
    def map_prestadorServico(prestador_servico_identity_from_db: tuple):
            usuario_from_db = prestador_servico_identity_from_db[0]
            identity_info_from_db = prestador_servico_identity_from_db[1]
            return PrestadorServico(id = UUID(usuario_from_db.id),
                                    nome = usuario_from_db.nome,
                                    email = identity_info_from_db.email,
                                    senha = identity_info_from_db.senha,
                                    especialidade = usuario_from_db.especialidade,
                                    empresa = usuario_from_db.empresa,
                                    data_nascimento = usuario_from_db.data_nascimento)


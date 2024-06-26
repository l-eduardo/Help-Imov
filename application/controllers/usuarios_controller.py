import uuid

import sqlalchemy
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from presentation.views.usuario_view import UsuarioView
from domain.models.administrador import Administrador
from domain.models.assistente import Assistente
from domain.models.locatario import Locatario
from domain.models.usuario import Usuario
from domain.models.prestador_servico import PrestadorServico
from infrastructure.repositories.administradores_repository import AdministradoresRepository
from infrastructure.repositories.assistentes_repository import AssistentesRepository
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.locatarios_repository import LocatariosRepository
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository
from infrastructure.repositories.user_identity_repository import UserIdentityRepository
from infrastructure.mappers.UsuariosOutput import UsuariosOutputMapper


class UsuariosController:
    def __init__(self):
        self.__tela_usuarios = UsuarioView()
        self.__administradores = []
        self.__assistentes = []
        self.__locatarios = []
        self.__prestadores_servicos = []
        self.__todos_usuarios = []
        self.__administradores_repository = AdministradoresRepository()
        self.__assistentes_repository = AssistentesRepository()
        self.__locatarios_repository = LocatariosRepository()
        self.__prestadores_servicos_repository = PrestadoresServicosRepository()
        self.__user_identity_repository = UserIdentityRepository()
        self.__usuarios_mapper = UsuariosOutputMapper()

    @SessionController.inject_session_data
    def lista_usuarios(self, session: Session = None):
        self.obter_usuarios_do_banco()
        if session.user_role == 'Administrador':
            lista_usuarios = self.__todos_usuarios
            event_lista,values_lista = self.__tela_usuarios.lista_usuarios(lista_usuarios, e_admin = True)
        elif session.user_role == 'Assistente':
            lista_usuarios = self.__locatarios+self.__prestadores_servicos
            event_lista,values_lista = self.__tela_usuarios.lista_usuarios(lista_usuarios, e_admin = False)
        else:
            self.__tela_usuarios.mostra_popup("Você não possui permissão para essa ação")
        match event_lista:
            case '-MOSTRA_USUARIO-':
                self.mostra_usuario(lista_usuarios[values_lista['-TABELA-'][0]])
            case '-ADC_USUARIO-':
                self.cria_usuario(values_lista['-ADC_USUARIO-'])
    

    def mostra_usuario(self, usuario_selecionado: Usuario):
        event_mostra,values_mostra = self.__tela_usuarios.mostra_usuario(usuario_selecionado)
        match event_mostra:
            case '-EDITAR-':
                self.edita_usuario(usuario_selecionado)
            case '-VOLTAR-':
                self.lista_usuarios()
            case '-EXCLUIR-':
                try:
                    self.exclui_usuario(usuario_selecionado)
                    self.__tela_usuarios.mostra_popup("Usuário foi excluído com sucesso!")
                except sqlalchemy.exc.IntegrityError:
                    self.__tela_usuarios.mostra_popup(
                        "Este usuário está em registros importantes para histórico do sistema e não pode ser excluído! \nCaso não deseje mais seu acesso, considere alterar a senha")
                    self.mostra_usuario(usuario_selecionado)
                except SystemError as e:
                    self.__tela_usuarios.mostra_popup(e)
                    self.mostra_usuario(usuario_selecionado)

    def cria_usuario(self, permissao):
        event,values = self.__tela_usuarios.pega_dados_usuario(permissao)
        match event:
            case '-REGISTRAR-':
                match permissao:
                    case 'Administrador':
                        administrador = Administrador(nome = values['nome'],
                                                        email = values['email'],
                                                        senha = values['senha'],
                                                        data_nascimento = values['data_nascimento'])
                        administrador_mapped = self.__usuarios_mapper.map_administrador(administrador)
                        self.__user_identity_repository.save_user(administrador_mapped[1])
                        self.__administradores_repository.insert(administrador_mapped[0])
                    case 'Assistente':
                        assistente = Assistente(nome = values['nome'],
                                                email = values['email'],
                                                senha = values['senha'],
                                                data_nascimento = values['data_nascimento'])
                        assistente_mapped = self.__usuarios_mapper.map_assistente(assistente)
                        self.__user_identity_repository.save_user(assistente_mapped[1])
                        self.__assistentes_repository.insert(assistente_mapped[0])
                    case 'Locatario':
                        locatario = Locatario(nome = values['nome'],
                                              email = values['email'],
                                              senha = values['senha'],
                                              data_nascimento = values['data_nascimento'],
                                              celular = values['celular'])
                        locatario_mapped = self.__usuarios_mapper.map_locatario(locatario)
                        self.__user_identity_repository.save_user(locatario_mapped[1])
                        self.__locatarios_repository.insert(locatario_mapped[0])
                    case 'PrestadorServico':
                        prestador_servico = PrestadorServico(nome = values['nome'],
                                                             email = values['email'],
                                                             senha = values['senha'],
                                                             data_nascimento = values['data_nascimento'],
                                                             empresa = values['empresa'],
                                                             especialidade = values['especialidade'])
                        prestador_servico_mapped = self.__usuarios_mapper.map_prestadores_servicos(prestador_servico)
                        self.__user_identity_repository.save_user(prestador_servico_mapped[1])
                        self.__prestadores_servicos_repository.insert(prestador_servico_mapped[0])
            case '-CANCELAR-':
                self.__tela_usuarios.mostra_popup("Operação cancelada, usuário não foi adicionado!")
        self.lista_usuarios()

    def edita_usuario(self, usuario: Usuario):
        permissao = usuario.__class__.__name__
        if permissao == 'Administrador' and self.__administradores_repository.is_root(usuario.id):
            self.__tela_usuarios.mostra_popup("Este usuário é um administrador root e não pode ser editado!")
            self.mostra_usuario(usuario)
        else:
            event,values = self.__tela_usuarios.pega_dados_usuario(permissao, usuario=usuario, edit_mode=True)
            match event:
                case '-REGISTRAR-':
                    usuario.nome = values['nome']
                    usuario.data_nascimento = values['data_nascimento']
                    usuario.email = values['email']
                    if values['senha'] != '******':
                        usuario.senha = values['senha']
                        self.__tela_usuarios.mostra_popup(f"A senha do usuario {usuario.nome} foi alterada com sucesso")
                    if permissao == 'Locatario':
                        usuario.celular = values['celular']
                    elif permissao == 'PrestadorServico':
                        usuario.especialidade = values['especialidade']
                        usuario.empresa = values['empresa']
                    match permissao:
                        case 'Administrador':
                            administrador_mapped = self.__usuarios_mapper.map_administrador(usuario)
                            self.__user_identity_repository.update_user(administrador_mapped[1])
                            self.__administradores_repository.update(administrador_mapped[0])
                        case 'Assistente':
                            assistente_mapped = self.__usuarios_mapper.map_assistente(usuario)
                            self.__user_identity_repository.update_user(assistente_mapped[1])
                            self.__assistentes_repository.update(assistente_mapped[0])
                        case 'Locatario':
                            locatario_mapped = self.__usuarios_mapper.map_locatario(usuario)
                            self.__user_identity_repository.update_user(locatario_mapped[1])
                            self.__locatarios_repository.update(locatario_mapped[0])
                        case 'PrestadorServico':
                            prestador_servico_mapped = self.__usuarios_mapper.map_prestadores_servicos(usuario)
                            self.__user_identity_repository.update_user(prestador_servico_mapped[1])
                            self.__prestadores_servicos_repository.update(prestador_servico_mapped[0])
                case '-CANCELAR-':
                    self.__tela_usuarios.mostra_popup("Operação cancelada, usuário não foi editado!")
        self.lista_usuarios()

    @SessionController.inject_session_data
    def exclui_usuario(self, usuario: Usuario, session: Session):
        repository_delete = {'Administrador': self.__administradores_repository.delete,
                     'Assistente': self.__assistentes_repository.delete,
                     'Locatario': self.__locatarios_repository.delete,
                     'PrestadorServico': self.__prestadores_servicos_repository.delete}
        permissao = usuario.__class__.__name__
 
        if permissao == 'Locatario' and ContratosRepositories.locatario_in_contrato_ativo(str(usuario.id)):
            raise SystemError("Este locatário está em um contrato ativo e não pode ser excluído! \nCaso não deseje mais seu acesso, considere alterar a senha.")
        elif permissao == 'Administrador' and self.__administradores_repository.is_root(usuario.id):
            raise SystemError("Este usuário é um administrador root e não pode ser excluído!")
        elif str(usuario.id) == str(session.user_id):
            raise SystemError("Não é permitido excluir o usuário corrente! Solicite a outro administrador.")
        else:
            confirmacao = self.__tela_usuarios.mostra_popup(f"Você tem certeza que deseja deletar este usuário?\nNome: {usuario.nome} | E-mail: {usuario.email}", confirmacao=True)
            if confirmacao == 'Yes':
                repository_delete[permissao](usuario.id)
                self.__user_identity_repository.delete_user(usuario.id)
            else:
                raise SystemError("Operação cancelada. O usuário não foi excluído")

    def obter_usuarios_do_banco(self) -> list:
        self.__administradores = self.__administradores_repository.get_all()
        self.__assistentes = self.__assistentes_repository.get_all()
        self.__locatarios = self.__locatarios_repository.get_all()
        self.__prestadores_servicos = self.__prestadores_servicos_repository.get_all()
        self.__todos_usuarios = self.__administradores + self.__assistentes + self.__locatarios + self.__prestadores_servicos
        return self.__todos_usuarios

    def obter_prestadores_servicos(self):
        # Buscar a lista de prestadores de serviços
        prestadores = self.__prestadores_servicos_repository.get_all()

        # Extrair apenas os nomes dos prestadores
        nomes_prestadores = [prestador.nome for prestador in prestadores]

        return nomes_prestadores

    @property
    def administradores(self) -> list[Administrador]:
        return self.__administradores_repository.get_all()

    @property
    def assistentes(self) -> list[Assistente]:
        return self.__assistentes_repository.get_all()

    @property
    def locatarios(self) -> list[Locatario]:
        return self.__locatarios_repository.get_all()

    @property
    def prestadores_servico(self) -> list[PrestadorServico]:
        return self.__prestadores_servicos_repository.get_all()

    @property
    def todos_usuarios(self) -> list[Usuario]:
        return self.obter_usuarios_do_banco()
    
    def usuario_by_id(self, id) -> Usuario:
        for usuario in self.obter_usuarios_do_banco():
            if id == str(usuario.id):
                return usuario
        # Se não encontrar
        return None

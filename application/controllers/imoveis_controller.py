import re
import PySimpleGUI as sg
from domain.models.imovel import Imovel
from infrastructure.repositories.imoveis_repository import ImoveisRepository
from infrastructure.services.Imagens_Svc import ImagensService
from presentation.views.imovel_view import TelaImovel


class ImoveisController:
    def __init__(self, main_controller):
        self.__main_controller = main_controller
        self.__imoveis_repository = ImoveisRepository()
        self.__tela_imovel = TelaImovel(self)
        self.imoveis = []
        self.contratos = []
        from application.controllers.contrato_controller import ContratoController

    def valida_endereco(self, endereco):
        if len(endereco) < 10:
            raise ValueError("Endereço muito curto. Deve ter pelo menos 10 caracteres.")
        if not re.search(r'\d', endereco):
            raise ValueError("Endereço deve conter pelo menos um número.")
        if not re.search(r'[A-Za-z]', endereco):
            raise ValueError("Endereço deve conter pelo menos uma letra.")
        return True

    def inclui_imovel(self):
        event, values = self.__tela_imovel.pega_dados_imovel()

        if event == "Registrar":
            try:
                self.valida_endereco(values['endereco'])
                imagens = ImagensService.bulk_read(values["imagens"].split(';'))
                imagens_invalidas = [imagem for imagem in imagens if not imagem.e_valida()]

                if imagens_invalidas:
                    self.__tela_imovel.mostra_msg(
                        "Imagens inválidas. Por favor, selecione imagens com resolução entre 1280x720 e 1820x1280 pixels!")
                else:
                    imovel = Imovel(codigo=values['codigo'], endereco=values['endereco'],
                                    imagens=imagens)
                    self.__imoveis_repository.insert(imovel)
                    self.__imoveis_repository.update(imovel)
                    self.listar_imoveis()
            except ValueError as e:
                sg.Popup(f"Erro de validação: {str(e)}")
            except FileNotFoundError as e:
                sg.Popup(f"Erro ao ler as imagens: {str(e)}")
            except Exception as e:
                sg.Popup(f"Algo deu errado, tente novamente. \n\nErro: {str(e)}")

    def editar_imovel(self, imovel):
        event, values = self.__tela_imovel.pega_dados_editar_imovel(imovel)
        if event == "Salvar":
            try:
                self.valida_endereco(values['endereco'])
                imovel.codigo = values["codigo"]
                imovel.endereco = values["endereco"]
                self.__imoveis_repository.update(imovel)
                sg.popup("Imóvel atualizado com sucesso", title="Sucesso")
            except ValueError as e:
                sg.Popup(f"Erro de validação: {str(e)}")
            except Exception as e:
                sg.Popup(f"Algo deu errado ao atualizar o imóvel. \n\nErro: {str(e)}")
        elif event == "Cancelar":
            sg.popup("Edição cancelada", title="Aviso")

        self.listar_imoveis()

    def excluir_imovel(self, imovel: Imovel):
        try:
            if self.contrato_associado(imovel.id):
                self.__tela_imovel.mostra_msg("Imóvel associado a um contrato. Não é possível excluir")
            else:
                self.imoveis.remove(imovel)
                self.__imoveis_repository.delete(imovel.id)
                sg.Popup("Imóvel excluído com sucesso", title="Sucesso")
        except KeyError as e:
            sg.Popup(f"Erro ao excluir o imóvel: {str(e)}")
        except Exception as e:
            sg.Popup(f"Algo deu errado ao excluir o imóvel. \n\nErro: {str(e)}")

    def contrato_associado(self, imovel_id):
        from application.controllers.contrato_controller import ContratoController

        contratos_controller = ContratoController(self)
        self.contratos = contratos_controller.obter_contratos_do_banco()
        for contrato in self.contratos:
            if contrato.imovel.id == str(imovel_id):
                return True
        return False

    def buscar_imovel_por_codigo(self, codigo):
        try:
            for item in self.imoveis:
                if item.codigo == codigo:
                    return item
        except Exception as e:
            sg.Popup(f"Erro ao buscar o imóvel: {str(e)}")
        return None

    def obter_imoveis_do_banco(self) -> list[Imovel]:
        try:
            imoveis = self.__imoveis_repository.get_all()
            return imoveis
        except Exception as e:
            sg.Popup(f"Erro ao obter imóveis do banco: {str(e)}")
            return []

    def get_id_imoveis(self):
        try:
            return [imovel.id for imovel in self.imoveis]
        except Exception as e:
            sg.Popup(f"Erro ao obter IDs dos imóveis: {str(e)}")
            return []

    def listar_imoveis(self):
        while True:
            self.imoveis = self.obter_imoveis_do_banco()
            imoveis_listados = []
            for imovel in self.imoveis:
                imoveis_listados.append({
                    "idImovel": imovel.id,
                    "codigo": imovel.codigo,
                    "endereco": imovel.endereco,
                    "imagem": imovel.imagens,
                    "entity": imovel
                })

            event, values = self.__tela_imovel.mostra_imoveis_lista(imoveis_listados)

            if event == "Visualizar":
                if values["-TABELA-"]:
                    entidade = imoveis_listados[values["-TABELA-"][0]]
                    try:
                        img_dir = ImagensService.bulk_local_temp_save(entidade["imagem"])
                        imovel_result = self.__tela_imovel.mostra_imovel(
                            entidade["entity"],
                            lista_paths_imagens=img_dir)
                        if imovel_result is not None:
                            event, imovel = imovel_result
                            if event == "editar_imovel":
                                self.editar_imovel(imovel)
                            if event == "excluir_imovel":
                                self.excluir_imovel(imovel)
                    except FileNotFoundError as e:
                        sg.Popup(f"Erro ao salvar imagens temporárias: {str(e)}")
                    except Exception as e:
                        sg.Popup(f"Erro ao visualizar imóvel: {str(e)}")
                else:
                    sg.Popup("Nenhum imóvel selecionado")

            if event == "Adicionar":
                self.inclui_imovel()

            if event in (sg.WIN_CLOSED, "Voltar"):
                from application.controllers.main_controller import MainController
                self.__main_controller.abrir_tela_inicial()
                break

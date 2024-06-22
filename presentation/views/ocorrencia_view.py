from typing import List

import PySimpleGUI as sg

from domain.enums.status import Status
from domain.models.ocorrencia import Ocorrencia
from infrastructure.repositories.prestadores_servicos_repository import PrestadoresServicosRepository
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from application.controllers.usuarios_controller import UsuariosController


class OcorrenciaView:
    def __init__(self):
        self.ocorrencia_repository = OcorrenciasRepository()
        self.prestadores_repository = PrestadoresServicosRepository()
        self.usuarios_controller = UsuariosController()

    def mostra_popup(self, mensagem: str):
        sg.popup(mensagem)

    def vw_nova_ocorrencia(self):
        window = self.__add_ocorrencia_layout()

        event, values = window.read()

        values['imagens'] = values['imagens'].split(';') if values['imagens'] else []

        window.close()
        return event, values

    def vw_editar_ocorrencia(self, ocorrencia: 'Ocorrencia'):
        window, prestadores_map = self.__edit_ocorrencia_layout(ocorrencia)

        event, values = window.read()
        window.close()

        if values['prestadores'] == 'Nenhum':
            values['prestadores'] = None
        else:
            values['prestadores'] = prestadores_map[values['prestadores']]

        return event, values

    def __edit_ocorrencia_layout(self, ocorrencia: 'Ocorrencia'):
        centrilizedButtons = [sg.Button("Confirmar", key="confirmar_edicao"), sg.Button("Cancelar")]

        prestadores = PrestadoresServicosRepository().get_all()
        prestadores_nomes = ['Nenhum'] + [prestador.nome for prestador in prestadores]
        prestadores_map = {prestador.nome: prestador.id for prestador in prestadores}

        layout = [
            [sg.Text("Titulo "),
             sg.InputText(key="titulo", tooltip="titulo", size=(50, 1), expand_x=True, default_text=ocorrencia.titulo)],
            [sg.Text("Descrição"),
             sg.Multiline(key="descricao", tooltip="descricao", size=(50, 10), no_scrollbar=True, expand_x=True,
                          default_text=ocorrencia.descricao)],
            [sg.Text("Prestador de serviço"),
             sg.Combo(prestadores_nomes, size=(20, 1),
                      default_value=ocorrencia.prestador_id and self.prestadores_repository.get_name_by_id(
                          ocorrencia.prestador_id) or 'Nenhum', key='prestadores')],
            [sg.Text("Status"),
             sg.Combo([Status.ABERTO.value, Status.FECHADO.value], default_value=ocorrencia.status.value,
                      key="status")],
            [sg.Column([centrilizedButtons], justification="center")]
        ]

        window = sg.Window(f"Help imov - Detalhes da ocorrencia ({ocorrencia.id})", layout)

        return window, prestadores_map

    def vw_mostra_ocorrencia(self, ocorrencia: 'Ocorrencia', dirs: List[str]):
        window = self.__show_details_layout(ocorrencia, dirs)

        event, values = window.read()

        window.close()
        return event, values

    def __show_details_layout(self, ocorrencia: 'Ocorrencia', dirs: List[str]):
        centrilizedButtons = [sg.Button("Editar", key="editar_ocorrencia"), sg.Button("Voltar")]
        prestador_nome = self.prestadores_repository.get_name_by_id(
            ocorrencia.prestador_id) if ocorrencia.prestador_id else 'Nenhum'


        layout = [[sg.Text("Detalhes da ocorrencia")],
                  [sg.Text("Titulo: "), sg.Text(ocorrencia.titulo, key="titulo")],
                  [sg.Text("Descrição: "), sg.Text(ocorrencia.descricao, key="descricao")],
                  [sg.Text("Status: "), sg.Text(ocorrencia.status.name, key="status")],
                  [sg.Text("Data de criação: "), sg.Text(ocorrencia.data_criacao, key="data_criacao")],
                  [sg.Text("Prestador de serviço"), sg.Text(prestador_nome, key="prestadores")],
                  [sg.Text("Imagens: ")],
                  [sg.Image(filename=dir, size=(200, 133), subsample=5, zoom=1) for dir in dirs],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window(f"Help imov - Detalhes da ocorrencia ({ocorrencia.id})", layout)

        return window

    def __add_ocorrencia_layout(self):
        centrilizedButtons = [sg.Button("Salvar", size=(10, 1)), sg.Button("Cancelar", size=(10, 1))]

        layout = [[sg.Text("Titulo ")],
                  [sg.InputText(key="titulo", tooltip="titulo", size=(50, 1), expand_x=True)],
                  [sg.HorizontalSeparator()],
                  [sg.Text("Descrição")],
                  [sg.Multiline(key="descricao", tooltip="descricao", size=(50, 10), no_scrollbar=True, expand_x=True)],
                  [[sg.Input(key='imagens'), sg.FilesBrowse(initial_folder="./", file_types=(("Imagens", "*.png"),),
                                                            tooltip="Selecione imagens da ocorrencia...")]],
                  [sg.Column([centrilizedButtons], justification="center")]]

        window = sg.Window("Help imov - Nova ocorrencia", layout)

        return window

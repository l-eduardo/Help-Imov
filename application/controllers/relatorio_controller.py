from datetime import date, datetime
from typing import List
from application.controllers.session_controller import SessionController
from domain.models.session import Session
from infrastructure.repositories.contratos_repository import ContratosRepositories
from infrastructure.repositories.ocorrencias_repository import OcorrenciasRepository
from infrastructure.repositories.solicitacoes_repository import SolicitacoesRepository
from infrastructure.services.canva_chart_Svc import CanvaChartService
from domain.enums.status import Status
from collections import Counter
from presentation.views.relatorio_view import RelatorioView


class RelatorioController:
    def __init__(self):
        self.__relatorio_view = RelatorioView()

        self.__ocorrencia_repository = OcorrenciasRepository()
        self.__solicitacao_repository = SolicitacoesRepository()
        self.__contrato_repository = ContratosRepositories()
        pass

    def menu_relatorios(self):

        while True:
            click_event = self.__relatorio_view.open_relatorio_menu()

            match click_event:
                case "contratos":
                    event, datas = self.__relatorio_view.pega_datas()
                    if event == None:
                        continue

                    data_inicial = datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
                    if datas["data_inicial"] != "":
                        data_inicial = datetime.strptime(datas["data_inicial"], "%Y-%m-%d %H:%M:%S")

                    data_final = datetime.strptime("9999-9-9 23:59:59", "%Y-%m-%d %H:%M:%S")
                    if datas["data_final"] != "":
                        data_final = datetime.strptime(datas["data_final"], "%Y-%m-%d %H:%M:%S")

                    contratos = self.__contrato_repository.get_all_with_start_and_date(data_inicial, data_final)

                    datas = [contrato.dataCadastro for contrato in contratos]
                    ordered_dates, quantidades = self.__date_to_ordered_counted_str(datas)

                    chart = CanvaChartService.create_line_chart(quantidades, ordered_dates, "Contratos X Tempo")

                    self.__relatorio_view.mostrar_grafico(chart)

                case "ocorrencias":
                    contratos = self.__contrato_repository.get_all()

                    contratos_id = [str(contrato.id)[:8] + "..." for contrato in contratos[-10:]]
                    solicitacoes_count_per_id = [len(contrato.ocorrencias) for contrato in contratos[-10:]]
                    solicitacoes_concluidas_count_per_id = [
                        len([ocorrencia for ocorrencia in contrato.ocorrencias if ocorrencia.status == Status.FECHADO])
                        for contrato in contratos[-10:]
                    ]

                    chart = CanvaChartService.create_stacked_bar_chart(top_values=solicitacoes_count_per_id,
                                                                    bottom_values=solicitacoes_concluidas_count_per_id,
                                                                    keys=contratos_id,
                                                                    bottom_values_legenda="Concluidas",
                                                                    top_values_legenda="Fechadas",
                                                                    title="Ocorrencias X Contratos")

                    self.__relatorio_view.mostrar_grafico(chart)
                    break

                case "solicitacoes":
                    contratos = self.__contrato_repository.get_all()

                    contratos_id = [str(contrato.id)[:8] + "..." for contrato in contratos[-10:]]
                    solicitacoes_count_per_id = [len(contrato.solicitacoes) for contrato in contratos[-10:]]
                    solicitacoes_concluidas_count_per_id = [
                        len([solicitacao for solicitacao in contrato.solicitacoes if solicitacao.status == Status.FECHADO])
                        for contrato in contratos[-10:]
                    ]

                    chart = CanvaChartService.create_stacked_bar_chart(top_values=solicitacoes_count_per_id,
                                                                    bottom_values=solicitacoes_concluidas_count_per_id,
                                                                    keys=contratos_id,
                                                                    bottom_values_legenda="Concluidas",
                                                                    top_values_legenda="Fechadas",
                                                                    title="Solicitacoes X Contratos")

                    self.__relatorio_view.mostrar_grafico(chart)

                case _:
                    break



    def __date_to_ordered_counted_str(self, dates: List[date]) -> list:
        dates.sort()
        dates = [date.strftime("%d/%m/%Y") for date in dates]
        datas_counter = Counter(dates)

        quantidades = [datas_counter[data] for data in datas_counter]

        quantidade_acumulada = []
        total_acumulado = 0

        for data in datas_counter:
            total_acumulado += datas_counter[data]
            quantidade_acumulada.append(total_acumulado)

        return datas_counter.keys(), quantidades

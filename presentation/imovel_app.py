from kivy.app import App

from domain.models.imovel import Imovel
from presentation.tela_inicial import TelaInicial


class ImovelApp(App):
    def build(self):
        self.imoveis = [  # valores de teste
            Imovel(codigo=1, endereco="Rua 1", imagens=[]),
            Imovel(codigo=2, endereco="Rua 2", imagens=[]),
        ]

        self.contratos = {}

        tela_inicial = TelaInicial(imoveis=self.imoveis)
        return tela_inicial


if __name__ == '__main__':
    ImovelApp().run()

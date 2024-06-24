from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CanvaChartService:
    @staticmethod
    def create_line_chart(x_axis_values: list, y_axis_values: list, title: str = "Grafico") -> None:
        plt.plot(y_axis_values, x_axis_values, marker='o', color='b', scalex=1)

        plt.title(title)

        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        return plt.gcf()

    @staticmethod
    def create_bar_chart(x_axis_values, y_axis_values, title: str = "Grafico") -> None:
        plt.bar(y_axis_values, x_axis_values, color='b')

        plt.title(title)

        plt.grid(True)
        plt.xticks(rotation=45, fontsize=10)

        plt.tight_layout()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        return plt.gcf()

    @staticmethod
    def create_stacked_bar_chart(keys, top_values, bottom_values, title: str = "Grafico") -> None:
        plt.bar(keys, top_values, color='blue')
        plt.bar(keys, bottom_values, color='green')
        plt.legend(['Ocorrencias abertas', 'Ocorrencias concluidas'])

        plt.title(title)

        plt.grid(True)
        plt.xticks(rotation=45, fontsize=10)

        plt.tight_layout()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        return plt.gcf()

from domain.models.imovel import Imovel


class ImovelUseCase:
    def __init__(self, imovel_repository):
        self.imovel_repository = imovel_repository

    def create_imovel(self, imovel: Imovel):
        self.imovel_repository.save(imovel)

        # Return the created imovel
        return imovel

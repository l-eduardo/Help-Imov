from uuid import UUID
from infrastructure.models.mensagens import Mensagens
from domain.models.chat import Chat


class ChatInputMapper:
    @staticmethod
    def map_chat(id_from_db: str, mensagens_from_db: list[Mensagens], participantes: list[UUID]):
            lista_mensagens = []
            #servico ordenar mensagens
            lista_mensagens = [(mensagem.id,
                                mensagem.usuario,
                                mensagem.mensagem, 
                                mensagem.datetime) for mensagem in mensagens_from_db]
            return Chat(id = UUID(id_from_db.id),
                        mensagens=lista_mensagens,
                        participantes=participantes)
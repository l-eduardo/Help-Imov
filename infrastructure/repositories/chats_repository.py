from typing import List
from uuid import UUID
from domain.models.chat import Chat
from domain.models.mensagem import Mensagem
from domain.models.ocorrencia import Ocorrencia
from infrastructure.configs.connection import Connection
from infrastructure.mappers.ChatInput import ChatInputMapper
from infrastructure.mappers.ChatOutput import ChatOutputMapper
from infrastructure.mappers.ImagemOutput import ImagemOutputMapper
from infrastructure.models.chats import Chats
from infrastructure.models.imagens import Imagens
from domain.models.imagem import Imagem
from infrastructure.models.mensagens import Mensagens
from infrastructure.models.usuarios_ocorrencias import UsuariosOcorrencias



class ChatsRepository():
    def get_by_ocorrencia_id(self, id_ocorrencia: UUID):
        with Connection() as connection:
            result_chat_id = connection.session.query(Chats).filter(Chats.ocorrencia_id == str(id_ocorrencia)).first()
            result_mensagens = connection.session.query(Mensagens).filter(Mensagens.chat_id == str(id)).all()
            result_participantes = connection.session.query(UsuariosOcorrencias).filter(UsuariosOcorrencias.ocorrencia_id == str(id)).all()
            chat_mapped = ChatInputMapper.map_chat(result_chat_id, result_mensagens, result_participantes)
            return result_chat_id

    def insert_chat(self, chat: Chat):
        chat_to_db = ChatOutputMapper.map_chat(chat)
        with Connection() as connection:
            connection.session.add(chat_to_db)
            connection.session.commit()
            return chat

    def insert_novas_mensagens(self, chat_id: UUID, novas_mensagens: List[Mensagem]):
        novas_mensagens_mapeadas = ChatOutputMapper.map_mensagens(chat_id, novas_mensagens)
        with Connection() as connection:
            [connection.session.add(mensagem) for mensagem in novas_mensagens_mapeadas]
            connection.session.commit()
            return novas_mensagens

    def insert_novas_imagens(self, chat_id: UUID, novas_imagens: List[Imagem]):
        with Connection() as connection:
            for imagem in novas_imagens:
                imagem_mapped = ImagemOutputMapper.map(imagem,
                                                       chat_id=chat_id)
                connection.session.add(imagem_mapped)
            connection.session.commit()
            return 0

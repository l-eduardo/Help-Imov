from uuid import UUID


class Session:
    def __init__(self, user_id: UUID,
                 user_email: str,
                 user_role: str,
                 is_root: bool,
                 is_admin: bool,
                 is_valid: bool,
                 session_id: UUID):
        self.__user_id: UUID = user_id
        self.__user_email: str = user_email
        self.__user_role: str = user_role
        self.__is_admin: bool = is_admin
        self.__is_root: bool = is_root
        self.__is_valid: bool = is_valid
        self.__session_id: UUID = session_id

    @property
    def session_id(self):
        return self.__session_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_role(self):
        return self.__user_role

    @property
    def is_root(self):
        return self.__is_root

    @property
    def is_admin(self):
        return self.__is_admin

    @property
    def is_valid(self):
        return self.__is_valid

    @property
    def user_email(self):
        return self.__user_email

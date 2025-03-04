import utils.ada as ada
from services.registration_service import RegistrationService
from error import UserManagerException


class RegistrationPageController():
    """
    RegistrationPageController - класс контроллера представления страницы регистрации нового пользователя
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def is_there_users(self):
        """
        Проверяет, есть ли в системе созданные пользователи
        Используется для того что бы определить при входе в систему не нужно ли создавать суперпользователя

        Returns:
            Boolean: True/False в зависимости от того есть в системе пользователи или нет
        """

        registration_service = RegistrationService()
        return registration_service.is_there_users()

    def create_user(self, _login, _name, _password, _password2, _email, _create_superuser):
        """
        Создает в системе суперпользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _create_superuser (Boolean): признак создания суперпользователя
        
        Returns:
            string: токен созданного пользователя

        """

        # создаем суперпользователя
        registration_service = RegistrationService()
        user_data = {
            'login': _login,
            'name': _name,
            'password': _password,
            'password2': _password2,
            'email': _email,
            'create_superuser': _create_superuser,
            'probationers_number': 5
        }
        user = registration_service.create_user(user_data)

        return user.token

    def send_confirmation_email(self, _email, _html):
        """
        Отправляет пользователю письмо с подтверждением регистрации

        Args:
            _email (String): email пользователя
            _html (String): текст письма
        """

        registration_service = RegistrationService()
        registration_service.send_confirmation_email(_email, "подтверждение регистрации", _html)
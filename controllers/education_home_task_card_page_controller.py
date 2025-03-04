from flask import Markup

from services.homework_card_service import HomeworkCardService
from error import HomeworkManagerException, HomeworkCardServiceException


class EducationHomeworkCardPageController():
    """
    EducationChatPageController - класс контроллера представления чата с пользователями, реализующий логику взаимодействия приложения с пользователем.
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    # def homework_chat_entry(self, _id_homework_chat, _id_user):
    #     """
    #     Подключает пользователя к чату
    #
    #     Args:
    #         _id_homework_chat(Integer): ID чата
    #         _id_user(Integer) ID пользователя
    #
    #     Returns:
    #         Dict: чат
    #     """
    #
    #     homework_service = HomeworkCardService()
    #
    #     homework_chat = homework_service.homework_chat_entry(_id_homework_chat, _id_user)
    #     if homework_chat is not None:
    #         homework_chat_view = {
    #             "id": homework_chat.id,
    #             "message": []
    #         }
    #         if homework_chat.message is not None:
    #             for i_message in homework_chat.message:
    #                 user = homework_service.get_user_by_id(i_message.id_user)
    #                 message = {
    #                     "id": i_message.id,
    #                     "text": Markup(i_message.text),
    #                     "id_user": i_message.id_user,
    #                     "name": user.name
    #                 }
    #
    #                 homework_chat_view['message'].append(message)
    #
    #         return homework_chat_view

    def add_message(self, _message, _id_lesson, _id_user):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            Dict: сообщение
        """

        homework_service = HomeworkCardService()

        # если в сообщениях есть такое сочетание, то оно удаляется для того, чтобы сократить расстояние между строчками
        if "<p><br></p>" in _message['text']:
            _message['text'] = ''.join(_message['text'].split('<p><br></p>'))

        homework_service.add_message(_message, _id_lesson, _id_user)

    def get_user_by_id(self, _user_id):
        """
        Возвращает данные текущего пользователя

        Returns:
            user(Dict): данные пользователя
        """

        homework_service = HomeworkCardService()

        user = homework_service.get_user_by_id(_user_id)
        user_view = {
            "user_id": user.user_id,
            "login": user.login,
            "role": user.role,
            "active_education_module": user.active_education_module,
            "education_module_expiration_date": user.education_module_expiration_date.strftime("%d/%m/%Y"),
            "education_stream": {}
        }

        return user_view

    def homework_answer_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Принято"

        Args:
            _id_homework(Int): ID домашней работы
            _user_id(Int): ID текущего пользователя

        Return:
            homework_view(Dict): домашняя работа
            message(String): сообщение к статус коду
            status_code(String): сообщает об успешном изменении оценки
        """

        homework_service = HomeworkCardService()

        homework_service.homework_answer_accepted(_id_homework, _user_id)
        message = "Домашняя работа принята"

        return message, "Successful"

    def homework_answer_no_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Не принято"

        Args:
            _id_homework(Int): ID домашней работы
            _user_id(Int): ID текущего пользователя

        Return:
            homework_view(Dict): домашняя работа
            message(String): сообщение к статус коду
            status_code(String): сообщает об успешном изменении оценки
        """

        homework_service = HomeworkCardService()

        homework_service.homework_answer_no_accepted(_id_homework, _user_id)
        message = "Домашняя работа не принята"

        return message, "Successful"

    def get_homework(self, _id_homework):
        """
        Возвращает данные домашней работы

        Args:
            _id_homework(Int): ID домашней работы

        Return:
            Dict: данные домашней работы
        """
        homework_service = HomeworkCardService()

        if _id_homework is None:
            return None

        homework = homework_service.get_homework(_id_homework)
        if homework is not None:
            if homework.status is None:
                homework.status = "не проверено"
            elif homework.status:
                homework.status = "Принято"
            elif not homework.status:
                homework.status = "Не принято"

            homework_view = {
                "id": homework.id,
                "id_lesson": homework.id_lesson,
                "id_user": homework.id_user,
                "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                "users_files_list": homework.users_files_list,
                "status": homework.status,
                "text": Markup(homework.text)
            }

            return homework_view

    def get_data_by_id_homework(self, _id_homework):
        """
        Возвращает данные, связанные с домашней работы

        Args:
            _id_homework(Int): ID домашней работы

        Return:
            Dict: данные, связанные с домашней работы
        """
        homework_service = HomeworkCardService()

        if _id_homework is None:
            return None, None
        else:
            homework = homework_service.get_homework(int(_id_homework))

        data = {}
        try:
            module = homework_service.get_lesson(homework.id_lesson)
            course = homework_service.get_course(module.id_course)

            data["module"] = {
                "id": module.id,
                "name": module.name,
                "lesson": {
                    "id": module.lessons.id,
                    "name": module.lessons.name,
                    "task": Markup(module.lessons.task)
                }
            }

            data["course"] = {
                "id": course.id,
                "name": course.name
            }
        except HomeworkCardServiceException as error:
            data['module'] = error

        user = homework_service.get_user_by_id(homework.id_user)
        if user is not None:
            data["user"] = {
                "id": user.user_id,
                "login": user.login,
                "name": user.name,
                "email": user.email,
            }
        else:
            data['user'] = 'Данный пользователь не найден'

        if homework.status is None:
            homework.status = "не проверено"
        elif homework.status:
            homework.status = "Принято"
        elif not homework.status:
            homework.status = "Не принято"

        homework_view = {
            "id": homework.id,
            "id_lesson": homework.id_lesson,
            "id_user": homework.id_user,
            "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
            "users_files_list": homework.users_files_list,
            "status": homework.status,
            "text": Markup(homework.text)
        }

        return data, homework_view

    def get_data_by_id_homework_chat(self, _id_homework_chat, _id_user):
        """
        Возвращает данные, связанные с домашней работы

        Args:
            _id_homework_chat(Integer): ID комнаты чата
            _id_user(Integer): ID пользователя

        Return:
            Dict: данные, связанные с домашней работы
        """
        homework_service = HomeworkCardService()

        if _id_homework_chat is None:
            return None, None

        else:
            homework_chat = homework_service.homework_chat_entry(int(_id_homework_chat), _id_user)

        data = {}
        try:
            module = homework_service.get_lesson(homework_chat.id_lesson)

            data["module"] = {
                "id": module.id,
                "name": module.name,
                "lesson": {
                    "id": module.lessons.id,
                    "name": module.lessons.name,
                    "task": Markup(module.lessons.task)
                }
            }
            course = homework_service.get_course(module.id_course)

            data["course"] = {
                "id": course.id,
                "name": course.name
            }
        except HomeworkCardServiceException as error:
            data['module'] = error

        except TypeError:
            data['course'] = "Данный курс не найден"

        user = homework_service.get_user_by_id(homework_chat.id_user)
        if user is not None:
            data["user"] = {
                "id": user.user_id,
                "login": user.login,
                "name": user.name,
                "email": user.email,
            }
        else:
            data['user'] = 'Данный пользователь не найден'

        homework_chat_view = {
            "id": homework_chat.id,
            "message": []
        }
        if homework_chat.message is not None:
            for i_message in homework_chat.message:
                user = homework_service.get_user_by_id(i_message.id_user)
                message = {
                    "id": i_message.id,
                    "text": Markup(i_message.text),
                    "id_user": i_message.id_user,
                    "name": user.name
                }

                homework_chat_view['message'].append(message)

        return data, homework_chat_view

    def get_homework_chat_by_id_homework(self, _id_homework, _id_current_user):
        """
        Возвращает данные комнаты чата по ID домашней работы

        Args:
            _id_homework(Int): ID домашней работы
            _id_current_user(Int): ID текущего пользователя

        Returns:
            Dict: чат
        """
        homework_service = HomeworkCardService()

        homework = homework_service.get_homework(_id_homework)
        if homework is not None:
            homework_chat = homework_service.get_homework_chat(homework.id_lesson, homework.id_user, _id_current_user)
            if homework_chat is not None:
                room_chat_view = {
                    "id": homework_chat.id,
                    "message": []
                }
                if homework_chat.message is not None:
                    message_list = []
                    for i_message in homework_chat.message:
                        user = homework_service.get_user_by_id(i_message.id_user)
                        message = {
                            "id": i_message.id,
                            "text": Markup(i_message.text),
                            "id_user": i_message.id_user,
                            "name": user.name
                        }

                        message_list.append(message)

                    room_chat_view["message"] = message_list

                return room_chat_view

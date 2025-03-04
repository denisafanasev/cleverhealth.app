from models.action_manager import ActionManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager
from models.module_manager import EducationModuleManager
from models.timetable_manager import TimetableManager


class EducationStreamCardService():
    """
    Класс сервиса карточки обучающего потока
    """

    def get_education_streams(self):
        """
        Возвращает список обучающих потоков

        Returns:
            education_streams_list(List): список обучающих потоков
        """

        education_stream_manager = EducationStreamManager()
        course_manager = EducationCourseManager()

        education_streams = education_stream_manager.get_education_streams()
        education_streams_list = []

        for i_education_stream in education_streams:

            course = course_manager.get_course_by_id(i_education_stream.course)
            i_education_stream.course = course
            education_streams_list.append(i_education_stream)

        return education_streams_list

    def get_students_list(self, _user_id, _id_education_stream):
        """
        Возвращает список студентов обучающего потока

        Args:
            _user_id(Int): ID текущего пользователя
            _id_education_stream(Int): ID обучающего потока

        Returns:
            students_list(List): список пользователей
        """

        user_manager = UserManager()
        education_stream_manager = EducationStreamManager()

        if _id_education_stream is not None:
            education_stream = education_stream_manager.get_education_stream(_id_education_stream)
            students_list = user_manager.get_users_by_ids_list(_user_id, education_stream.students_list)
            if len(students_list) == 0:
                users_list = user_manager.get_users_by_role(_user_id, 'user')
                for user in users_list:
                    if user.user_id in education_stream.students_list:
                        students_list.append(user)
        else:
            students_list = user_manager.get_users_by_role(_user_id, 'user')

        return students_list

    def get_curators_list(self, _user_id, _id_education_stream):
        """
        Возвращает список кураторов обучающего потока

        Args:
            _user_id(Int): ID текущего пользователя
            _id_education_stream(Int): ID обучающего потока

        Returns:
            curators_list(List): список пользователей
        """

        user_manager = UserManager()
        education_stream_manager = EducationStreamManager()

        if _id_education_stream is not None:
            education_stream = education_stream_manager.get_education_stream(_id_education_stream)
            curators_list = user_manager.get_users_by_ids_list(_user_id, education_stream.curators_list)
            if len(curators_list) == 0:
                users_list = user_manager.get_users_by_role(_user_id, 'superuser')
                curators_list = []
                for user in users_list:
                    if user.user_id in education_stream.curators_list:
                        curators_list.append(user)
        else:
            curators_list = user_manager.get_users_by_role(_user_id, 'superuser')

        return curators_list

    def get_courses_list(self):
        """
        Возвращает список курсов

        Returns:
            (List): список курсов
        """

        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()

        courses_list = course_manager.get_courses()
        main_courses_list = [course for course in courses_list if course.type == 'main']
        courses = []
        for course in main_courses_list:
            course.modules = module_manager.get_course_modules_list(course.id)
            courses.append(course)

        return courses

    def get_education_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        education_stream_manager = EducationStreamManager()
        course_manager = EducationCourseManager()
        user_manager = UserManager()

        education_stream = education_stream_manager.get_education_stream(_id)
        if education_stream is not None:
            education_stream.teacher = user_manager.get_user_by_id(education_stream.teacher)
            education_stream.course = course_manager.get_course_by_id(education_stream.course)

        return education_stream

    def create_education_stream(self, _education_stream, _timetables_list, _current_user_id):
        """
        Создает обучающий поток и создает событие "Создан обучающий поток"

        Args:
            _education_stream(Dict): обучающий поток
            _timetables_list(List): расписание открытия модулей для обучающего потока
            _current_user_id(Int): ID текущего пользователя

        Returns:
            id(Int): идентификатор обучающего потока
        """
        education_stream_manager = EducationStreamManager()
        timetable_manager = TimetableManager()
        action_manager = ActionManager()
        user_manager = UserManager()
        course_manager = EducationCourseManager()

        education_stream = education_stream_manager.create_education_stream(_education_stream)
        timetable_manager.create_timetable(_timetables_list, education_stream.id)

        current_user = user_manager.get_user_by_id(_current_user_id)
        course = course_manager.get_course_by_id(_education_stream['id_course'])
        action_manager.add_notifications(course.name, 'создал', education_stream.name, 'education_stream_manager',
                                         current_user)

        return education_stream.id

    def save_education_stream(self, _education_stream, _timetables_list, _current_user_id):
        """
        Изменяет данные обучающего потока и создает событие "Изменен обучающий поток"

        Args:
            _education_stream(Dict): обучающий поток
            _timetables_list(List): список расписаний открытия модулей для потока
            _current_user_id(Int): ID текущего пользователя

        Returns:
            None
        """

        education_stream_manager = EducationStreamManager()
        timetable_manager = TimetableManager()
        user_manager = UserManager()
        action_manager = ActionManager()
        course_manager = EducationCourseManager()

        education_stream = education_stream_manager.save_education_stream(_education_stream)
        timetable_manager.save_timetable(_timetables_list, education_stream.id)

        current_user = user_manager.get_user_by_id(_current_user_id)
        course = course_manager.get_course_by_id(_education_stream['id_course'])
        action_manager.add_notifications(course.name, 'отредактировал', education_stream.name,
                                         'education_stream_manager', current_user)

    def get_education_streams_by_login_user(self, _login_user, _role_user):
        """_summary_

        Args:
            _login_user (_type_): _description_
            _role_user (_type_): _description_

        Returns:
            _type_: _description_
        """        

        education_stream_manager = EducationStreamManager()

        return education_stream_manager.get_education_streams_list_by_id_user(_login_user, _role_user)

    def get_timetables_list(self, _id):
        """
        Возвращает список расписаний обучающего потока по ID потока

        Args:
            _id(Int): ID обучающего потока

        Returns:
            List(Timetable): список расписаний
        """
        timetable_manager = TimetableManager()

        return timetable_manager.get_timetables_list_by_id_education_stream(_id)

    def get_timetable_by_id_module_and_id_education_stream(self, _id_module, _id_education_stream):
        """
        Возвращает расписание по id модуля и id обучающего потока

        Args:
            _id_module(Int): ID модуля
            _id_education_stream(Int): ID обучающего потока

        Returns:
            TimeTable: расписание
        """
        timetable_manager = TimetableManager()

        return timetable_manager.get_timetable_by_id_module_and_id_education_stream(_id_module, _id_education_stream)

    def get_module_by_id(self, _id):
        """
        Возвращает модуль курса по id модуля

        Args:
            _id(Int): ID модуля

        Returns:
            Module: модуль курса
        """
        module_manager = EducationModuleManager()

        return module_manager.get_module_by_id(_id)

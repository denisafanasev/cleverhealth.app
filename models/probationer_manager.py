from data_adapters.data_store import DataStore
from models.probationer import Probationer
from datetime import datetime
from error import ProbationerManagerException


class ProbationerManager():

    def get_probationers(self, _user):
        """
        Возвращает список испытуемых

        Args:
            _user(User): пользователь

        Returns:
            probationers(List): список тестируемых
        """
        probationers = []

        data_store = DataStore("probationers")

        patients_list_data = data_store.get_rows()

        for patients_data in patients_list_data:

            patient = self.probationer_row_to_probationer(patients_data.doc_id, patients_data["name_probationer"],
                                                        patients_data["name_parent"],
                                                        patients_data["educational_institution"],
                                                        patients_data["contacts"],
                                                       patients_data["diagnoses"], patients_data["reasons_for_contact"],
                                                          patients_data["user_login"], patients_data["date_of_birth"])

            patient.date_of_birth = datetime.strptime(patients_data["date_of_birth"], "%d/%m/%Y").strftime("%d/%m/%Y")

            if _user.role == "superuser":
                probationers.append(patient)
            elif patient.user_login == _user.login:
                probationers.append(patient)

        return probationers

    def get_probationer_by_id(self, _probationer_id):
        """
        Возвращает объект Probationer по id испытуемого

        Args:
            _probationers_id   - Required  : id пользователя (Int)
        """

        data_store = DataStore("probationers")

        patient = None

        patients_data = data_store.get_row_by_id(_probationer_id)

        if patients_data is not None:
            patient = self.probationer_row_to_probationer(patients_data.doc_id, patients_data["name_probationer"],
                                                        patients_data["name_parent"], patients_data["educational_institution"],
                                                        patients_data["contacts"],
                                                        patients_data["diagnoses"], patients_data["reasons_for_contact"],
                                                          patients_data["user_login"], patients_data["date_of_birth"])

            patient.date_of_birth = datetime.strptime(patients_data["date_of_birth"], "%d/%m/%Y").strftime("%Y-%m-%d")

        return patient

    def probationer_row_to_probationer(self, _probationer_id, _name_probationer, _name_parent,
                                       _educational_institution, _contacts,
                                       _diagnoses, _reasons_for_contact, _user_login="", _date_of_birth=""):
        """
        Преобразует структуру данных, в которой хранится информация о испытуемом в структуру Probationer

       Args:
            _user_login(String): логин пользователя, к которому прикреплен испытуемый.
            _name_probationer(String): имя испытуемого
            _date_of_birth(date, optional): дата рождения испытуемого
            _name_parent(String): ФИО родителя испытуемого
            _educational_institution(String): учебное заведение испытуемого
            _contacts(String): контакты для связи
            _diagnoses(String): сопутствующие диагнозы
            _reasons_for_contact(String): причины обращения

        Returns:
            Probationer: испытуемый
        """

        # создадим пользователя с указанием обязательных атрибутов
        probationer = Probationer(_probationer_id, _name_probationer=_name_probationer, _date_of_birth=_date_of_birth,
                                  _name_parent=_name_parent, _educational_institution=_educational_institution,
                                  _contacts=_contacts, _diagnoses=_diagnoses, _reasons_for_contact=_reasons_for_contact,
                                  _user_login=_user_login)

        # проверим наличие в структуре хранения необязательных атрибутов

        return probationer

    def create_probationer(self, _user_login, _name_probationer, _date_of_birth, _name_parent,
                           _educational_institution, _contacts, _diagnoses, _reasons_for_contact):
        """
        Процедура создания нового испытуемого в системе

        Args:
            _user_login(String): логин пользователя, к которому прикреплен испытуемый.
            _name_probationer(String): имя испытуемого
            _date_of_birth(date, optional): дата рождения испытуемого
            _name_parent(String): ФИО родителя испытуемого
            _educational_institution(String): учебное заведение испытуемого
            _contacts(String): контакты для связи
            _diagnoses(String): сопутствующие диагнозы
            _reasons_for_contact(String): причины обращения
        """

        user_login = _user_login
        name_probationer = _name_probationer
        date_of_birth = _date_of_birth
        name_parent = _name_parent
        educational_institution = _educational_institution
        contacts = _contacts
        diagnoses = _diagnoses
        reasons_for_contact = _reasons_for_contact

        # создаем новую запись
        data_store = DataStore("probationers")

        # создаем новую запись
        probationer = Probationer(_user_login=user_login, _name_probationer=name_probationer,
                                  _name_parent=name_parent, _educational_institution=educational_institution,
                                  _contacts=contacts, _diagnoses=diagnoses, _reasons_for_contact=reasons_for_contact)

        probationer.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").strftime("%d/%m/%Y")

        probationer_data = {"user_login":probationer.user_login, "name_probationer": probationer.name_probationer,
                            "date_of_birth": probationer.date_of_birth, "name_parent": probationer.name_parent,
                            "educational_institution": probationer.educational_institution,
                            "contacts": probationer.contacts, "diagnoses": probationer.diagnoses,
                            "reasons_for_contact": probationer.reasons_for_contact}

        data_store.insert_row(probationer_data)

        return probationer.name_probationer

    def change_probationer(self, _probationer_id, _name_probationer, _date_of_birth, _name_parent, _educational_institution,
                           _contacts, _diagnoses, _reasons_for_contact):
        """
        Записывает изменения данных тестируемого

        Args:
            _probationer_id(Int): id тестируемого
            _name_probationer(String): имя тестируемого
            _date_of_birth(date, optional): дата рождения тестируемого
            _name_parent(String): ФИО родителя тестируемого
            _educational_institution(String): учебное заведение тестируемого
            _contacts(String): контакты для связи
            _diagnoses(String): сопутствующие диагнозы
            _reasons_for_contact(String): причины обращения
        """

        probationer = self.probationer_row_to_probationer(_probationer_id=_probationer_id, _name_probationer=_name_probationer,
                                                          _name_parent=_name_parent, _educational_institution=_educational_institution,
                                                          _contacts=_contacts,
                                                          _diagnoses=_diagnoses, _reasons_for_contact=_reasons_for_contact)

        probationer.date_of_birth = datetime.strptime(_date_of_birth, "%Y-%m-%d").strftime("%d/%m/%Y")

        probationer_data = {"name_probationer": probationer.name_probationer,
                            "date_of_birth": probationer.date_of_birth, "name_parent": probationer.name_parent,
                            "educational_institution": probationer.educational_institution,
                            "contacts": probationer.contacts, "diagnoses": probationer.diagnoses,
                            "reasons_for_contact": probationer.reasons_for_contact}

        data = DataStore("probationers")

        data.update_row_by_id(probationer_data, probationer.probationer_id)

        return probationer.name_probationer

    def is_probationers(self, _user_login):

        data_store = DataStore("probationers")

        if data_store.get_rows({"user_login": _user_login}) != []:
            return True
        else:
            return False


"""
app configuration
"""

import pathlib

VERSION = "0.0.9.1"
APP_NAME = "NeuroHealth"
DATA_FOLDER = "../neurohealth.care.data.devs/"

if str(pathlib.Path().resolve()).find("prod")!=-1:
    ENVIRONMENT = "prod"
else:
    ENVIRONMENT = "dev"

# system settings
THREADING_ENABLE = True
DEBUG = False
LOG_FILE = "neuro_health.log"

SECRET_KEY = 'my_secret_key'
SECURITY_PASSWORD_SALT = 'my_security_password_salt'

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# mail accounts
MAIL_DEFAULT_SENDER = 'from@example.com'

# gmail authentication
MAIL_USERNAME = ""
MAIL_PASSWORD = ""


SUPERUSER_MENU = [
    {"module": "Центр управления", "name": "Пользователи", "endpoint": "user_manager", "icon": "users"},
    {"module": "Центр управления", "name": "Настройки", "endpoint": "age_range_list", "icon": "settings"},
        {"module": "Центр управления", "name": "Домашние задания",
        "endpoint": "education_home_tasks", "icon": "edit"},
]

EDUCATION_MENU = [
    {"module": "Центр обучения", "name": "Каталог курсов",
        "endpoint": "education_list_courses", "icon": "video"}
]

TESTING_MENU = [

    {"module": "Центр тестирования", "name": "Тестируемые", "endpoint": "probationers", "icon": "users"},
    {"module": "Центр тестирования", "name": "Протоколы", "endpoint": "probes", "icon": "list"},
    {"module": "Центр тестирования", "name": "Результаты", "endpoint": "results", "icon": "activity"}    
]

CORRECTIONS_MENU = [

    {"module": "Центр коррекции", "name": "Коррекция", "endpoint": "corrections", "icon": "trending-up"}
    
]

MAIN_MENU = [
    {"module": "", "name": "Рабочий стол", "endpoint": "main_page", "icon": "sliders"}  
]

SETTINGS_MENU = [
    {"name": "Справочник оценочных значений", "endpoint": "estimated_values"},
    {"name": "Справочник диапазонов возрастов", "endpoint": "age_range_list"}
]

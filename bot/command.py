import re

from tools import *
import os,dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

dotenv.load_dotenv()

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findEmailCommand(update: Update, context):
    update.message.reply_text("Введите текст для поиска электронных почт: ")
    return 'findEmail'

def findEmail(update: Update, context):
    emails = find_email_in_text(update.message.text) # Список email в формате (номер, почта) 
    context.user_data['emails'] = emails

    if not emails: #Если наш список пустой, то выход
        update.message.reply_text('Элетронные почты не найдены')
        return ConversationHandler.END 
    
    Exists_In_BD = True
    message = ""
    for num_email,email in emails: 
        if check_to_exists_table("emails","email",email):
            message += f"✅{num_email}. {email}\n"
        else:
            message += f"❌{num_email}. {email}\n"
            Exists_In_BD = False 
        
    if not Exists_In_BD:
        message += "\nХотите добавить новые почты в базу данных?\n[Да/Нет]"
        update.message.reply_text(message)
        return 'insert_find_emails'
    else:
        message += "\nВсе почты есть в базе данных!"
        update.message.reply_text(message)
        return ConversationHandler.END 

def insert_find_emails(update:Update, context):
    message = ""
    if update.message.text == "Да":
        emails = context.user_data['emails']
        for number_email, email in emails:
            if not check_to_exists_table("emails","email",email):
                if insert_to_table_info("emails","email",email):
                    message = "Почты(-а) успешно добавлены(-а) в базу данных!"
                else:
                    message = "Произошла ошибка при добавлении в базу данных"
    update.message.reply_text(message)
    return ConversationHandler.END 


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'


def findPhoneNumbers(update: Update, context):
    phoneNumbers = find_phone_in_text(update.message.text)
    context.user_data['phones'] = phoneNumbers

    if not phoneNumbers:
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END
    
    Exists_In_BD = True
    message = ""
    for num_phone,phone in phoneNumbers: 
        if check_to_exists_table("phones","phone",phone):
            message += f"✅{num_phone}. {phone}\n"
        else:
            message += f"❌{num_phone}. {phone}\n"
            Exists_In_BD = False 
        
    if not Exists_In_BD:
        message += "\nХотите добавить новые телефоны в базу данных?\n[Да/Нет]"
        update.message.reply_text(message)
        return 'insert_find_phones'
    else:
        message += "\nВсе телефоны есть в базе данных!"
        update.message.reply_text(message)
        return ConversationHandler.END 
    
def insert_find_phones(update:Update, context):
    message = ""
    if update.message.text == "Да":
        phones = context.user_data['phones']
        for number_phone, phone in phones:
            if not check_to_exists_table("phones","phone",phone):
                if insert_to_table_info("phones","phone",phone):
                    message = "Телефон(-ы) успешно добавлен(-ы) в бвазу данных!"
                else:
                    message = "Произошла ошибка при добавлении в базу данных"
    update.message.reply_text(message)
    return ConversationHandler.END 

def verifyPassswordCommand(update: Update, context):
    update.message.reply_text('Введите ваш пароль: ')

    return 'verifyPasssword'

def verifyPasssword(update: Update, context):
    user_input = update.message.text

    verifyPassswordRegex = re.compile(r'(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$%^&*()]).{8,}')
    
    if verifyPassswordRegex.search(user_input):
        update.message.reply_text("Пароль сложный!")
    else:
        update.message.reply_text("Пароль простой!")

    return ConversationHandler.END

def echo(update: Update, context):
    update.message.reply_text(update.message.text)

def get_release_command(update: Update, context):
    result = exec_command_ssh("cat /etc/os-release")
    update.message.reply_text(result)

def get_uname_command(update: Update, context):
    cpu_arch = exec_command_ssh("uname -m")
    hostname = exec_command_ssh("uname -n")
    kernel_version = exec_command_ssh("uname -r")

    update.message.reply_text(f"Архитектура процессора системы: {cpu_arch}\nИмя хоста системы: {hostname}\nВерсия ядра системы: {kernel_version}")

def get_uptime_command(update: Update, context):
    uptime = exec_command_ssh("uptime -p")
    update.message.reply_text(f'System is {uptime}')

def get_df_command(update: Update, context):
    result = exec_command_ssh("df -h")
    update.message.reply_text(result)

    
def get_free_command(update: Update, context):
    result = exec_command_ssh("free -h")
    update.message.reply_text(result)

def get_mpstat_command(update: Update, context):
    result = exec_command_ssh("mpstat")
    update.message.reply_text(result)

def get_w_command(update: Update, context):
    result = exec_command_ssh("w")
    update.message.reply_text(result)

def get_auths_command(update: Update, context):
    result = exec_command_ssh("last -n 10")
    update.message.reply_text(f"Последние 10 входов в систему: \n\n{result}")

def get_critical_command(update: Update, context):
    result = exec_command_ssh("journalctl -r -p crit -n 5")
    update.message.reply_text(f"Последние 5 критических событий в системе: \n\n{result}")

def get_ps_command(update: Update, context):
    result = exec_command_ssh("ps -A | head -n 30")
    update.message.reply_text(f"Первые 30 процессов в системе: \n\n{result}")

def get_ss_command(update: Update, context):
    result = exec_command_ssh("ss -tulpn -H")
    update.message.reply_text(f"Открытые порты на системе: \n\n{result}")

def get_apt_list_command(update: Update, context):
    command = update.message.text
    if len(command.split()) == 1:
        result = exec_command_ssh("apt list | head -n 30")
        update.message.reply_text(f"Первые 30 установленных пакетов в системе: \n\n{result}")
    else:
        arg = update.message.text.split()[1]
        if re.match(r'^[0-9A-z\-]+$',arg):
            result = exec_command_ssh(f"apt list {arg}")
            update.message.reply_text(f"Информация о пакете: \n\n{result}")
        else:
            update.message.reply_text("Название пакета, может состоять только из букв, цифр и тире")
        

def get_services_command(update: Update, context):
    result = exec_command_ssh("systemctl list-unit-files --state=enabled")
    update.message.reply_text(f"Сервисы запущенные на системе: \n\n{result}")


def get_repl_logs_command(update: Update, context):
    command = f"echo {os.getenv('RM_PASSWORD')} | sudo -S docker logs db | grep repl | head -n 30" 
    result = exec_command_ssh(command)
    update.message.reply_text(result)

def get_emails_commands(update: Update, context):
    data = get_row_from_table("emails")
    update.message.reply_text(f"Список почт: \n\n{data}")

def get_phones_commands(update: Update, context):
    data = get_row_from_table("phones")
    update.message.reply_text(f"Список телефонов: \n\n{data}")
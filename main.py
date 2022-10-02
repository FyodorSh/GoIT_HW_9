# Завдання
# Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, і відповідати відповідно
# до введеної команди.
#
# Бот помічник повинен стати для нас прототипом додатка-асистента. Додаток-асистент в першому наближенні повинен уміти
# працювати з книгою контактів і календарем. У цій домашній роботі зосередимося на інтерфейсі самого бота. Найбільш
# простий і зручний на початковому етапі розробки інтерфейс - це консольний додаток CLI (Command Line Interface).
# CLI досить просто реалізувати. Будь-який CLI складається з трьох основних елементів:
#
# Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та
# модифікаторів команд.
# Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання
# команд.
# Цикл запит-відповідь. Ця частина програми відповідає за отримання від користувача даних та повернення користувачеві
# відповіді від функції-handlerа.
# На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям,
# змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку,
# скористаємося словником. У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.
#
# Умови
# Бот повинен перебувати в безкінечному циклі, чекаючи команди користувача.
# Бот завершує свою роботу, якщо зустрічає слова: .
# Бот не чутливий до регістру введених команд.
# Бот приймає команди:
# "hello", відповідає у консоль "How can I help you?"
# "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. Замість ... користувач
# вводить ім'я та номер телефону, обов'язково через пробіл.
# "change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. Замість ... користувач
# вводить ім'я та номер телефону, обов'язково через пробіл.
# "phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. Замість ... користувач
# вводить ім'я контакту, чий номер треба показати.
# "show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
# "good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе у консоль
# "Good bye!".
# Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає за
# повернення користувачеві повідомлень виду "Enter user name", "Give me name and phone please" і т.п. Декоратор
# input_error повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати
# відповідну відповідь користувачеві.
# Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають
# рядок.
# Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там.


RECORDS = {}


# Decorators


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            print("Wrong command")
        except IndexError:
            print("Wrong command")
    return wrapper


# Procedures


def hello():
    print("How can I help you?")


@input_error
def add(*args):
    command_list = args[0]
    if not len(command_list) == 2:
        print("Give me name and phone please")
        return
    contact_name = command_list[0]
    contact_phone = command_list[1]
    RECORDS[contact_name] = contact_phone


@input_error
def change(*args):
    command_list = args[0]
    if not len(command_list) == 2:
        print("Give me name and phone please")
        return
    contact_name = command_list[0]
    contact_phone = command_list[1]
    RECORDS[contact_name] = contact_phone


@input_error
def phone(*args):
    command_list = args[0]
    if not len(command_list) == 1:
        print("Enter user name")
        return

    contact_name = args[0][0]
    print(RECORDS[contact_name])


@input_error
def show():
    for key, data in RECORDS.items():
        print(f"Name: {key} - Phone: {data}")


def stop():
    print("Good bye!")
    quit()


@input_error
def get_handler(command_list):
    return read_command_list(command_list)


def read_command_list(command_list: list):
    command = OPERATIONS[command_list.pop(0).lower()]
    command = read_command_list(command_list) if command == read_command_list else command
    return command


OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show': read_command_list,
    'all': show,
    'good': read_command_list,
    'bye': stop,
    'close': stop,
    'exit': stop
}


def bot():
    while True:
        command = input("Enter command: ")
        command_list = command.split(sep=" ")
        handler = get_handler(command_list)
        if handler is not None:
            if not command_list:
                handler()
            else:
                handler(command_list)


if __name__ == '__main__':
    bot()

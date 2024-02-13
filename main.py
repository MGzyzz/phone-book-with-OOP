import re
import os


class Application:

    def main_menu(self):
        log = FileLoader("./data.txt")
        safe_log = log.loading_file()
        phone_book = PhoneBook(safe_log)

        print("Добро пожаловать в телефонную книгу, Пожалуйста сделайте выбор по индексам ниже")
        while True:
            match phone_book.choose_user():
                case "1":
                    print(phone_book.contact_number())
                case "2":
                    find = input("Пожалуйста напишите имя контакта\n").capitalize()
                    phone_book.find_user(find)
                case "3":
                    phone_book.add_user()
                case "4":
                    phone_book.add_phone()
                case "5":
                    phone_book.edit_user()
                case "6":
                    phone_book.delete_user()
                case "7":
                    phone_book.delete_number()
                case "0":
                    if phone_book.continue_user():
                        break
                case _:
                    print("Введеная вами команда не существует. Пожалуйста попробуете снова")

            phone_book.contact_number()

            log.unloading_file(safe_log)


class PhoneBook:
    def __init__(self, new_contact):
        self.contact = new_contact


    def edit_user(self):
        choose_contact = input("Напишите контакт который вы хотите изменить\n").capitalize()
        contacted_user = self.get_contact(self.contact, choose_contact)

        if contacted_user:
            self.find_user(choose_contact)
            choose_reset = input("Что вы хотите изменить? Выбор = имя/номер\n").lower()

            if choose_reset == "имя" or choose_reset == "name":
                choose_name = input("Введите новое имя пользователя\n").capitalize()
                if contacted_user and self.check_numbers(choose_name) and not self.get_contact(self.contact,
                                                                                               choose_name):
                    contacted_user['name'] = choose_name
                    return print("Имя изменено!")
                else:
                    return print("Пользователь с таким именнем существует")

            elif choose_reset == "номер" or choose_reset == "phone":
                choose = input("\nКакой номер вы хотите изменить? Выбор осуществляется с помощью индексов\n")
                if int(choose) <= len(contacted_user['phone']):
                    choose_phone = input("Введите новый номер телефона\n")
                    if self.check_words(choose_phone):
                        index_number = int(choose) - 1
                        contacted_user['phone'][index_number] = choose_phone
                        return print("Номер изменен!")

                else:
                    print("Введенный вами номер не существует")

            else:
                print("Неверная команда попробуйте снова")
        else:
            self.notFound()


    def notFound(self):
        return print("Введеный вами контакт не существует. Попробуйте снова")


    def check_words(self, check):
        if re.match(r'^[\d+-]+$', check):
            return check
        else:
            return print(
                "Действие невозможно так как введенный вами номер содержит букву или другой символ. Пожалуйста напишите номер повторно")


    def check_numbers(self, check):
        if re.match(r'^[a-zA-Z]+$', check):
            return check
        else:
            return print(
                "Действие невозможно так как введенный вами имя содержит цифры или другой символ. Пожалуйста напишите имя повторно")


    def get_contact(self, contact_list: list, name) -> dict:
        for contact in contact_list:
            if contact.get('name') == name:
                return contact

    def find_user(self, find):
        user_find = self.get_contact(self.contact, find)
        if user_find:
            if user_find['name'] == find:
                return print(
                    f"\nКонтакт найден:\nИмя: {user_find['name']}\nНомера: {' '.join(f'[{x + 1}] {n}' for x, n in enumerate(user_find['phone']))}\n")
        else:
            return print("Введеный вами контакт не существует. Попробуйте снова")


    def contact_number(self):
        result = f'\n{"Name":<5}|{"Phone":>5}\n{"-" * 35}\n'
        self.contact.sort(key=lambda x: x["name"])

        for name in self.contact:
            phone_numbers = " ".join(name['phone'])
            result += f"{name['name']:<5}|{phone_numbers:>5}\n"
        return result


    def add_user(self):
        add_name = input("Пожалуйста введите имя\n").capitalize()
        new_user = self.get_contact(self.contact, add_name)

        if not new_user:
            if self.check_numbers(add_name):
                add_phone = input("Введите номер телефона\n")
                if self.check_words(add_phone):
                    new_contact = {"name": add_name, "phone": [add_phone]}
                    self.contact.append(new_contact)
                    return print("Пользователь был успешно добавлен!")
        else:
            print("Пользователь с таким именнем существует")


    def add_phone(self):
        user = input("Пожалуйста введите имя контакта\n").capitalize()
        new_user = self.get_contact(self.contact, user)
        self.find_user(user)

        if new_user:
            add_number = input("\nВведите номер для добавление\n")
            if self.check_words(add_number):
                new_user['phone'].append(add_number)
                return print("Номер успешно добавлен!")


    def continue_user(self):
        choose = input("Вы точно хотите совершить это действие? y/n\n").lower()

        if choose == "y" or choose == "ok" or choose == "yes":
            return True
        else:
            print("Действие отменено!")
            return False


    def show_number(self, find):
        number = self.get_contact(self.contact, find)
        return number["phone"]


    def delete_user(self):
        delete_name = input("Какого пользователя вы хотите удалить?\n").capitalize()
        user_delete = self.get_contact(self.contact, delete_name)
        if user_delete:
            self.find_user(delete_name)
            if user_delete['name'] and self.continue_user():
                self.contact.remove(user_delete)
                return print("Действие завершено")
            else:
                return
        else:
            self.notFound()


    def delete_number(self):
        user = input("Введите контакт для удаление номер\n").capitalize()
        contacted_user = self.get_contact(self.contact, user)
        if contacted_user:
            self.find_user(user)
            choose_number = input("Какой номер вы хотите удалить? Выбор осуществляется с помощью индексов\n")
            if len(self.show_number(user)) == 1:
                return print("Действие невозможно, так как у пользователя один номер")
            elif int(choose_number) <= len(contacted_user['phone']) and self.continue_user():
                choose_number = int(choose_number) - 1
                contacted_user['phone'].pop(choose_number)
                return print("Номер удален!")
        else:
            self.notFound()


    def choose_user(self):
        choose = input(
            "\n[1] Вывести контакты\n[2] Найти контакт\n[3] Добавить контакт\n[4] Добавить номер для контакта\n[5] Изменить "
            "контакт\n[6] Удалить контакт\n[7] Удалить номер контакта\n[0] Выход\n")
        return choose


class FileLoader:
    def __init__(self, name):
        self.name_file = name
        if os.path.exists(self.name_file):
            self.loading_file()
        else:
            self.name_file = "./new_file.txt"
            with open(self.name_file, "w+") as f:
                choose_person = input(
                    "Файл не найден. Для удобства был создан новый файл. Хотите ли вы добавить новый контакт? y/n\n")
                if choose_person == 'y':
                    choose_one = input("Напишите контакт\n").capitalize()
                    choose_two = input("Напишите номер\n")
                    f.write(f"{choose_one}, {choose_two}")


    def loading_file(self):
        new_contact = Contact('', '')
        with open(self.name_file, 'r') as f:
            for line in f.readlines():
                data = line.replace('\n', '').split(', ')
                name = data[0]
                phone_numbers = [x.strip() for x in data[1:]]
                new_contact.name = name
                new_contact.phone_numbers = phone_numbers
                new_contact.add_book()
        return new_contact.massive


    def unloading_file(self, data, ):
        with open(self.name_file, 'w') as f:
            for entry in data:
                name = entry['name']
                phones = ', '.join(entry['phone'])
                f.write(f'{name}, {phones}\n')


class Contact:
    def __init__(self, name, phone_numbers):
        self.name = name
        self.phone_numbers = phone_numbers
        self.massive = []

    def add_book(self):
        product = {
            'name': self.name,
            'phone': self.phone_numbers,
        }
        self.massive.append(product)

    def display(self):
        for i in self.massive:
            print(f"Name:{i['name']}, Phone:{i['phone']}")


Application().main_menu()





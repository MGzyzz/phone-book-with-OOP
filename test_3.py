import os

class FileLoader:
    def __init__(self):
        self.name_file = "data.txt"

    def check_file(self):
        if os.path.exists(self.name_file):
            self.loading_file()
        else:
            new_file = "./new_file.txt"
            with open(new_file, "w+") as f:
                choose_person = input(
                    "Файл не найден. Для удобства был создан новый файл. Хотите ли вы добавить новый контакт? y/n\n")
                if choose_person == 'y':
                    choose_one = input("Напишите контакт\n").capitalize()
                    choose_two = input("Напишите номер\n")
                    f.write(f"{choose_one}, {choose_two}")
            self.name_file = new_file

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

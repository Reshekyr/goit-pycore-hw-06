from __future__ import annotations

from collections import UserDict
from typing import List, Optional


class Field:
    """Базовий клас для полів запису. Зберігає тільки value і текстове подання."""

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:  # pragma: no cover
        return str(self.value)


class Name(Field):
    """Обов'язкове поле імені контакту."""
    pass


class Phone(Field):
    """Поле номера телефону з валідацією (рівно 10 цифр)."""

    def __init__(self, value: str):
        digits = ''.join(ch for ch in str(value) if ch.isdigit())
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(digits)


class Record:
    """Зберігає ім'я (Name) та список телефонів (List[Phone])."""

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    # Додавання телефону
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    # Видалення телефону (за значенням). Повертає True якщо видалено.
    def remove_phone(self, phone: str) -> bool:
        target = self.find_phone(phone)
        if target is None:
            return False
        self.phones.remove(target)
        return True

    # Редагування телефону: old -> new. Повертає True якщо змінено.
    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        target = self.find_phone(old_phone)
        if target is None:
            return False
        # перевірка валідності нового номера
        new_phone_obj = Phone(new_phone)
        # заміна значення (можемо замінити об'єкт або змінити value)
        target.value = new_phone_obj.value
        return True

    # Пошук телефону: повертає Phone або None
    def find_phone(self, phone: str) -> Optional[Phone]:
        digits = ''.join(ch for ch in str(phone) if ch.isdigit())
        for p in self.phones:
            if p.value == digits:
                return p
        return None

    def __str__(self) -> str:  # pragma: no cover
        phones = '; '.join(p.value for p in self.phones) if self.phones else ''
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """Книга контактів на базі словника: ключ — ім'я (str), значення — Record."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True
        return False

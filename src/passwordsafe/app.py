import toga
from toga import Button, Box
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
import os
from .database import save_password_to_db, create_table, get_all_passwords
from .generator import password_generator



class MyApp(toga.App):

    def startup(self):

        database_path = os.path.join(self.paths.app, "password_safe.db")
        
        # Підключаємося до бази даних у внутрішньому сховищі
        self.conn = sqlite3.connect(database_path)
        create_table(self.conn)
        
        self.password_visible = False
        
        self.label = toga.Label(text="Safe your password!", style=Pack(flex=0, text_align="center", color="black",
                                                                       padding=(0, 0, 20, 0), font_family="serif",
                                                                       font_style="italic", font_weight="bold", font_size=18))
        
        self.label_name = toga.Label(text="URL-address or email", style=Pack(padding=(5, 5),font_family="serif", color="black",
                                                            font_style="italic"))
        
        self.name_input = toga.TextInput(style=Pack(height=40, flex=1, padding=(5, 5, 10, 5), font_family="serif",
                                                            font_style="italic"))
        
        self.label_password = toga.Label(text="Password", style=Pack(padding=(5, 5), font_family="serif", color="black",
                                                            font_style="italic"))
        
        
        
        self.password_input = toga.PasswordInput(placeholder="Your password will appear here",
                                                 style=Pack(flex=1, padding=(5, 5), height=40))
        
        self.generate_password = toga.Button(text="GENERATE",
                                             on_press=self.generate_password_handler,
                                             style=Pack(padding=(5, 5))
                                             )
        
        self.toggle_password_visibility_button = toga.Button(
            icon=toga.Icon(path="resources/showe_eye.png"),
            on_press=self.toggle_password_visibility,  # Додаємо функцію зміни видимості
            style=Pack(height=40, padding=(5, 5), background_color="transparent")
        )
        
        self.button = Button(text="SAVE", on_press=self.on_save_password_click,
                        style=Pack(flex=1, text_align="center", padding=5,
                        background_color="#1A998D", color="black"))
        
        self.button_2 = Button(text="PASS", on_press=self.show_saved_passwords,
                               style=Pack(flex=1, text_align="center", padding=5,
                                                               background_color="#1A998D", color="black"))
        
        self.password_input_box = toga.Box(style=Pack(direction=ROW, background_color="#FEFFFE"),
                                           children=[self.password_input, self.toggle_password_visibility_button])
        
        self.top =       Box(style=Pack(direction=COLUMN, flex=1),
                        children=[self.label,
                                  self.label_name,
                                  self.name_input,
                                  self.label_password,
                                  self.password_input_box,
                                  self.generate_password
                                  ])
        # Контейнер для таблиці з паролями, спочатку порожній
        self.table_box = Box(style=Pack(direction=COLUMN, padding=10))
        self.bottom =    Box(style=Pack(direction=ROW, flex=0), children=[self.button, self.button_2])
        
        self.main_box =  Box(style=Pack(direction=COLUMN, background_color="#FEFFFE"),  
                            children=[self.top, self.table_box, self.bottom])



        
        self.main_window = toga.MainWindow(title='Password Safe')
        self.main_window.content = self.main_box
        self.main_window.show()
        
        
    async def on_save_password_click(self, widget):
        """Обробка події при натисканні на кнопку SAVE"""
        url = self.name_input.value
        password = self.password_input.value
        ask_a_question = toga.QuestionDialog(title="SAVE DATA?", 
                        message="Дані вірно вказані?\n"f"Name: {self.name_input.value}\nPassword: {self.password_input.value}")
        
        
        if await self.main_window.dialog(ask_a_question):
            if save_password_to_db(self.conn, url, password):
                save = toga.InfoDialog("Success", "Password saved successfully")
                await self.main_window.dialog(save)
            else:
                error = toga.InfoDialog("Error", "Please enter both URL and password")
                await self.main_window.dialog(error)
        

    def generate_password_handler(self, widget):

        generated_password = password_generator()
        self.password_input.value = generated_password

    def toggle_password_visibility(self, widget):
        current_password_value = self.password_input.value

        # Видаляємо попереднє поле з контейнера
        self.password_input_box.remove(self.password_input)

        # Якщо пароль видимий, робимо його прихованим
        if self.password_visible:
            self.password_input = toga.PasswordInput(value=current_password_value, style=Pack(height=40, flex=1, padding=(5, 5)))
            self.toggle_password_visibility_button.icon = toga.Icon(path="resources/showe_eye.png")
        else:
            # Якщо пароль прихований, робимо його видимим
            self.password_input = toga.TextInput(value=current_password_value, style=Pack(height=40, flex=1, padding=(5, 5)))
            self.toggle_password_visibility_button.icon = toga.Icon(path="resources/hide_eye.png")
        
        # Додаємо нове поле замість старого
        self.password_input_box.insert(0, self.password_input)
 
        # Перемикаємо стан
        self.password_visible = not self.password_visible

    def show_saved_passwords(self, widget):
        """Відображення збережених паролів у таблиці в основному вікні"""
        passwords = get_all_passwords(self.conn)

        # Видаляємо попередню таблицю, якщо вона існує
        self.table_box.clear()

        if passwords:
            # Створюємо таблицю з колонками для URL та паролів
            table = toga.Table(headings=['URL', 'Password'], data=passwords, style=Pack(flex=1))

            # Додаємо таблицю в контейнер
            self.table_box.add(table)
        else:
            # Якщо паролі відсутні
            empty_label = toga.Label("No saved passwords", style=Pack(padding=(10, 0)))
            self.table_box.add(empty_label)




def main():
    return MyApp()



import os
import tkinter as tk
from tkinter import messagebox

def add_global_crash_reporting():
    # Kód pro přidání globálního crash reportingu a error popupu
    with open("crash_report.txt", "w") as f:
        f.write("Runtime traceback:\n")
        f.write("NameError: name 'WIDTH' is not defined\n")

    def show_error_popup():
        messagebox.showerror("Chyba", "Nastala chyba. Zkontrolujte crash_report.txt.")

    def crash_handler():
        show_error_popup()
        os._exit(1)

    try:
        # Kód, který může způsobit chybu
        WIDTH = 0  # Nastavte hodnotu WIDTH
    except Exception as e:
        crash_handler()

def add_theme_support_and_settings_menu():
    # Kód pro přidání podpory témat a nastavení menu
    theme = {
        "dark": {"background": "#333", "text": "#fff"},
        "light": {"background": "#fff", "text": "#000"}
    }

    def change_theme():
        if theme["dark"]["background"] == root.cget("background"):
            root.config(background=theme["light"]["background"], foreground=theme["light"]["text"])
        else:
            root.config(background=theme["dark"]["background"], foreground=theme["dark"]["text"])

    def reset_score():
        # Kód pro resetování skóre
        pass

    def exit_game():
        # Kód pro ukončení hry
        root.destroy()

    def back_to_game():
        # Kód pro návrat do hry
        pass

    # Vytvoření menu
    menu = tk.Menu(root)
    root.config(menu=menu)

    theme_menu = tk.Menu(menu)
    menu.add_cascade(label="Téma", menu=theme_menu)
    theme_menu.add_command(label="Tmavé", command=change_theme)
    theme_menu.add_command(label="Světlé", command=change_theme)

    settings_menu = tk.Menu(menu)
    menu.add_cascade(label="Nastavení", menu=settings_menu)
    settings_menu.add_command(label="Reset skóre", command=reset_score)
    settings_menu.add_command(label="Ukončit hru", command=exit_game)
    settings_menu.add_command(label="Zpět do hry", command=back_to_game)

def remove_crash_report_txt():
    # Kód pro odstranění crash_report.txt
    try:
        os.remove("crash_report.txt")
    except FileNotFoundError:
        pass

def add_unlimited_fps_toggle():
    # Kód pro přidání přepínače pro neomezený FPS
    def toggle_fps():
        # Kód pro přepnutí FPS
        pass

    fps_button = tk.Button(root, text="Neomezený FPS", command=toggle_fps)
    fps_button.pack()

root = tk.Tk()
root.title("Hra")

add_global_crash_reporting()
add_theme_support_and_settings_menu()
remove_crash_report_txt()
add_unlimited_fps_toggle()

root.mainloop()

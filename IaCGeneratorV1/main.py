import os
import tkinter as tk        # Needed for PhotoImage for window icon
import customtkinter as ctk # For all CTk widgets
from tabs.home import create_home_tab
from tabs.cheat import create_cheat_tab
from tabs.information import create_information_tab

def main():
    # Appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Main window frame
    root = ctk.CTk()
    root.title("IaC Generator v1.0")
    root.geometry("800x650")
    root.minsize(800, 650)

    # Program icon
    icon_path = os.path.join("images", "icon.png")
    icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(True, icon)

    # Signature label
    signature_label = ctk.CTkLabel(root,
        text="IaC Generator v0.1  |  Szymon Kawecki (C00286043 - SETU Carlow)",
        font=("Arial", 9),
        text_color="gray"
    )
    signature_label.pack(side="bottom", anchor="e", padx=10, pady=5)

    # Tabs container
    notebook_frame = ctk.CTkFrame(root)
    notebook_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

    tabview = ctk.CTkTabview(notebook_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    tabview.add("Home")
    tabview.add("Input Cheat Sheet")
    tabview.add("Information")

    # Create page tabs
    create_home_tab(tabview.tab("Home"))
    create_cheat_tab(tabview.tab("Input Cheat Sheet"))
    create_information_tab(tabview.tab("Information"))

    root.mainloop()


if __name__ == "__main__":
    main()

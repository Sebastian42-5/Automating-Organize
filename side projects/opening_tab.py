from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from functools import partial
import sys
import time
import webbrowser
import os
import json


shortcuts_file = 'shortcuts.json'

def load_shortcuts():
    if not os.path.exists(shortcuts_file):
        with open(shortcuts_file, 'w') as f:
            json.dump([], f)
    with open(shortcuts_file, 'r') as f:
        return json.load(f)
    


def save_shortcuts(shortcuts):
    with open(shortcuts_file, 'w') as f:
        json.dump(shortcuts, f, indent = 4)


class MyWindow(QMainWindow):

    def __init__(self):

        super(MyWindow, self).__init__()

        self.setGeometry(200, 200, 300, 300)

        self.setWindowTitle('Tab opener!')

        self.setWindowIcon(QIcon(os.path.abspath('shark-icon-size_24.ico')))

        self.shortcuts = load_shortcuts()

        print(f'Loaded shortcuts: {self.shortcuts}')

        self.initUI()


    def initUI(self):

        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)

        self.layout_display = QVBoxLayout(self.central_widget)

        self.label = QLabel('Welcome! Click one of the shortcuts below: ')
        self.label.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')

        self.layout_display.addWidget(self.label)



        self.scroll_area = QtWidgets.QScrollArea()

        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()

        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)

        self.layout_display.addWidget(self.scroll_area)



        self.add_shortcut_buttons()

        self.create_btn = QPushButton('Create new shortcut')

        self.create_btn.setStyleSheet('margin: 10px; padding: 6px 12px;')

        self.create_btn.clicked.connect(self.open_create_dialog)

        self.layout_display.addWidget(self.create_btn, alignment = Qt.AlignRight)

    
    def delete_shortcut_by_name(self, name, widget):
        reply = QtWidgets.QMessageBox.question(self, 'Delete Shortcut', f'Are you sure you want to delete {name} ?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.shortcuts = [s for s in self.shortcuts if s['name'] != name]

            save_shortcuts(self.shortcuts)

            self.refresh_buttons()

        

    def add_shortcut_buttons(self):

        for i, shortcut in enumerate(self.shortcuts):
            name = shortcut['name']
            urls = shortcut['urls']

            row_widget = QWidget()

            row_layout = QtWidgets.QHBoxLayout()

            row_widget.setLayout(row_layout)



            open_btn = QPushButton(name)

            open_btn.setStyleSheet('padding: 8px; font-size: 14px;')


            open_btn.clicked.connect(partial(self.open_url_program, urls))
        

            delete_btn = QPushButton('X')

            delete_btn.setStyleSheet('padding: 6px;')

            delete_btn.setMinimumSize(30, 30)

            delete_btn.clicked.connect(partial(self.delete_shortcut_by_name, name, row_widget))


            row_layout.addWidget(open_btn)
            row_layout.addWidget(delete_btn)

            row_layout.setContentsMargins(0, 0, 0, 0)


            self.scroll_layout.addWidget(row_widget)


    def open_url_program(self, urls):

        for path in urls:

            if isinstance(path, str):
                if os.path.exists(path):
        
                    os.startfile(path)
                    time.sleep(2)
            
                else:
                    webbrowser.open_new_tab(path)
                    time.sleep(0.5)


    def open_create_dialog(self):

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Create new shortcut')
        dialog.setFixedSize(300, 300)

        layout = QtWidgets.QVBoxLayout(dialog)

        name_label = QLabel('Shortcut name: ')

        name_input = QtWidgets.QLineEdit()

        urls_label = QLabel('Enter URLs (one per line): ')

        urls_input = QtWidgets.QPlainTextEdit()

        done_btn = QPushButton('Done')

        done_btn.clicked.connect(partial(self.handle_done_clicked, dialog, name_input, urls_input))


        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(urls_label)
        layout.addWidget(urls_input)
        layout.addWidget(done_btn)


        dialog.setLayout(layout)

        dialog.exec_()


    
    def handle_done_clicked(self, dialog, name_input, urls_input):
        name = name_input.text()
        urls_text = urls_input.toPlainText()
        self.save_new_shortcut(dialog, name, urls_text)

    
    def refresh_buttons(self):

        while self.scroll_layout.count():

            item = self.scroll_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
        
        self.add_shortcut_buttons()


    
    def save_new_shortcut(self, dialog, name, urls_text):

        urls = [] 

        for line in urls_text.strip().split('\n'):
            line = line.strip()

            if line:
                urls.append(line)

        if not name or not urls:
            QtWidgets.QMessageBox.warning(self, 'Invalid input', 'Please enter a name and at least one valid URL.')
            return
        
        new_shortcut = {'name': name, 'urls': urls}

        self.shortcuts.append(new_shortcut)

        save_shortcuts(self.shortcuts)


        self.refresh_buttons()

        dialog.accept()
    


def window():
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = MyWindow()
        win.show()
        sys.exit(app.exec())


window()






# on my terminal, I did pip install pyinstaller and then I did 

# pyinstall --onefile opening_tab.py



# next project: add a edit feature where you can edit the name and the urls on each shortcut 

# expand the app beyond urls and make it also run programs. 





    

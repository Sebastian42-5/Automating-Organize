from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget
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



class ShortcutListWidget(QtWidgets.QListWidget):
    def __init__(self, parent= None):

        super().__init__(parent)

        self.parent = parent

    
    def mousePressEvent(self, event):
        
        item = self.itemAt(event.pos())

        if item:
            index = self.row(item)
            
            if event.button() == Qt.RightButton:
                
                self.parent.show_context_menu(index, self.mapToGlobal(event.pos()))
            
        super().mousePressEvent(event)


    def mouseDoubleClickEvent(self, event):

        item = self.itemAt(event.pos())

        if item and event.button() == Qt.LeftButton:
            index = self.row(item)
            shortcut = self.parent.shortcuts[index]

            self.parent.open_url_program(shortcut['urls'])


        super().mouseDoubleClickEvent(event)





class ShortcutTile(QWidget):

    def __init__(self, name, dark_mode = False):
        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(10, 8, 10, 8)

        label = QLabel(name)

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet('font-size: 14px;')


        layout.addWidget(label)

        self.setLayout(layout)

        self.apply_style(dark_mode)



    
    def apply_style(self, dark_mode):
        if dark_mode:
            self.setStyleSheet("""
            background-color: #3a3a3a;
            border: 2px solid #666;
            border-radius: 15px;
        """)
        
        else:
            self.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px solid #aaa;
            border-radius: 15px;
        """)





class MyWindow(QMainWindow):

    def __init__(self):

        super(MyWindow, self).__init__()

        self.setGeometry(200, 200, 300, 500)

        self.setWindowTitle('Tab opener!')

        self.setWindowIcon(QIcon(os.path.abspath('shark-icon-size_24.ico')))

        self.dark_mode = False

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



        self.shortcut_list = ShortcutListWidget(self)

        self.shortcut_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.shortcut_list.setDefaultDropAction(Qt.MoveAction)

        self.shortcut_list.setSpacing(4)

        self.shortcut_list.setStyleSheet('font-size: 14px; padding: 6px')

        self.layout_display.addWidget(self.shortcut_list)


        self.shortcut_list.model().rowsMoved.connect(self.save_shortcut_order)



        self.add_shortcut_buttons()

        self.create_btn = QPushButton('Create new shortcut')

        self.create_btn.setStyleSheet('margin: 10px; padding: 6px 12px;')

        self.create_btn.clicked.connect(self.open_create_dialog)

        self.layout_display.addWidget(self.create_btn, alignment = Qt.AlignRight)


        self.dark_mode_btn = QPushButton('Toggle Dark Mode')

        self.dark_mode_btn.setStyleSheet('margin: 10px; padding: 6px 12px;')

        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)


        self.layout_display.addWidget(self.dark_mode_btn, alignment = Qt.AlignRight)


    def toggle_dark_mode(self):

        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 8px;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #555;
            }

            QLineEdit, QPlainTextEdit {
                background-color: #3b3b3b;
                color: white;
                border: 1px solid #666;
                border-radius: 6px;
            }

            QListWidget {
                background-color: #2d2d2d;
                border: none;
            }

            QLabel {
                color: white;
            }
        """)
        else:
            self.setStyleSheet('')
        
        self.refresh_buttons()


    
    def delete_shortcut_by_name(self, name, widget):
        reply = QtWidgets.QMessageBox.question(self, 'Delete Shortcut', f'Are you sure you want to delete {name} ?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.shortcuts = [s for s in self.shortcuts if s['name'] != name]

            save_shortcuts(self.shortcuts)

            self.refresh_buttons()
    

    def show_context_menu(self, index, position):

        shortcut = self.shortcuts[index]

        menu = QtWidgets.QMenu()

        edit_action = menu.addAction('Edit')
        delete_action = menu.addAction('Delete')
        cancel_action = menu.addAction('Cancel')


        action = menu.exec_(position)

        if action == edit_action:
            self.edit_shortcut(index)
        
        elif action == delete_action:
            self.delete_shortcut_by_name(shortcut['name'], None)



    def save_shortcut_order(self):
        new_order = []
        for i in range(self.shortcut_list.count()):
            item = self.shortcut_list.item(i)

            old_index = item.data(Qt.UserRole)

            new_order.append(self.shortcuts[old_index])
        
        self.shortcuts = new_order

        save_shortcuts(self.shortcuts)



    def add_shortcut_buttons(self):

        self.shortcut_list.clear()

        for i, shortcut in enumerate(self.shortcuts):

            item = QtWidgets.QListWidgetItem()

            item.setSizeHint(QtCore.QSize(180, 80))

            self.shortcut_list.addItem(item)

            tile = ShortcutTile(shortcut['name'], self.dark_mode)

            tile.setToolTip('Double-click to open, or right-click for more options')

            self.shortcut_list.setItemWidget(item, tile)

            item.setData(Qt.UserRole, i)



    def open_url_program(self, urls):

        for path in urls:

            if path.startswith('http://') or path.startswith('https://'):
    
                webbrowser.open_new_tab(path)

                time.sleep(0.5)
        
            else:
                
                try:
                    os.startfile(path)
                    time.sleep(2)
                
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, 'Error', f'Could not open program: {path}/n/n{e}')


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

    
    def save_edited_shortcut(self, dialog, index, name_input, urls_input):

        name = name_input.text().strip()

        urls = []

        for line in urls_input.toPlainText().strip().split('\n'):
            line = line.strip()

            if line:
                urls.append(line)
        
        if not name or not urls:
            QtWidgets.QMessageBox.warning(self, 'Invalid input', 'Please enter a name and at least one valid URL/program.')

        self.shortcuts[index] = {'name': name, 'urls': urls}

        save_shortcuts(self.shortcuts)

        self.refresh_buttons()

        dialog.accept() 


    
    def edit_shortcut(self, index):

        shortcut = self.shortcuts[index]

        dialog = QtWidgets.QDialog(self)

        dialog.setWindowTitle('Edit shortcut')

        dialog.setFixedSize(300, 300)


        layout = QtWidgets.QVBoxLayout(dialog)

        name_label = QLabel('Edit name:')

        name_input = QtWidgets.QLineEdit(shortcut['name'])


        urls_label = QLabel('Edit URLs/programs (enter one per line):')

        urls_input = QtWidgets.QPlainTextEdit('\n'.join(shortcut['urls']))


        save_btn = QPushButton('Save changes')

        save_btn.clicked.connect(partial(self.save_edited_shortcut, dialog, index, name_input, urls_input))


        layout.addWidget(name_label)

        layout.addWidget(name_input)

        layout.addWidget(urls_label)

        layout.addWidget(urls_input)

        layout.addWidget(save_btn)


        dialog.setLayout(layout)

        dialog.exec_()


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





    

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QPushButton,
                           QLineEdit, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_events()
    
    def init_ui(self):
        self.setWindowTitle('ToDoリストアプリ')
        self.setGeometry(100, 100, 400, 300)
        
        main_layout = QVBoxLayout()
        
        title = QLabel('ToDoリスト')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        main_layout.addWidget(title)
        
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('新しいタスクを入力...')
        self.add_button = QPushButton('追加')
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)
        
        self.task_list = QListWidget()
        main_layout.addWidget(self.task_list)
        
        self.setLayout(main_layout)
    
    def setup_events(self):
        self.add_button.clicked.connect(self.add_task)
        self.task_input.returnPressed.connect(self.add_task)
        self.task_list.itemDoubleClicked.connect(self.edit_task)
    
    def edit_task(self, item):
        print(f"編集開始: {item.text()}")
        self.task_list.editItem(item)
    
    def add_task(self):
        task_text = self.task_input.text()
        if task_text.strip():
            # ここが重要な変更点！
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.task_list.addItem(item)
            self.task_input.clear()
            print(f"タスクを追加しました: {task_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_()) 
import sys
from PySide6.QtWidgets import (
    QMessageBox,
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # 初期のUI関数
    def init_ui(self):
        # ウィンドウタイトル
        self.setWindowTitle("PySide6 画面切り替えテスト")
        # ウィンドウサイズ
        self.setGeometry(100, 100, 800, 600)

        # メインウィンドウ
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # メインレイアウト
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        # 最初の画面の作成
        self.create_initial_screen()

        # 結果画面作成
        self.create_result_screen()

        # 両方のウィジェットをメインレイアウトに追加
        self.main_layout.addWidget(self.input_widget)
        self.main_layout.addWidget(self.result_widget)

        # 最初の画面表示
        self.show_initial_screen()

    def create_initial_screen(self):
        """入力画面のウィジェットを作成"""
        self.input_widget = QWidget()
        input_layout = QVBoxLayout()

        # ラベル
        label = QLabel("Hello PySide6")
        input_layout.addWidget(label)

        # テキストフォーム
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("ここにテキストを入力...")
        self.text_input.setMaximumHeight(200)
        input_layout.addWidget(self.text_input)

        # ボタン
        self.submit_button = QPushButton("クリックしてテキスト送信")
        input_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.show_result)

        input_layout.addStretch()

        self.input_widget.setLayout(input_layout)

    def create_result_screen(self):
        """結果画面のウィジェットを作成"""
        self.result_widget = QWidget()
        result_layout = QVBoxLayout()

        # タイトルラベル
        self.result_title = QLabel("入力内容は以下です。")
        result_layout.addWidget(self.result_title)

        # 結果表示ラベル
        self.result_display = QLabel()
        self.result_display.setWordWrap(True)  # 長い場合は改行
        self.result_display.setStyleSheet("background-color: lightgray; padding: 10px;")
        result_layout.addWidget(self.result_display)

        # 戻るボタン
        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(self.show_initial_screen)
        result_layout.addWidget(self.back_button)

        result_layout.addStretch()

        # レイアウトをウィジェットに設定
        self.result_widget.setLayout(result_layout)

    def show_initial_screen(self):
        """最初の画面を表示"""
        self.result_widget.hide()
        self.input_widget.show()

    def show_result(self):
        """結果画面を表示"""
        text = self.text_input.toPlainText().strip()

        # 入力チェック
        if not text:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("警告")
            msg.setText("テキストが入力されていません。")
            msg.exec()
            return
        self.result_display.setText(text)
        self.input_widget.hide()
        self.result_widget.show()


def main():
    app = QApplication(sys.argv)

    # メインのウィンドウ
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

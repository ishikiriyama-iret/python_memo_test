import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

from PIL import Image


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 画像ビューア")
        self.setGeometry(100, 100, 1000, 700)

        # 現在の画像データ
        self.current_pixmap = None
        self.original_pixmap = None
        self.current_file_path = None

        self.setup_ui()

    def setup_ui(self):
        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # メインレイアウト
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # コントロールパネル
        control_frame = QFrame()
        control_frame.setStyleSheet(
            "background-color: lightgray; border: 1px solid gray;"
        )
        control_frame.setFixedHeight(70)

        control_layout = QHBoxLayout()
        control_frame.setLayout(control_layout)

        # 読み込みボタン
        self.load_button = QPushButton("画像読み込み")
        self.load_button.setFixedSize(120, 40)
        self.load_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )
        self.load_button.clicked.connect(self.load_image)

        # クリアボタン
        self.clear_button = QPushButton("クリア")
        self.clear_button.setFixedSize(100, 40)
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #be1309;
            }
        """
        )
        self.clear_button.clicked.connect(self.clear_image)

        # ファイル情報ラベル
        self.file_info_label = QLabel("ファイルが読み込まれていません")
        self.file_info_label.setStyleSheet(
            "color: #333; font-size: 12px; background: transparent;"
        )

        # サイズ情報ラベル
        self.size_info_label = QLabel("")
        self.size_info_label.setStyleSheet(
            "color: #666; font-size: 10px; background: transparent;"
        )

        # コントロールパネルにウィジェットを追加
        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addWidget(self.file_info_label)
        control_layout.addStretch()
        control_layout.addWidget(self.size_info_label)

        # 画像表示エリア
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: red; border: 2px solid #ccc;")

        # 画像ラベル
        self.image_label = QLabel(
            "画像を読み込むには「画像読み込み」ボタンをクリックしてください"
        )
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(
            """
            color: #999; 
            font-size: 14px; 
            background-color: white;
            min-height: 400px;
        """
        )
        self.image_label.setMinimumSize(800, 500)

        self.scroll_area.setWidget(self.image_label)

        # レイアウトに追加
        main_layout.addWidget(control_frame)
        main_layout.addWidget(self.scroll_area)

        # ステータスバー
        self.statusBar().showMessage("準備完了")

    def load_image(self):
        """ファイルダイアログで画像を読み込み"""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("画像ファイルを選択")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilters(
            [
                "画像ファイル (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)",
                "PNG files (*.png)",
                "JPEG files (*.jpg *.jpeg)",
                "BMP files (*.bmp)",
                "GIF files (*.gif)",
                "すべてのファイル (*.*)",
            ]
        )

        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                print("選択した画像:::", file_paths)
                self.load_image_from_path(file_paths[0])

    def load_image_from_path(self, file_path):
        """指定されたパスから画像を読み込み"""
        try:
            # ファイルの存在確認
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

            # QPixmapで画像を読み込み
            pixmap = QPixmap(file_path)

            if pixmap.isNull():
                # QPixmapで読み込めない場合はPILを試す
                pil_image = Image.open(file_path)
                # PILからQPixmapに変換
                if pil_image.mode == "RGBA":
                    data = pil_image.tobytes("raw", "RGBA")
                    qimage = QImage(
                        data, pil_image.width, pil_image.height, QImage.Format_RGBA8888
                    )
                elif pil_image.mode == "RGB":
                    data = pil_image.tobytes("raw", "RGB")
                    qimage = QImage(
                        data, pil_image.width, pil_image.height, QImage.Format_RGB888
                    )
                else:
                    pil_image = pil_image.convert("RGB")
                    data = pil_image.tobytes("raw", "RGB")
                    qimage = QImage(
                        data, pil_image.width, pil_image.height, QImage.Format_RGB888
                    )

                pixmap = QPixmap.fromImage(qimage)

            if pixmap.isNull():
                raise ValueError("サポートされていない画像形式です")

            # 画像データを保存
            self.original_pixmap = pixmap
            self.current_file_path = file_path

            # 表示サイズに調整
            self.display_image()

            # UI更新
            filename = os.path.basename(file_path)
            self.file_info_label.setText(f"ファイル: {filename}")

            original_size = f"元サイズ: {pixmap.width()} x {pixmap.height()}"
            self.size_info_label.setText(original_size)

            self.statusBar().showMessage(f"画像を読み込みました: {filename}")

            print(f"画像を正常に読み込みました: {file_path}")
            print(f"サイズ: {pixmap.width()} x {pixmap.height()}")

        except Exception as e:
            error_msg = f"画像の読み込みに失敗しました:\n{str(e)}"
            QMessageBox.critical(self, "エラー", error_msg)
            self.statusBar().showMessage("読み込みエラー")
            print(f"エラー: {e}")

    def display_image(self):
        """画像を表示エリアに表示"""
        if self.original_pixmap is None:
            return

        # スクロールエリアのサイズを取得
        scroll_size = self.scroll_area.size()
        available_width = scroll_size.width() - 20
        available_height = scroll_size.height() - 20

        # 画像をスケーリング（アスペクト比を保持）
        scaled_pixmap = self.original_pixmap.scaled(
            available_width,
            available_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.current_pixmap = scaled_pixmap

        # 画像ラベルに表示
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.resize(scaled_pixmap.size())

        # 表示サイズ情報を更新
        display_size = (
            f" | 表示サイズ: {scaled_pixmap.width()} x {scaled_pixmap.height()}"
        )
        original_text = self.size_info_label.text().split(" |")[0]
        self.size_info_label.setText(original_text + display_size)

    def clear_image(self):
        """画像をクリア"""
        self.original_pixmap = None
        self.current_pixmap = None
        self.current_file_path = None

        # UIをリセット
        self.image_label.clear()
        self.image_label.setText(
            "画像を読み込むには「画像読み込み」ボタンをクリックしてください"
        )
        self.file_info_label.setText("ファイルが読み込まれていません")
        self.size_info_label.setText("")

        self.statusBar().showMessage("画像をクリアしました")
        print("画像をクリアしました")

    def resizeEvent(self, event):
        """ウィンドウサイズ変更時に画像を再表示"""
        super().resizeEvent(event)
        if self.original_pixmap is not None:
            self.display_image()


def main():
    """メイン関数"""
    app = QApplication(sys.argv)

    # アプリケーション情報
    app.setApplicationName("PySide6 画像ビューア")
    app.setApplicationVersion("1.0")

    # メインウィンドウを作成・表示
    viewer = ImageViewer()
    viewer.show()

    # イベントループ開始
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

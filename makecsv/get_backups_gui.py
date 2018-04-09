#!/usr/bin/env python
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QProgressBar)
from PyQt5.QtCore import QCoreApplication,QBasicTimer

from get_backups import GetBackups

class TermWindow(QWidget):
    def __init__(self, parent=None):
        super(TermWindow, self).__init__(parent)
        self.count = 0
        # QLineEditの作成
        self.input_ip = QLineEdit()
        self.input_ip.setFixedWidth(200)
        self.input_ip.setText('192.168.1.254')

        # QPushButtonの作成
        self.okButton = QPushButton("&Start")
        self.okButton.setFixedWidth(100)
        self.okButton.clicked.connect(self.ok)
        
        # LineLayoutの作成
        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("接続先のIPアドレスを入力"), 0, 0)
        lineLayout.addWidget(self.input_ip, 1, 0)
        lineLayout.addWidget(QLabel("下記「Start」ボタンを押すと取得開始"), 2, 0)
        lineLayout.addWidget(QLabel("下記ボタンが「Finished」になると取得終了"), 3, 0)

        # buttonLayoutの作成
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.okButton,0,0)

        # mainLayoutの作成
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(buttonLayout)
        # ウィンドウにレイアウトを追加
        self.setLayout(mainLayout)
        self.setWindowTitle("backup取得ウィンドウ")

        
    def ok(self):
        if self.count == 0:
            self.okButton.setText('Stop')
            print("start")
            self.okButton.clicked.connect(QCoreApplication.instance().quit)
            self.count =+ 1
        else:
            print("stop or finish:", self.count)
            # finishボタンをクリックしたら画面を閉じる
            self.okButton.clicked.connect(QCoreApplication.instance().quit)
            return
        
        # バックアップの取得
        gb = GetBackups(ip=self.input_ip.text())
        gb.get()
        
        self.okButton.setText('Finished')
        
        print(self.input_ip)


# In[2]:


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    # classの呼び出し
    term_window = TermWindow()
    term_window.show()
    
    app.aboutToQuit.connect(app.deleteLater)
    #プログラムをクリーンに終了する
    sys.exit(app.exec_())


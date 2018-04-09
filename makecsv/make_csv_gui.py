#!/usr/bin/env python

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QProgressBar)
from PyQt5.QtCore import QCoreApplication,QBasicTimer

import datetime
import zipfile
from make_csv import MakeCsv

class TermWindow(QWidget):
    def __init__(self, parent=None):
        super(TermWindow, self).__init__(parent)
        
        self.count = 0
        
        # 今日を取得
        today = datetime.datetime.today()
        # 当月1日の値を出す
        thismonth = datetime.datetime(today.year, today.month, 1)
        # 前月末日の値を出す
        lastmonth = thismonth + datetime.timedelta(days=-1)
        
        # QLineEditの作成
        self.s_Y = QLineEdit()
        self.s_Y.setFixedWidth(40)
        self.s_Y.setText(str(lastmonth.year))
        self.s_m = QLineEdit()
        self.s_m.setFixedWidth(20)
        self.s_m.setText(str(lastmonth.month))
        self.s_D = QLineEdit()
        self.s_D.setFixedWidth(20)
        self.s_D.setText("1")
        self.s_H = QLineEdit()
        self.s_H.setFixedWidth(20)
        self.s_H.setText("0")
        self.s_M = QLineEdit()
        self.s_M.setFixedWidth(20)
        self.s_M.setText("0")
        self.s_S = QLineEdit()
        self.s_S.setFixedWidth(20)
        self.s_S.setText("0")
        self.e_Y = QLineEdit()
        self.e_Y.setFixedWidth(40)
        self.e_Y.setText(str(today.year))
        self.e_m = QLineEdit()
        self.e_m.setFixedWidth(20)
        self.e_m.setText(str(today.month))
        self.e_D = QLineEdit()
        self.e_D.setFixedWidth(20)
        self.e_D.setText("1")
        self.e_H = QLineEdit()
        self.e_H.setFixedWidth(20)
        self.e_H.setText("0")
        self.e_M = QLineEdit()
        self.e_M.setFixedWidth(20)
        self.e_M.setText("0")
        self.e_S = QLineEdit()
        self.e_S.setFixedWidth(20)
        self.e_S.setText("0")
        

        # QPushButtonの作成
        self.okButton = QPushButton("&Start")
        self.okButton.setFixedWidth(100)
        self.okButton.clicked.connect(self.ok)
    
        
        # LineLayoutの作成
        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("開始日時"), 0, 0)
        lineLayout.addWidget(self.s_Y, 0, 1)
        lineLayout.addWidget(QLabel("年"), 0, 2)
        lineLayout.addWidget(self.s_m, 0, 3)
        lineLayout.addWidget(QLabel("月"), 0, 4)
        lineLayout.addWidget(self.s_D, 0, 5)
        lineLayout.addWidget(QLabel("日"), 0, 6)
        lineLayout.addWidget(self.s_H, 0, 7)
        lineLayout.addWidget(QLabel("時"), 0, 8)
        lineLayout.addWidget(self.s_M, 0, 9)
        lineLayout.addWidget(QLabel("分"), 0, 10)
        lineLayout.addWidget(self.s_S, 0, 11)
        lineLayout.addWidget(QLabel("秒"), 0, 12)
        lineLayout.addWidget(QLabel("終了日時"), 1, 0)
        lineLayout.addWidget(self.e_Y, 1, 1)
        lineLayout.addWidget(QLabel("年"), 1, 2)
        lineLayout.addWidget(self.e_m, 1, 3)
        lineLayout.addWidget(QLabel("月"), 1, 4)
        lineLayout.addWidget(self.e_D, 1, 5)
        lineLayout.addWidget(QLabel("日"), 1, 6)
        lineLayout.addWidget(self.e_H, 1, 7)
        lineLayout.addWidget(QLabel("時"), 1, 8)
        lineLayout.addWidget(self.e_M, 1, 9)
        lineLayout.addWidget(QLabel("分"), 1, 10)
        lineLayout.addWidget(self.e_S, 1, 11)
        lineLayout.addWidget(QLabel("秒"), 1, 12)
        lineLayout.addWidget(QLabel("下記「Start」ボタンを押すとcsv作成開始"), 2, 0)
        lineLayout.addWidget(QLabel("下記ボタンが「Finished」になるとcsv作成終了"), 3, 0)

        # buttonLayoutの作成
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.okButton,0,0)

        # mainLayoutの作成
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(buttonLayout)
        # ウィンドウにレイアウトを追加
        self.setLayout(mainLayout)
        self.setWindowTitle("CSV作成ウィンドウ")

        
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
        
        
        a = int(self.s_Y.text())
        b = int(self.s_m.text())
        c = int(self.s_D.text())
        d = int(self.s_H.text())
        e = int(self.s_M.text())
        f = int(self.s_S.text())
        g = int(self.e_Y.text())
        h = int(self.e_m.text())
        i = int(self.e_D.text())
        j = int(self.e_H.text())
        k = int(self.e_M.text())
        l = int(self.e_S.text())
        
        # csvの作成
        make_csv = MakeCsv((a,b,c,d,e,f),(g,h,i,j,k,l))
        make_csv.make('./data/pre.csv')
        
        # zipファイルの作成
        with zipfile.ZipFile('./data/pre.zip','w',zipfile.ZIP_DEFLATED) as myzip:
            myzip.write('./data/pre.csv')
            myzip.close()
        
        self.okButton.setText('Finished')
        
        print((a,b,c,d,e,f),(g,h,i,j,k,l))
        return (a,b,c,d,e,f),(g,h,i,j,k,l)


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


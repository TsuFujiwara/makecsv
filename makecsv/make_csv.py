
"""
sqlite3データベースの読込、csv,zipの出力
・出力されるcsvは00秒以外削除
author: Yuya Fujiwara 2018/4/6
"""
import pandas as pd
import numpy as np
import csv
import sqlite3
import time
import datetime

class MakeCsv():
    with open('backup_path.txt','r') as f:
        for row in f:
            print("backup_path: ",row.strip())
    nv=row.strip()+'/TrendLogConfig.csv'
    sp= row.strip()+'/monitored_object_data.sqlite3'
    
    def __init__(self, s_date, e_date, name_csv=nv, sqlite3_path=sp):
        self.s_date = s_date
        self.e_date = e_date
        self.name_csv= name_csv
        self.sqlite3_path = sqlite3_path
        
        self.s_Y,self.s_m,self.s_d,self.s_H,self.s_M,self.s_S = self.s_date
        self.e_Y,self.e_m,self.e_d,self.e_H,self.e_M,self.e_S = self.e_date
        
    
    # 日付変換関数の定義
    #datetime2timestamp
    def convert_dt2epoch(self,Y,M,D,h,m,s):
        """convert datetime object to epochtime
        http://d.hatena.ne.jp/tozawan/20110110/1294666583
        """
        
        dt = datetime.datetime(Y,M,D,h,m,s)
        epoch = time.mktime(dt.timetuple())
        return str(int(epoch))
    
    #timestamp2datetime
    def convert_epoch2dt(self,tm = time.time()):
        """convet epochtime to datetime object"""
        dt = datetime.datetime.fromtimestamp(tm)
        return dt
    
    
    # csvファイルの読み込み
    def read_csv(self):
        f = open(self.name_csv, "r")
        csv_data = csv.reader(f)
        data = [ e for e in csv_data]
        name_arr = np.array(data).T[1]
        return name_arr
        
        
    ## DBのデータ（レコード）取得
    def read_data(self,start_date='0', end_date='0'):
        list1 =[]
        list2 =[]
        df = pd.DataFrame()
        
        conn = sqlite3.connect(self.sqlite3_path)
        c = conn.cursor()
        
        # テーブル名の取得
        sql = 'select * from sqlite_master WHERE type="table"'
        c.execute(sql)
        
        for i,item in enumerate(c.fetchall()):
            if i == 0:
                continue
                
            # 各テーブル内データ（レコード）の取得
            sql = 'select * from '+item[1]+' WHERE log_datetime BETWEEN '+                   start_date+' AND '+end_date
                
            for row in c.execute(sql):
                list1.append(row[0])
                list2.append(row[2])
                
            array = np.array([list1,list2])
            list1 = []
            list2 = []
            df_tmp = pd.DataFrame(array.T)
            df_tmp = df_tmp.set_index(0)
            df = pd.concat([df,df_tmp],axis=1).astype('float32')
            
        # to_datetime で日時型に変換 / タイムゾーンを表すオフセットを適宜設定
        df.index = pd.to_datetime(df.index,unit="s",utc=True).tz_convert('Asia/Tokyo')
        # タイムゾーンは使わないので削除
        df.index = df.index.tz_localize(None)
        c.close()
        return df


    # 00秒データ以外は削除
    def drop_rows(self, df):
        drop_list = []
        for i,j in enumerate(df.index):
            #print(j.strftime('%Y-%m-%d %H:%M:%S'))
            if not j.strftime('%S') == '00':
                #print(i,j)
                drop_list.append(i)
                
        df_fix = df.drop(df.index[drop_list])
        return df_fix
    
    
    def make(self,file):
        # 日付の入力
        start_date = self.convert_dt2epoch(self.s_Y,self.s_m,self.s_d,self.s_H,self.s_M,self.s_S)
        end_date = self.convert_dt2epoch(self.e_Y,self.e_m,self.e_d,self.e_H,self.e_M,self.e_S)
        
        df = self.read_data(start_date,end_date)
        
        # カラム名の追加
        a = len(df.columns)
        df.columns = self.read_csv()[:a]
        
        # 0秒以外のデータドロップ
        df_fix = self.drop_rows(df)
        
        # DataFrameからcsvの作成
        df_fix.to_csv(file, encoding='shift-jis', float_format='%.1f')


# In[2]:


if __name__ == '__main__':
    import zipfile
    # csvの作成、作成時間計測
    start = time.time()
    
    # 今日を取得
    today = datetime.datetime.today()
    # 当月1日の値を出す
    thismonth = datetime.datetime(today.year, today.month, 1)
    # 前月末日の値を出す
    lastmonth = thismonth + datetime.timedelta(days=-1)
    
    # csvの作成
    make_csv = MakeCsv((lastmonth.year, lastmonth.month, 1, 0, 0, 0),(today.year, today.month, 1, 0, 0, 0))
    make_csv.make('./data/pre.csv')
    
    # zipファイルの作成
    with zipfile.ZipFile('./data/pre.zip','w',zipfile.ZIP_DEFLATED) as myzip:
        myzip.write('./data/pre.csv')
        myzip.close()
        
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


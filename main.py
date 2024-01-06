import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from kivy.properties import ObjectProperty
from kivymd.theming import ThemableBehavior
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.icon_definitions import md_icons
from kivy.uix.image import Image 
from kivy.uix.popup import Popup


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar2Kivy, FigureCanvasKivyAgg
from matplotlib.figure import Figure

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import datetime

import mysql.connector

conn=mysql.connector.connect(
    host="localhost", 
    password="sella04123",
    user="lalasel", 
    auth_plugin='mysql_native_password',
    database="pendaftaran")

cur=conn.cursor()

class LogInScreen(Screen):
     def login(self):
        nama = self.ids.nm.text
        username = self.ids.usr.text
        password = self.ids.psd.text


        sql1='SELECT * FROM dataform WHERE nama=%s and username=%s and password=%s'
        vals=(nama,username,password)
        cur.execute(sql1,vals)
        data=cur.fetchone()
        if data==None:
            Snackbar(text="Login Tidak Berhasil!",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    bg_color=(0, 0, 1, 1),
                    size_hint_x=.5).open()
        else:
            Snackbar(text="Login Berhasil!",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    bg_color=(0, 0, 1, 1),
                    size_hint_x=.5).open()
            self.manager.current='halaman'

class Registrasi(Screen):
    def regis(self):
        name = self.ids.nam.text
        username = self.ids.uesr.text
        password = self.ids.pesd.text

        sql='INSERT INTO dataform(nama,username,password) VALUES(%s,%s,%s)'
        vals=(name,username,password)
        cur.execute(sql,vals)  
        conn.commit()
        Snackbar(text="Registrasi Berhasil!",
                 snackbar_x="10dp",
                 snackbar_y="10dp",
                 bg_color=(0, 0, 1, 1),
                 size_hint_x=.5).open()


class HomePage(Screen):
    pass


class MainScreen(ScreenManager):
    pass

sm = ScreenManager()
sm.add_widget(LogInScreen(name='login'))
sm.add_widget(Registrasi(name='Register'))
sm.add_widget(HomePage(name='halaman'))

class Aplikasi(MDApp):
    file_manager = ObjectProperty(None)
    manager_open = False
    valid_selection = False
    selected_file = ""
    
    def build(self):
        
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        Window.bind(on_keyboard=self.events)
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('maincoba.kv')

    def file_manager_open(self, root_callback):
        self.root_callback = root_callback
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

        
    def select_path(self, path):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        
        if path:
            self.selected_file = path
            self.valid_selection = True
            toast(path)
            # self.kalibrasi_daya(self.selected_file)
            # self.kalibrasi_batangkendali(self.selected_file)
            # self.nilaikoefisiensuhu(self.selected_file)
            self.root_callback(self.selected_file)
            self.file_manager.close()
        else:
            self.valid_selection = False

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
        
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''
            
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
                return True
        return False
    
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_start(self):
        self.valid_selection = False
        self.selected_file = ""
   
    
    def kalibrasi_daya(self, file_path):
        if not self.valid_selection:
            return 
        try:
            data = []
            data2 = []
            res = []
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    data.append(row)
            res = data.pop(0)
            banyak_data = len(data)
            print("banyak data : ",banyak_data)


            for i in range (0,banyak_data):
                data2.append(data[i])
                

            # data_awalan=data[0]
            # print("data awal: ",data_awalan)
            #KOLOM DIJADIKAN LIST    
            A  = []
            B  = []
            C  = []
            D  = []
            E  = []
            A2 = []
            for i in data2:
                A.append(i[0])
                B.append(i[1])
                C.append(i[2])
                D.append(i[3])
                E.append(i[4])


            B2 = [float(i) for i in B]
            C2 = [float(i) for i in C]
            D2 = [float(i) for i in D]
            E2 = [float(i) for i in E]

            '''ini untuk data awal'''
            # print(A[0])

            '''ini untuk data akhir'''
            # print([i])

            for i in A:
                dt_object = datetime.strptime(i, "%H:%M:%S")
                
                Hour=dt_object.hour
                Menit=dt_object.minute
                Detiks=dt_object.second
                jumlahdetiknya=(Hour*3600)+(Menit*60)+Detiks
                A2.append(jumlahdetiknya)
            
            # print(type([i]))  
            # print(A2)
            # print(type(A2))

            Waktu_awal = datetime.strptime(A[0],"%H:%M:%S")
            waktu1_jam=Waktu_awal.hour
            waktu1_menit=Waktu_awal.minute
            waktu1_detiks=Waktu_awal.second
            jumlah1_detiknya=(waktu1_jam*3600)+(waktu1_menit*60)+waktu1_detiks
            print("Jumlah detik awal : ",jumlah1_detiknya)


            Waktu_akhir=datetime.strptime(i,"%H:%M:%S")
            waktu2_jam=Waktu_akhir.hour
            waktu2_menit=Waktu_akhir.minute
            waktu2_detiks=Waktu_akhir.second
            jumlah2_detiknya=(waktu2_jam*3600)+(waktu2_menit*60)+waktu2_detiks
            print("Jumlah detik akhir : ",jumlah2_detiknya)

            Banyak_detik_keseluruhan=jumlah2_detiknya-jumlah1_detiknya
            print("Jumlah detik keseluruhan : ",Banyak_detik_keseluruhan)
            W2= len(A2)

            rata_rata=Banyak_detik_keseluruhan/W2
            print("Rata-rata : ",rata_rata)

            F2 = list(np.arange(0,Banyak_detik_keseluruhan,rata_rata))

            col2=[]
            for i in range(1,len(A2)):
                hit = A2[i] - A2[i-1]
                col2.append(hit)

            # print(col2)
            # col2 = kolom untuk perbedaan waktu kedua dan pertama

            col3=[0]
            for i in range(len(col2)):
                coba = col2[i] - rata_rata
                col3.append(coba)
            # print(col3)
            # col3 = kolom untuk selisih perbedaan dengan rata-rata waktu
            indeks = []
            for i in range(len(col3)):
                if col3[i] >= 0:
                    indeks.append(i)
                    
            col4=[]

            B3 = []
            C3 = []
            D3 = []
            E3 = []
            F3 = []

            for i in indeks:
                col4.append(A2[i])
                B3.append(B2[i])
                C3.append(C2[i])
                D3.append(D2[i])
                E3.append(E2[i])
                F3.append(F2[i])
                
            columns = ['atrtemp', 'atr1temp', 'atr2temp', 'atr3temp']
            H = 19.0476
            results = ""

            for col in range(len(columns)):
                T = [B3, C3, D3, E3][col]
                t = F3
                y = np.array(T)
                x = np.array([[1, val] for val in t])

                xt = np.transpose(x)
                yt = np.transpose(y)
                m = np.dot(xt, x)
                m1 = np.linalg.inv(m)
                b = np.dot(np.dot(m1, xt), yt)

                RE = b[-1]
                P = H * RE * 3600

                print("Nilai Regresi", columns[col], "=", RE)
                print("Daya Pada", columns[col], "=", P)
                print("==========================================")
                results += f"Nilai Regresi {columns[col]} = {RE}\n"
                results += f"Daya Pada {columns[col]} = {P}\n"
                results += "==========================================\n"
            self.create_and_save_plot(columns, [B3, C3, D3, E3], t)
            self.show_results_popup(results)
            return results
        except IOError:
            print("Error opening the CSV file:", file_path)
    
    def create_and_save_plot(self, columns, data, t):
        self.fig, self.ax = plt.subplots()
        for col, d in enumerate(data):
            label = columns[col]
            self.ax.plot(t, d, label=label)
            self.ax.scatter(t, d, label=label)

        self.ax.set_xlabel('Waktu')
        self.ax.set_ylabel('Temperatur')
        self.ax.set_title('Waktu Terhadap Temperatur')
        self.ax.legend()

        # Save the plot as an image file.
        # self.add_widget(self.graph)
        
    
    def show_results_popup(self, results):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        
        open_graph = Button(text='grafik', size_hint=(1, 0.2) )
        content.add_widget(label)
        content.add_widget(close_button)
        
        content.add_widget(open_graph)
        popup = Popup(title='Calculation Results', content=content, size_hint=(None, None), size=(400, 400))
        close_button.bind(on_release=popup.dismiss)
        open_graph.bind(on_release=self.display_plot)
        popup.open()
    
    
    def display_plot(self, instance):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        save_button = Button(text='Save', size_hint=(1, 0.2))
        # plot_image = Image(source='plot.png')
        
        self.graph = FigureCanvasKivyAgg(figure=self.fig)
        
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)

        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()
        
        popup = Popup(title='Plot', content=plot_container, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    def create_and_save_plot2(self,result_df, d_values):
        self.fig2, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values)  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Pengatur')
        self.ax.legend()

        # plt.show()
    
    def show_results2_popup(self, results2):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results2)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        open_graph = Button(text='grafik', size_hint=(1, 0.2) )
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(open_graph)
        popup = Popup(title='BATANG KENDALI PENGATUR', content=content, size_hint=(None, None), size=(400, 500))
        close_button.bind(on_release=popup.dismiss)
        open_graph.bind(on_release=self.display_plot2)
        popup.open()
    
    def display_plot2(self, instance):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        save_button = Button(text='Save', size_hint=(1, 0.2))
        self.graph = FigureCanvasKivyAgg(figure=self.fig2)
        self.fig.savefig('gambar')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    
    def create_and_save_plot3(self,result_df, d_values2):
        self.fig1, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values2)  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values2)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Kompensasi')
        self.ax.legend()

        # plt.show()
    
    def show_results3_popup(self, results3):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results3)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        open_graph = Button(text='grafik', size_hint=(1, 0.2) )
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(open_graph)
        popup = Popup(title='BATANG KENDALI KOMPENSASI', content=content, size_hint=(None, None), size=(400, 500))
        close_button.bind(on_release=popup.dismiss)
        open_graph.bind(on_release=self.display_plot3)
        popup.open()
    
    def display_plot3(self, instance):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        save_button = Button(text='Save', size_hint=(1, 0.2))
        self.graph = FigureCanvasKivyAgg(figure=self.fig1)
        self.fig.savefig('gambar')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    def create_and_save_plot4(self,result_df, d_values3):
        self.fig, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values3, label='Some Label')  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values3)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Pengaman')
        self.ax.legend()

        # plt.show()
    
    def show_results4_popup(self, results4):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results4)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        open_graph = Button(text='grafik', size_hint=(1, 0.2) )
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(open_graph)
        popup = Popup(title='BATANG KENDALI PENGAMAN', content=content, size_hint=(None, None), size=(400, 500))
        close_button.bind(on_release=popup.dismiss)
        open_graph.bind(on_release=self.display_plot4)
        popup.open()
    
    def display_plot4(self, instance):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        save_button = Button(text='Save', size_hint=(1, 0.2))
        self.graph = FigureCanvasKivyAgg(figure=self.fig)
        self.fig.savefig('plot')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()

        
    
    def show_results5_popup(self, results5):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results5)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        content.add_widget(label)
        content.add_widget(close_button)
        popup = Popup(title='Calculation Results', content=content, size_hint=(None, None), size=(600, 400))
        close_button.bind(on_release=popup.dismiss)
        popup.open()
    
    def show_results6_popup(self, results):
        content = BoxLayout(orientation='vertical', padding=20)
        label = Label(text=results)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        content.add_widget(label)
        content.add_widget(close_button)
        popup = Popup(title='Calculation Results', content=content, size_hint=(None, None), size=(600, 400))
        close_button.bind(on_release=popup.dismiss)
        popup.open()
    
    def kalibrasi_batangkendali (self, file_path):
        if not self.valid_selection:
            return 
        try:
            df= pd.read_csv(file_path)
            # df= pd.read_csv('CR Calibration 14 april231.csv')

            # setelah diurutkan
            ac=df.loc[::-1].reset_index(drop=True)
            # pemilihan kolom
            bc=ac.loc[:,['htime','safe','shim','reg','reactivity']]
            df = pd.DataFrame(bc)

            # Inisialisasi list untuk menyimpan baris yang memenuhi kriteria
            stabil_pengatur = []
            stabil_kompensasi = []
            stabil_pengaman = []
            parts = []
            current_part = []

            # =============BATANG KENDALI PENGATUR===================

            # ========KONDISI 1 (KRITIS)==============
            for index, row in df.iterrows():
                if row['safe'] == 100:
                    if row['shim'] == 100:
                        if -0.3 < row['reactivity'] < 0:
                            if 10 < row['reg'] <16:
                                stabil_pengatur.append(row)
                                
            selected1_df = pd.DataFrame(stabil_pengatur)
            hasil1 = selected1_df['reg'].mode().iloc[0]


            # ========KONDISI 2 (REAKTIVITAS)==============
            filtered_data = df[df['reactivity'] > 15]
            threshold = 16
            continue_adding = True

            for index, row in df.iterrows():
                if continue_adding and row['safe'] == 100 and row['reactivity'] > threshold and row['reg'] <= 100:
                    current_part.append(row)
                elif current_part:
                    if row['reg'] == 100:
                        current_part.append(row)
                        parts.append(pd.DataFrame(current_part))
                        current_part = []
                        continue_adding = False
                    else:
                        parts.append(pd.DataFrame(current_part))
                        current_part = []

            for i, part in enumerate(parts):
                max_rec = part['reactivity'].max()

            result_df = pd.DataFrame(columns=['reg', 'reactivity'])
            result_df = pd.concat([part.loc[part['reactivity'].idxmax(), ['reg', 'reactivity']].to_frame().T for part in parts], ignore_index=True)

            # ========KONDISI 3 (CORE EXCESS)==============
            for index, row in df.iterrows():
                if row['safe'] == 100:
                    if row['shim'] == 100:
                        if -30< row['reactivity'] < -12:
                            if 0<= row['reg'] <=hasil1:
                                stabil_pengatur.append(row)
                                
            selectedd1_df = pd.DataFrame(stabil_pengatur)
            hasill1 = selectedd1_df['reactivity']*(-1)
            rect=hasill1.max()

            # ======== TABEL DATA==============
            baris_baru = pd.DataFrame({'reg': [0,hasil1], 'reactivity': [0,rect]})
            result_df = pd.concat([baris_baru, result_df], ignore_index=True)
            result_df = result_df.rename(columns={'reg': 'posisi', 'reactivity':'reaktivitas'})

            c1=result_df['reaktivitas']
            c_list1 = result_df['reaktivitas'].tolist()

            # ========PERHITUNGAN INTEGRAL==============
            d_values = [0]

            for i in range(1, len(c_list1)):
                d_values.append(d_values[i-1] + c_list1[i])

            for i, d in enumerate(d_values):
                as1=d
                # print(d)

            result_df['Integral'] =d_values
            result_df = result_df.reset_index(drop=True)
            result2= str(result_df)
            self.show_results2_popup(result2)
            self.create_and_save_plot2(result_df, d_values)
            # print(result_df)

            # ========PENGOLAHAN DATA==============
            total_pengatur=result_df['reaktivitas'].sum()
            core_pengatur=total_pengatur-rect
            # print('total_pengatur: ',total_pengatur)
            # print('core_pengatur',core_pengatur)
            

            # ========GRAFIK==============
            # plt.plot(result_df['posisi'],d_values)
            # plt.scatter(result_df['posisi'],d_values)
            # plt.xlabel ('Posisi')
            # plt.ylabel ('Reaktivitas')
            # plt.title ('Grafik Integral Batang Kendali Pengatur')
            # plt.show()



            # =========BATANG KENDALI KOMPENSASI===========

            # ========KONDISI 1==============
            for index, row in df.iterrows():
                if row['safe'] == 100:
                    if row['reg'] == 100:
                        if 0< row['reactivity'] < 0.5:
                            stabil_kompensasi.append(row)

            selected2_df = pd.DataFrame(stabil_kompensasi)
            hasil2 = selected2_df['shim'].mode().iloc[0]

            # ========KONDISI 2==============
            filtered_data = df[df['reactivity'] >= 3]
            # Create an empty list to store the parts
            parts = []
            # Set a threshold for the 'rec' values to split the data into parts
            threshold = 3
            # Initialize variables for the loop
            current_part = []
            result_data = []
            # Iterate through the data
            continue_adding = True 
            # Iterate through the data
            for index, row in df.loc[selected2_df.index[0]:].iterrows():
                if continue_adding and row['safe'] == 100 and row['reactivity'] >= threshold and row['shim'] <= 100:
                    current_part.append(row)
                elif current_part:
                    # Stop adding rows once 'reg' reaches 100
                    if row['shim'] == 100:
                        current_part.append(row)
                        parts.append(pd.DataFrame(current_part))
                        current_part = []
                        continue_adding = False
                    else:
                        parts.append(pd.DataFrame(current_part))
                        current_part = []

            for part in parts:
                if not part.empty :
                    # Exclude the rows where 'shim' is 100 for Bagian 10 and Bagian 11
                    if part['shim'].iloc[0] < 100 and part['reg'].iloc[-1] < 100:
                        max_row = part.loc[part['reactivity'].idxmax(), ['shim', 'reactivity']]
                        result_data.append(max_row.to_dict())

            # Create the resulting DataFrame
            result_df = pd.DataFrame(result_data)

            # Print the resulting DataFrame
            # print(result_df)

            # ========KONDISI 3==============
            for index, row in df.iterrows():
                # Check apakah Nilai1 sama dengan 100
                if 95<= row['safe'] <= 100:
                    # Jika ya, check kriteria Nilai4
                    if row['reg'] == 100:
                        if -3< row['reactivity'] < -0.05:
                            if 0<= row['shim'] <=hasil2:
                                # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                                stabil_kompensasi.append(row)
                                

            # Buat DataFrame baru dari baris yang memenuhi kriteria
            selectedd2_df = pd.DataFrame(stabil_kompensasi)
            hasill2 = selectedd2_df['reactivity']*(-100)
            rect2=hasill2.max()
            # Print DataFrame yang memenuhi kriteria
            # print('f',selectedd2_df)
            # print('fg',hasill2)
            # print('ff',rect2)

            # ======== TABEL DATA==============
            baris_baru = pd.DataFrame({'shim': [0,hasil2], 'reactivity': [0,rect2]})
            result_df = pd.concat([baris_baru, result_df], ignore_index=True)
            result_df = result_df.rename(columns={'shim': 'posisi', 'reactivity':'reaktivitas'})
            # print(result_df)

            c2=result_df['reaktivitas']
            # print(c1)
            c_list2 = result_df['reaktivitas'].tolist()
            # print(c_list1)

            # ========PERHITUNGAN INTEGRAL==============
            d_values2 = [0]

            # Calculate d values using a loop
            for i in range(1, len(c_list2)):
                d_values2.append(d_values2[i-1] + c_list2[i])

            # Print the results
            for i, d in enumerate(d_values2):
                as1=d
                # print(d)

            result_df['Integral'] =d_values2
            result_df = result_df.reset_index(drop=True)
            # print(result_df)
            result3= str(result_df)
            self.show_results3_popup(result3)
            self.create_and_save_plot3(result_df, d_values2)
            

            # ========PENGOLAHAN DATA==============
            total_kompensasi=result_df['reaktivitas'].sum()
            core_kompensasi=total_kompensasi-rect2
            # print('total_kompensasi: ',total_kompensasi)
            # print('core_kompensasi',core_kompensasi)

            # ========GRAFIK==============
            # plt.plot(result_df['posisi'],d_values2)
            # plt.scatter(result_df['posisi'],d_values2)
            # plt.xlabel ('Posisi')
            # plt.ylabel ('Reaktivitas')
            # plt.title ('Grafik Integral Batang Kendali Kompensasi')
            # plt.show()

            # # =========BATANG KENDALI PENGAMAN===========

            # ========KONDISI 1==============
            for index, row in df.iterrows():
                # Check apakah Nilai1 sama dengan 100
                if row['shim'] == 100:
                    # Jika ya, check kriteria Nilai4
                    if row['reg'] == 100:
                        if 0< row['reactivity'] < 0.5:
                            # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                            stabil_pengaman.append(row)

            # Buat DataFrame baru dari baris yang memenuhi kriteria
            selected3_df = pd.DataFrame(stabil_pengaman)
            hasil3 = selected3_df['safe'].mode().iloc[0]
            # Print DataFrame yang memenuhi kriteria
            # print(selected3_df)
            # print(hasil3)

            # ========KONDISI 2==============
            filtered_data = df[df['reactivity'] >= 3]
            # Create an empty list to store the parts
            parts = []
            # Set a threshold for the 'rec' values to split the data into parts
            threshold = 3
            # Initialize variables for the loop
            current_part = []
            result_data = []
            # Iterate through the data
            continue_adding = True 
            # Iterate through the data
            # shim>reg
            for index, row in df.loc[selected3_df.index[0]:].iterrows():
                if continue_adding:
                    if (row['reg'] == 100 and row['reactivity'] >= threshold and row['safe'] <= 100) or \
                    (row['shim'] == 100 and row['reactivity'] >= threshold and row['safe'] <= 100):
                        current_part.append(row)
                    elif current_part:
                        # Stop adding rows once 'reg' or 'shim' reaches 100
                        if row['safe'] == 100:
                            current_part.append(row)
                            parts.append(pd.DataFrame(current_part))
                            current_part = []
                            continue_adding = False
                        else:
                            parts.append(pd.DataFrame(current_part))
                            current_part = []

            for part in parts:
                if not part.empty and part['safe'].iloc[0] < 100:
                    if (part['shim'].iloc[-1] < 100) or (part['reg'].iloc[-1] < 100):
                        max_row = part.loc[part['reactivity'].idxmax(), ['safe', 'reactivity']]
                        result_data.append(max_row.to_dict())

            # Create the resulting DataFrame
            result_df = pd.DataFrame(result_data)

            # # Print the resulting DataFrame
            # print('d',part)
            # print('f',result_df)

            # ========KONDISI 3==============
            for index, row in df.iterrows():
                # Check apakah Nilai1 sama dengan 100
                if 95<= row['reg'] <= 100:
                # if 95<= row['shim'] <= 100:
                    # Jika ya, check kriteria Nilai4
                    if row['shim'] == 100:
                    # if row['reg'] == 100:
                        if -2< row['reactivity'] < -0.02:
                            if 0<= row['safe'] <=hasil3 :
                                # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                                stabil_pengaman.append(row)
                                

            # Buat DataFrame baru dari baris yang memenuhi kriteria
            selectedd3_df = pd.DataFrame(stabil_pengaman)
            hasill3 = selectedd3_df['reactivity']*(-100)
            rect3=hasill3.max()
            # Print DataFrame yang memenuhi kriteria
            # print('f',selectedd3_df)
            # print('fg',hasill3)
            # print('fh',rect3)

            # ======== TABEL DATA==============
            baris_baru = pd.DataFrame({'safe': [0,hasil3], 'reactivity': [0,rect3]})
            result_df = pd.concat([baris_baru, result_df], ignore_index=True)
            result_df = result_df.rename(columns={'safe': 'posisi', 'reactivity':'reaktivitas'})
            # print(result_df)

            c3=result_df['reaktivitas']
            # print(c1)
            c_list3 = result_df['reaktivitas'].tolist()
            # print(c_list1)

            # ========PERHITUNGAN INTEGRAL==============
            d_values3 = [0]

            # Calculate d values using a loop
            for i in range(1, len(c_list3)):
                d_values3.append(d_values3[i-1] + c_list3[i])

            # Print the results
            for i, d in enumerate(d_values3):
                as1=d
                # print(d)

            result_df['Integral'] =d_values3
            result_df = result_df.reset_index(drop=True)
            # print(result_df)
            result4= str(result_df)
            self.show_results4_popup(result4)
            self.create_and_save_plot4(result_df, d_values3)
            
            gb4=result_df['posisi']

            # ========PENGOLAHAN DATA==============
            total_pengaman=result_df['reaktivitas'].sum()
            core_pengaman=total_pengaman-rect3
            # print('total_pengaman: ',total_pengaman)
            # print('core_pengaman',core_pengaman)

            # ========GRAFIK==============
            # plt.plot(gb4,d_values3)
            # plt.scatter(gb4,d_values3)
            # plt.xlabel ('Posisi')
            # plt.ylabel ('Reaktivitas')
            # plt.title ('Grafik Integral Batang Kendali Pengaman')
            # plt.show()

            # =========PENGOLAHAN REAKTIVITAS BATANG KENDALI=========
            total_reaktivitas=(total_pengatur+total_kompensasi+total_pengaman)
            persen_total=total_reaktivitas/100
            core_excess=((core_pengatur+core_kompensasi+core_pengaman)/3)
            persen_core = core_excess/100
            shutdown_margin=(total_reaktivitas-core_excess-total_kompensasi)
            persen_shutdown = shutdown_margin/100
            results5 =f"Reaktivitas Batang pengatur={total_pengatur} cent \nCore Excess pengatur={core_pengatur} cent\nReaktivitas Batang kompensasi={total_kompensasi} cent \nCore Excess kompensasi={core_kompensasi}\nReaktivitas Batang Pengaman={total_pengaman} cent\nCore Excess Pengaman={core_pengaman}\n\ntotal_reaktivitas = {total_reaktivitas} atau {persen_total}\ncore_excess= {core_excess} atau {persen_total}%%\nshutdown_margin={shutdown_margin}cent atau {persen_shutdown}%%"
            
        
            self.show_results5_popup(results5)
            
            # print('total_reaktivitas : %d cent atau %s %%' %(total_reaktivitas,persen_total))
            # print('core_excess : %d cent atau %s %%' %(core_excess,persen_core))
            # print('shutdown_margin : %d cent atau %s %%' %(shutdown_margin,persen_shutdown))
        except IOError:
            print("Error opening the CSV file:", file_path)
    
    
    
    
    def nilaikoefisiensuhu (self, file_path):
        if not self.valid_selection:
            return 
        try:
            df= pd.read_csv(file_path)
            # df= pd.read_csv('practice1_10_11_2023.csv')
            bc=df.loc[:,['Time','Power NP1000','Safety rod','Compensation rod','Regulator rod','primary flow','IFE temp']]
            df = pd.DataFrame(bc)

            # ======KONDISI1======
            index_prim_zero = df[df['primary flow'] == 0].index[0]

            # Extract the 5 rows before primary flow = 0
            hasil_df = df.iloc[max(0, index_prim_zero - 15):index_prim_zero]
            data_reg = hasil_df['Regulator rod']
            hasil_reg = hasil_df['Regulator rod'].mean()
            data_prim = hasil_df['IFE temp']
            hasil_prim = hasil_df['IFE temp'].mean()

            # print(hasil_df)
            # # print(data_reg)
            # print('Rata-Rata Posisi Batang Kendali Kondisi 1:',hasil_reg) #Nilai rata-rata batang kendali pengatur KONDISI1
            # # print(data_prim)
            # print('Rata-Rata IFE temp Kondisi 1: ',hasil_prim) #Nilai rata-rata IFE temp KONDISI1

            # ======PERHITUNGAN======
            x1=hasil_reg
            y1 = -0.0002 * x1**3 + 0.0181 * x1**2 + 1.8314 * x1 - 2.4464

            # print('Reaktivitas Batang Kendali Pengatur Kondisi 1: ',y1)

            # ======KONDISI2======
            setelah_daya= df[(df['primary flow'] == 0) & (df['Safety rod'] == 100) & (df['Power NP1000'] >= 100)]

            # Find the index of the first matching row
            if not setelah_daya.empty:
                start_index = setelah_daya.index[0]

                # Retrieve the next 10 rows after the matching row
                hasil_2 = df.iloc[start_index + 51: start_index + 61]
                # print(hasil_2)
                data_reg2 = hasil_2['Regulator rod']
                hasil_reg2 = hasil_2['Regulator rod'].mean() 
                data_prim2 = hasil_2['IFE temp']
                hasil_prim2 = hasil_2['IFE temp'].mean()
                # Display the result
                # print(data_reg2)
                # print('Rata-Rata Posisi Batang Kendali Kondisi 2:',hasil_reg2) #Nilai rata-rata batang kendali pengatur KONDISI2
                # print(data_prim2)
                # print('Rata-Rata IFE temp Kondisi 2: ',hasil_prim2) #Nilai rata-rata IFE temp KONDISI2

                # ======PERHITUNGAN======
                x=hasil_reg2
                Y = -0.0002 * x**3 + 0.0181 * x**2 + 1.8314 * x - 2.4464

                # print('Reaktivitas Batang Kendali Pengatur Kondisi 2: ',Y)
                
            else:
                print("No matching rows.")
                
            # ======PERHITUNGAN KOEFISIEN REAKTIVITAS SUHU BAHAN BAKAR======
            R=abs(Y-y1)
            R1 = str(R)
            T=(hasil_prim2-hasil_prim)
            T1=str(T)
            K=R/T
            
            print("Nilai Koefisien Negatif Temperatur: ",K)
            
            results =f"Reaktivitas Kondisi 1={y1}\nReaktivitas Kondisi 2={Y}\nRata-Rata IFE temp Kondisi 1={hasil_prim}\nRata-Rata IFE temp Kondisi 2={hasil_prim2}\nSelisih Reaktivitas= {R1}\nSelisih Temperatur= {T1}\nNilai Koefisien Negatif Temperatur= {K}"

            self.show_results6_popup(results)
            return results
        except IOError:
            print("Error opening the CSV file:", file_path)
    
    def close_application(self):
        MDApp.get_running_app().stop()
        Window.close()
    
    

if __name__ == '__main__':
    Aplikasi().run()
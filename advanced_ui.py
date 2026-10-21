
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-01
Nombre del Soft: 🎧 PRO PLAYER X_v2
Distribución: Gratuito  -->OPENSOURCE<--
'''
##=========================================================================================
import cv2
import os, sys
import random
import threading
from threading import Thread

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QMessageBox, QFileDialog, QScrollArea, QTextEdit, 
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QShortcut, QApplication,
    QPushButton, QListWidget, QLabel, QStackedWidget, QGraphicsOpacityEffect, QDialog
)
from PyQt5.QtCore import QPropertyAnimation, Qt, QTimer
from PyQt5.QtGui import QMovie, QPixmap, QKeySequence, QIcon, QPalette, QBrush, QFont, QImage

from player import AudioPlayer
from loader import FileLoader
from load_image_slide import load_images
from Video_Player_Widget_Logic_v3 import VideoPlayerWidget

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
##====================================================================================
# --- Clase para manejo de rutas de recursos (Sin cambios) ---
##====================================================================================
class Path():

    # =========================
    # ✨ Debuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================
    def resource_path(relative_path):    ## Forma #1 resource_path(relative_path)
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # =========================
    # ✨ Debuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================
    def resource_path_app():    ## Forma #2 resource_path_app()

        try:
            path_app = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

        except Exception as e:
            print(e)

        except IOError as error:
            print( error )

        return path_app
##====================================================================================
# --- Clase para cargar los Gif´s
##====================================================================================
class GifControlWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setFixedSize(420, 260)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)

        bg_path = Path.resource_path("assets/img_btn/1.jpg")
        pixmap = QPixmap(bg_path)

        palette = QPalette()
        palette.setBrush(
            QPalette.Window,
            QBrush(
                pixmap.scaled(
                    self.size(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
            )
        )

        self.setPalette(palette)

        # 🌌 IMAGEN DE FONDO
        bg_path = Path.resource_path("assets\\img_btn\\2.jpg").replace("\\", "/")
        
        self.setStyleSheet(f"""
            QWidget {{
                background-image: url("{bg_path}");
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        """)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 🔘 BOTÓN
        self.btn = QPushButton("➕ Agregar GIF")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setFixedHeight(48)
        self.btn.setFixedWidth(260)

        # 🎨 Estilo del botón (overlay elegante)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 170);
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,80);
            }
            QPushButton:hover {
                background-color: rgba(0, 150, 255, 200);
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(0, 110, 200, 220);
            }
        """)

        self.btn.clicked.connect(self.add_gif)

        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.center()

    # ======================================================
    # Colaca en el Centro la APP
    # ======================================================
    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # =========================
    # ✨ Busqueda de Más Gif´s, a la List Gif
    # =========================
    def add_gif(self):

        if self.parent.player.playlist == []:
            pass
        else:

            try:

                new_gif, _ = QFileDialog.getOpenFileNames(self, "Open file", "/gui/desktop", "GIF files: (*.gif)")

                for plus_gif in new_gif:

                    self.parent.filename_gif.append(plus_gif)

                path = self.parent.filename_gif[self.parent.index_gif]

                self.parent.load_new_gif(path)

            except Exception as e:
                print(f"Error en: [add_gif-L152|-|Exception: L171]  {e}")

##====================================================================================
# --- Clase Principal de toda la APP-DESCK
##====================================================================================
class AdvancedUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎧 PRO PLAYER X_v2")
        #self.setGeometry(100, 100, 1100, 650)

        # Icono
        icon_path = Path.resource_path("assets\\Ico\\logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.center_on_screen()

        self.player = AudioPlayer()
        self.player.track_changed.connect(self.aviso)
        self.player.positionChanged.connect(self.position)
        self.player.durationChanged.connect(self.duration)

        self.loader = FileLoader()

        self.pages = []
        self.init_ui()
        self.apply_style()

    # =========================
    # 🧱 UI BASE
    # =========================
    def init_ui(self):

        self.video_player = VideoPlayerWidget()
        
        main = QHBoxLayout()

        self.images = []
        self.filename_gif = []
        self.image_paths = []

        self.current_video_list = []

        self.current_image = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)

        self.pause_play = True        
        self.GIF_PAUSED = True
        self.SLIDE_PAUSED = True
        self.des_ocult = True
        self.aleatory_track = True

        self.vol = 05.00
        self.index = 0
        self.index_gif = 0

        self.gif_path = ""
        self.size_1 = 550
        self.size_2 = 550

        self.Pocicion = ""
        self.Duracion = ""
        self.A = ""

        # 🔥 SIDEBAR
        self.sidebar_widget = QWidget()
        sidebar = QVBoxLayout(self.sidebar_widget)

        self.sidebar_widget.setFixedWidth(180)  # 👈 ancho pequeño

        btn_home = QPushButton("🏠 Home")
        btn_playlist = QPushButton("🎵 Playlist")
        btn_gif = QPushButton("🎞️ Visualizer")
        btn_video = QPushButton("🎬 Video")
        btn_video_list = QPushButton("📂 Lista Videos")
        btn_video.setMinimumHeight(40)

        self.title_track = QLabel()
        self.title_track.setAlignment(Qt.AlignCenter)
        self.title_track.setFixedHeight(15)
        self.title_track.hide()

        self.btn_tm = QPushButton("🕒 - 🕒")
        self.btn_tm.setFixedWidth(180)
        self.btn_tm.clicked.connect(self.Ocultar_Desocultar)

        sidebar.addWidget(btn_home)
        sidebar.addWidget(btn_playlist)
        sidebar.addWidget(btn_gif)
        sidebar.addWidget(btn_video)
        sidebar.addWidget(btn_video_list)
        sidebar.addStretch()

        # 🔥 STACK
        self.stack = QStackedWidget()

        self.page_home = self.build_home()
        self.page_playlist = self.build_playlist()
        self.page_gif = self.build_gif_panel()
        self.page_video = self.build_video_panel()
        self.page_video_list = New_Win2(self.current_video_list, self.video_player)

        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_playlist)
        self.stack.addWidget(self.page_gif)        
        self.stack.addWidget(self.page_video)
        self.stack.addWidget(self.page_video_list)

        # 🔗 NAV
        btn_home.clicked.connect(lambda: self.switch_page(0))
        btn_playlist.clicked.connect(lambda: self.switch_page(1))
        btn_gif.clicked.connect(lambda: self.switch_page(2))
        btn_video.clicked.connect(lambda: self.switch_page(3))
        btn_video_list.clicked.connect(lambda: self.switch_page(4))

        # 🔥 ROOT
        container = QWidget()
        # main.addWidget(self.sidebar_widget)
        # main.addWidget(self.stack, 5)

        main.addWidget(self.sidebar_widget, 0)
        main.addWidget(self.stack, 1)

        container.setLayout(main)
        self.setCentralWidget(container)

        # Atajo Ctrl + P para mostrar y ocultar el Panel Izquierdo
        ts_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        ts_shortcut.activated.connect(self.toggle_sidebar)

        # Atajo Ctrl + G para agregar mas Gif´s a la List-Gif
        og_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        og_shortcut.activated.connect(self.open_gif)

        # Atajo Ctrl + I para mostrar información del software
        info_software = QShortcut(QKeySequence('Ctrl+I'), self)
        info_software.activated.connect(self.show_app_info)

        # Atajo Ctrl + K para mostrar información Sobre las Teclas de Atajo
        key_info_software = QShortcut(QKeySequence('Ctrl+K'), self)
        key_info_software.activated.connect(self.key_app_info)

        # Atajo Ctrl + N Avansa 1 Track
        key_next_software = QShortcut(QKeySequence('Ctrl+N'), self)
        key_next_software.activated.connect(self.next_track)

        # Atajo Ctrl + F Regresa 1n Track
        key_atras_software = QShortcut(QKeySequence('Ctrl+F'), self)
        key_atras_software.activated.connect(self.prev_track)

        # Atajo Ctrl + A Coloca el Index en forma Aleatorio
        key_Aleatory_software = QShortcut(QKeySequence('Ctrl+A'), self)
        key_Aleatory_software.activated.connect(self.aleatory_track_list)

        self.load_images(load_images)

        self.show_app_info()
        self.movie.setPaused(False)

##=========================================================================================================
##=========================================================================================================

## Metodo para Acortar el Titulo si este fuera muy Largo (Alternativo)
    def acortando_title(self, text, length=60):

        name, ext = os.path.splitext(text)

        if text:

            if len(text) <= length:
                return text

            else:
                return f"{' '.join(text[:length+1].split(' ')[0:-1])} ....{ext}"

## Metodo para Colocar en el Titulo Lo Que Deseemos que Hira, en este Caso el Titulo del Video
    def Actualizando_Title(self, p="", d="", a=""):

        if self.player.playlist == [] or self.player.playlist == "":
            pass

        else:

            track = self.player.playlist[self.index]
            fpath, fname = os.path.split(track)

            name = self.acortando_title(fname)

            name_track = f"{name}          {self.Pocicion}|{self.Duracion}   {self.A}"
            self.track_label.setText(name_track)
            #self.track_label.setFixedWidth(25)
            self.track_label.setFixedHeight(15)

            self.btn_tm.setText(f"🕒 {self.Pocicion} | 🕒 {self.Duracion}   {self.A}")
            self.title_track.setText(f"{name}")

##=========================================================================================================
##=========================================================================================================

    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    def show_app_info(self):
        dialog_i = app_info(self)
        dialog_i.exec_()

    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    def key_app_info(self):
        dialog_k = key_info(self)
        dialog_k.exec_()

##-------------------------------------------------------------------------
    # =========================
    # 🎵 Centrar App
    # =========================
    def center_on_screen(self):

        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 1100, 650
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2 + 10
        self.setGeometry(x, y, w, h)

    # =========================
    # 🎵 Cargar El Logo, y Todas las Imagenes
    # =========================
    def load_imgs_slid(self):

        files  = []
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Imágenes", "", "All Files (*);;Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.ico *.webp)", options=options)
        
        if files:
            self.image_paths.extend(files)

        self.img_extra_slid()
##-------------------------------------------------------------------------
    # =========================
    # 🎵 Cargar Imagenes, Extra
    # =========================
    def img_extra_slid(self):
        self.load_logo_img(self.image_paths)

    # =========================
    # 🎵 Cargar El Logo, y Todas las Imagenes
    # =========================
    def load_images(self, image_list):

        if self.image_paths == []:
            self.load_logo_img(image_list)

        else:
            self.load_logo_img(self.image_paths)

    # =========================
    # ✨ Pausa el Imagenes en el Slider
    # =========================
    def paused_play_imgslid(self):
        print(self.SLIDE_PAUSED)

        if self.SLIDE_PAUSED == False:

            self.SLIDE_PAUSED = True
            self.timer.stop()

        elif self.SLIDE_PAUSED == True:

            self.SLIDE_PAUSED = False
            self.timer.start()

    # =========================
    # 🎵 Cargar El Logo, y Todas las Imagenes
    # =========================
    def load_logo_img(self, list_img):
        self.images = list_img
        if self.images:

            self.show_image(self.images[0])
            self.timer.start(30000)  # 1 minuto

    # =========================
    # ✨ Siguiente Imagen, entre las Imagenes Locales
    # =========================
    def next_image(self):
        if not self.images:
            return

        try:
            cont = len(self.images)
            self.current_image = random.randint(0, int(cont))  ## (start, istop+1)

            self.current_image = (self.current_image + 1) % len(self.images)
            self.fade_to_image(self.images[self.current_image])

        except Exception as e:
            print(f"Error en [next_image-L374|-|Exception: -L386]  {e}")

            self.current_image = 0
            self.next_image()

##-------------------------------------------------------------------------
    # =========================
    # ✨ Efecto, de Transición, entre Imagenes
    # =========================
    def fade_to_image(self, path):

        effect = QGraphicsOpacityEffect()
        self.logo_label.setGraphicsEffect(effect)

        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)

        self.show_image(path)
        self.anim.start()
##-------------------------------------------------------------------------
    # =========================
    # ✨ Cargan Todas las Imagenes
    # =========================
    def show_image(self, path):	    
	    pix = QPixmap(path)

	    if pix.isNull():
	        return

	    self.logo_label.setPixmap(pix.scaled(
	        self.logo_label.width(),
	        self.logo_label.height(),
	        Qt.KeepAspectRatio,
	        Qt.SmoothTransformation
	    ))
	    self.logo_label.setScaledContents(True)
##-------------------------------------------------------------------------
    # =========================
    # ✨ Abre y Cierra, el Panel Izquierdo
    # =========================
    def toggle_sidebar(self):
        self.sidebar_widget.setVisible(not self.sidebar_widget.isVisible())

        # 🔥 FORZAR RECÁLCULO
        self.centralWidget().updateGeometry()
        self.centralWidget().adjustSize()
##-------------------------------------------------------------------------
    # =========================
    # 🏠 HOME
    # =========================
    def build_home(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 🖼️ LOGO / SLIDER (EXPANDIBLE)
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Conectar el clic del label al método de reproducción
        self.logo_label.mousePressEvent = lambda e: AdvancedUI.play_audio(self)

	    # 🔥 CLAVE: que EXPANDA
        self.logo_label.setSizePolicy(
	        self.logo_label.sizePolicy().Expanding,
	        self.logo_label.sizePolicy().Expanding
	    )

        layout.addWidget(self.logo_label, 5)  # 👈 más peso

	    # 🎵 TRACK NAME (DEBAJO DEL LOGO)
        self.track_label = QLabel("Sin reproducción")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("font-size:18px;")
        self.track_label.setFixedHeight(15)

        layout.addWidget(self.track_label, 1)  # 👈 menos peso

	    # 🎛️ CONTROLES
        controls = QHBoxLayout()

        btn_prev = QPushButton("⏪")
        self.btn_play = QPushButton("▶")
        btn_stop = QPushButton("◼️")
        btn_next = QPushButton("⏩")
        btn_load = QPushButton("📂")

        btn_load.clicked.connect(self.load_folder)
        self.btn_play.clicked.connect(self.play_audio)
        btn_stop.clicked.connect(self.player.stop)
        btn_next.clicked.connect(self.next_track)
        btn_prev.clicked.connect(self.prev_track)

        controls.addWidget(btn_prev)
        controls.addWidget(self.btn_play)
        controls.addWidget(btn_stop)
        controls.addWidget(btn_next)
        controls.addWidget(btn_load)

        layout.addLayout(controls)

        w = QWidget()
        w.setLayout(layout)
        return w

    # =========================
    # 🎵 PLAY control´s
    # =========================
    def play_audio(self):

        if self.player.playlist == []:
            pass

        else:

            try:

                self.Actualizando_Title()
                self.paused_play_Gif()
                self.paused_play_imgslid()

                if self.pause_play == True:
                    self.pause_play = False
                    print(f"Ahora Suena:  {self.player.playlist[self.index]}")

                    self.player.play(self.index)
                    self.btn_play.setText("⏳")

                elif self.pause_play == False:
                    self.pause_play = True

                    self.player.play(self.index)
                    self.btn_play.setText("▶")

            except Exception as e:
                print(f"Error en: [play_audio-L496|-|Exception: -L530]  {e}")

                self.index = 0
                AdvancedUI.play_audio(self)

    # =========================
    # ✨ Track Anterior, en la PlayList
    # =========================
    def prev_track(self):

        if self.player.playlist == []:
            pass

        else:

            self.index -= 1
            self.Actualizando_Title()
            track = self.player.playlist[self.index]
            fpath, fname = os.path.split(track)
            print(f"Esto es Index-prev_track:  {fname}")

            if self.filename_gif == []:
                pass

            else:
                cont = len(self.filename_gif)
                self.index_gif = random.randint(0, int(cont))  ## (start, istop+1)

                path = self.filename_gif[self.index_gif]
                print(path)
                self.load_new_gif(path)

            try:

                i = self.aleatory_chec()
                if i == "X":
                    self.player.prev(self.index)
                else:
                    self.index = i
                    self.player.prev(self.index)

            except Exception as e:
                print(f"Error en: [prev_track-L538|-|Exception: -L565]  {e}")

                self.index = 0
                self.player.prev(self.index)

    # =========================
    # ✨ Siguiente Track, en la PlayList
    # =========================
    def next_track(self):

        if self.player.playlist == []:
            pass

        else:

            self.index += 1
            self.Actualizando_Title()
            track = self.player.playlist[self.index]
            fpath, fname = os.path.split(track)
            print(f"Esto es Index-next_track:  {fname}")

            if self.filename_gif == []:
                pass

            else:
                cont = len(self.filename_gif)
                self.index_gif = random.randint(0, int(cont))  ## (start, istop+1)

                path = self.filename_gif[self.index_gif]
                print(path)
                self.load_new_gif(path)

            try:

                i = self.aleatory_chec()
                if i == "X":
                    self.player.next(self.index)
                else:
                    self.index = i
                    self.player.next(self.index)

            except Exception as e:
                print(f"Error en: [next_track-L573|-|Exception: -L602]  {e}")

                self.index = 0
                self.player.next(self.index)

    # =========================
    # 🎵 Tracks Aleatorios
    # =========================
    def aleatory_chec(self):

        if self.aleatory_track == True:
            self.A = ""
            return "X"

        elif self.aleatory_track == False:

            self.A = "A"
            self.Actualizando_Title(a=f"{self.A}")

            cont = len(self.player.playlist)
            return random.randint(0, int(cont))

    # =========================
    # 🎵 Tracks Aleatorios
    # =========================
    def aleatory_track_list(self):

        if self.aleatory_track == True:
            print("Aleatorio Activado.")
            self.aleatory_track = False

        else:
            print("Aleatorio Desactivado.")            
            self.aleatory_track = True

    # =========================
    # 🎵 PLAYLIST
    # =========================
    def build_playlist(self):
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.clicked.connect(self.select_track)

        layout.addWidget(QLabel("🎵 Playlist"))
        layout.addWidget(self.list_widget)

        w = QWidget()
        w.setLayout(layout)
        return w

    # =========================
    # 🎵 Cargar Folder de Tracks
    # =========================
    def load_folder(self):
        folder = QFileDialog.getExistingDirectory(self)

        tracks = self.loader.load_folder(folder)
        self.load_tracks(tracks)
    
    # =========================
    # 🎵 Cargar a PLAYLIST los Tracks
    # =========================
    def load_tracks(self, tracks):

        for t in tracks:
        	self.list_widget.addItem(t["title"])
        	self.player.load(t["audio"])

    # =========================
    # 🎵 PLAYLIST Selecciona Track a Reproducir
    # =========================
    def select_track(self):

        self.name_track()

        self.player.index = self.list_widget.currentRow()
        self.player.play(self.index)

    # =========================
    # ✨ El Nombre de Cada Track, Dependiendo, del (currentRow())
    # =========================
    def name_track(self):

        self.index = self.list_widget.currentRow()
        self.player.index = self.index
        track = self.player.playlist[self.index]
        self.player.load(track)
        self.Actualizando_Title()
        #self.track_label.setFixedWidth(25)
        self.track_label.setFixedHeight(15)
        self.btn_play.setText("⏳")
        self.timer.start()

##-------------------------------------------------------------------------

## Carga La Carpeta donde se encuentran los 50 Gif´s Precargados en el Programa y los Enlista
## Para posteriormente hacer uso de esa lista y Visualizarlos de uno en uno, segun...
    def Load_New_GIF_LIST(self):

        try:

            self.filename_gif.clear()

            ## Forma 1 - para localizar la Carpeta ('GIFS'), dentro de la App. en el Dir Raiz
            bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath( os.path.dirname(__file__) ) )
            dir_gifs = os.path.join(bundle_dir, "assets\\gifs",)

            ## Forma 2 - para localizar la Carpeta ('GIFS'), dentro de la App. en el Dir Raiz
            # dir_gifs = os.path.join(os.path.dirname(__file__), 'GIFS')                        
                                                                            
            if not os.path.exists(dir_gifs):                                
                pass                                                        
            else:
                                                                            
                ima_copy = os.listdir(dir_gifs)
                for copy_ima in ima_copy:
                    if copy_ima.endswith(".gif"):                                   
                                                                            
                        full_file_name = os.path.join(copy_ima)                 
                        self.filename_gif.append(dir_gifs+'/'+full_file_name)

                    else:
                        continue

        except Exception as e:
            print(f"Error en [Load_New_GIF_LIST-L687|-|Exception: -L716]  {e}")

    # =========================
    # ✨ Buscamos, más, Gif´s, y Hasi, se Ignagura, la List Gif´s
    # =========================
    def open_gif(self):

        if self.player.playlist == []:
            pass
        else:

            try:

                new_gif, _ = QFileDialog.getOpenFileNames(self, "Open file", "/gui/desktop", "GIF files: (*.gif)")

                for plus_gif in new_gif:

                    self.filename_gif.append(plus_gif)

                path = self.filename_gif[self.index_gif]
                print(path)
                self.load_new_gif(path)

            except Exception as e:
                print(f"Error en: [open_gif-L721|-|Exception: -L740]  {e}")

                ##gif_animations.dialog_critical3(self, e)

    # =========================
    # ✨ Aviso si el MediaPlayer se Detuvo, para cambiar al Siguiente Gif
    # =========================
    def position(self, i):
        self.Pocicion = i
        self.Actualizando_Title(p=i)

    # =========================
    # ✨ Aviso si el MediaPlayer se Detuvo, para cambiar al Siguiente Gif
    # =========================
    def duration(self, i):
        self.Duracion = i
        self.Actualizando_Title(d=i)

    # =========================
    # ✨ Aviso si el MediaPlayer se Detuvo, para cambiar al Siguiente Gif
    # =========================
    def aviso(self, i):
        print(f"Esto es Aviso: ... Index {i}")

        if self.filename_gif == []:
            pass

        else:

            num = len(self.player.playlist)-1
            print(f"Cantidad de Track´s, en Lista:  {num}")

            if num == i:
                self.index = 0
                print(f"Esto es Index-{self.index} dentro de: Caso #1")
                self.res_aviso(self.index)

            else:
                print(f"Esto es Index-{self.index} dentro de: Caso #2")
                self.res_aviso(i)

    def res_aviso(self, i):
        print("Estoy en:  res_aviso")

        try:
            self.index = i
            self.Actualizando_Title()

            cont = len(self.filename_gif)
            self.index_gif = random.randint(0, int(cont))  ## (start, istop+1)

            path = self.filename_gif[self.index_gif]
            print(f"Siguiente Gif:  {path}")
            self.load_new_gif(path)

            track = self.player.playlist[self.index]
            self.player.load(track)
            self.player.play(self.index)

        except Exception as e:
            print(f"Error-Exception en: [res_aviso-L802|-|Exception: -L788] {e}")

            self.index_gif = 0
            path = self.filename_gif[self.index_gif]
            print(f"Siguiente Gif:  {path}")
            self.load_new_gif(path)

        except IndexError as e:
            print(f"Error-IndexError en: [res_aviso-L809|-|IndexError: -L778] {e}")

            self.index_gif = 0
            path = self.filename_gif[self.index_gif]
            print(f"Siguiente Gif:  {path}")
            self.load_new_gif(path)

    # =========================
    # 🎞️ GIF PANEL
    # =========================
    def build_gif_panel(self):

        self.gif_label = QLabel()
        self.gif_label.setScaledContents(True)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Conectar el clic del label al método de reproducción
        self.gif_label.mousePressEvent = lambda e: AdvancedUI.play_audio(self)

        if self.filename_gif == []:
            # 🔥 GIF (puedes cambiarlo)
            gif = Path.resource_path("assets/gifs/visual.gif")
            self.gif_path = f"{gif}"
            
            self.Load_New_GIF_LIST()

        else:
            self.gif_path = self.filename_gif[self.index_gif]
            self.index_gif += 1

        if os.path.exists(self.gif_path):
            self.movie = QMovie(self.gif_path)
            self.movie.setScaledSize(QtCore.QSize(self.size_1, self.size_2))
            self.gif_label.setMovie(self.movie)
            self.movie.start()

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        layout.addWidget(self.gif_label)
        layout.addWidget(self.title_track)
        btn_ctrl = QPushButton("⚙️ GIF Control")
        btn_ctrl.clicked.connect(self.show_gif_window)

        btn_siguiente = QPushButton("➕ Siguiente GIF")
        btn_siguiente.clicked.connect(self.siguiente_gif)

        btn_layout.addWidget(btn_ctrl)
        btn_layout.addWidget(self.btn_tm)
        btn_layout.addWidget(btn_siguiente)

        layout.addLayout(btn_layout)

        w = QWidget()
        w.setLayout(layout)
        return w

    def Ocultar_Desocultar(self):

        if self.des_ocult == True:
            self.des_ocult = False
            self.title_track.show()

        else:
            self.des_ocult = True
            self.title_track.hide()


    # =========================
    # ✨ Al Siguiente Gif
    # =========================
    def siguiente_gif(self):

        if self.player.playlist == []:
            pass
        else:

            if self.filename_gif == []:
                pass

            else:

                try:
                    cont = len(self.filename_gif)
                    self.index_gif = random.randint(0, int(cont))  ## (start, istop+1)

                    path = self.filename_gif[self.index_gif]
                    print(f"Siguiente Gif:  {path}")
                    self.load_new_gif(path)

                except Exception as e:
                    print(f"Error en: [siguiente_gif-L836|-|Exception: -L856]  {e}")

                    self.index_gif = 0
                    AdvancedUI.siguiente_gif(self)

    # =========================
    # ✨ ANIMACIÓN CAMBIO GIF´S
    # =========================
    def load_new_gif(self, path):
        if hasattr(self, "movie"):
            self.movie.stop()

        self.movie = QMovie(path)
        self.movie.setScaledSize(QtCore.QSize(self.size_1, self.size_2))
        self.gif_label.setMovie(self.movie)
        self.movie.start()

    # =========================
    # ✨ Pausa el Gif, en Reproducción del Momento
    # =========================
    def paused_play_Gif(self):

        if self.GIF_PAUSED == False:

            self.GIF_PAUSED = True
            self.movie.setPaused(self.GIF_PAUSED)

        elif self.GIF_PAUSED == True:

            self.GIF_PAUSED = False
            self.movie.setPaused(self.GIF_PAUSED)
##-------------------------------------------------------------------------
    # =========================
    # ✨ ANIMACIÓN CAMBIO PÁGINA
    # =========================
    def switch_page(self, index):
        self.animation = QPropertyAnimation(self.stack, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(1)
        self.animation.start()

        self.stack.setCurrentIndex(index)

    # =========================
    # 🎨 ESTILO PRO
    # =========================
    def apply_style(self):
        self.setStyleSheet("""
        QMainWindow { background:#121212; }

        QPushButton {
            background:#1f1f2e;
            color:white;
            padding:10px;
            border-radius:10px;
            font-size:14px;
        }

        QPushButton:hover {
            background:#00c3ff;
            color:black;
        }

        QListWidget {
            background:#1e1e2f;
            color:white;
            border-radius:10px;
        }

        QLabel {
            color:white;
            font-size:18px;
        }
        """)
##-------------------------------------------------------------------------
    def show_gif_window(self):
	    self.gif_window = GifControlWindow(self)
	    self.gif_window.show()
##-------------------------------------------------------------------------
    # =========================
    # ✨ Metodo para Subir y Vajar Volumen con el Scroll del Mouse
    # =========================
    def wheelEvent(self, event):

    	num = event.angleDelta().y()
    	print(num)

    	if num == 120:

    		if self.vol == 10.0 or self.vol == 10.00:
    			return None

    		else:
    			print(self.vol)
	    		self.vol = float(self.vol)
	    		self.vol += 0.1
	    		self.vol = f"{self.vol:.2f}"

    			self.vol = float(self.vol)
    			self.player.volumen(self.vol)

    	else:

    		if self.vol == 0.00 or self.vol == 0.0:
    			return None
    		else:
    			print(self.vol)
	    		self.vol = float(self.vol)
	    		self.vol -= 0.1
	    		self.vol = f"{self.vol:.2f}"

    			self.vol = float(self.vol)
    			self.player.volumen(self.vol)
##-------------------------------------------------------------------------
    # =========================
    # ✨ Cuarta Pestaña (VIDEO)
    # =========================
    def build_video_panel(self):
        ## Otra forma para el Color en el Tab
        # page = QWidget()

        # page.setStyleSheet("""
        #     QWidget {
        #         background-color: #e9eef3;
        #     }
        # """)

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setAlignment(Qt.AlignCenter)

        # botón abrir video
        self.video_open_button = QPushButton("Buscar y Abrir Video")
        self.video_open_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)

        self.video_open_button.clicked.connect(self.cuestion_choise)

        layout.addWidget(self.video_open_button)

        # contenedor del reproductor
        self.video_container = QVBoxLayout()
        layout.addLayout(self.video_container)

        return page

    def open_video_dialog(self):
        self.play_audio()
        self.player.stop()
        self.btn_play.setText("⏳")
        file_filter = []
        file_filter.clear()
        self.current_video_list = []
        self.current_video_list.clear()

        file_filter = "Archivos de Video (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm);;Todos los archivos (*.*)"

        file_path, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar un archivo de video",
            "",
            file_filter
        )

        if file_path:
            self.current_video_list = file_path

            # 🔥 actualizar tab 5
            self.page_video_list.current_video_list = self.current_video_list
            self.page_video_list.update_pages()

            self.show_video_player(file_path)

        else:
            self.video_open_button.show()

    def cuestion_choise(self):

        self.video_open_button.hide()
        self.show_info('Respuesta', 'Empesare con el Ingreso, de los medios que Sean Seleccionados.')

        # Crear un QMessageBox personalizado
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)
        msg_box.setWindowTitle('--> Pregunta? <--')

        # Establecer el icono personalizado
        self.Ico_wath = Path.resource_path('Ico\\wath.png')
        msg_box.setIconPixmap(QIcon(f'{self.Ico_wath}').pixmap(50, 50))

        # Establecer el texto del mensaje
        msg_box.setText('Deseas Buscar Videos de forma Normal? o Buscar por Directorio? o Ninguna?')

        # Añadir botones personalizados
        button_normal = msg_box.addButton('   Buscar Videos Normal?   ', QMessageBox.YesRole)
        button_Miniaturas = msg_box.addButton('   Buscar Videos por Directorio?   ', QMessageBox.YesRole)

        no_button = msg_box.addButton('  Ninguna Gracias  ', QMessageBox.NoRole)

        # Mostrar el mensaje y obtener la respuesta
        reply = msg_box.exec_()

        # Manejar la respuesta
        if msg_box.clickedButton() == button_normal:
            ##self.show_info('Respuesta', 'Has seleccionado:  Seleccion Normal.')

            try:

                self.open_video_dialog()
                self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            except Exception as e:
                print(e)

                self.video_open_button.show()

        elif msg_box.clickedButton() == button_Miniaturas:
            
            try:

                result = Search_MP4.on_browse_MP4(self)
                self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

                if result:
                    self.current_video_list = result

                    # 🔥 actualizar la Busqueda por Directorio
                    self.page_video_list.current_video_list = self.current_video_list
                    self.page_video_list.update_pages()

                    self.show_video_player(result)

            except Exception as e:
                print(e)

                self.video_open_button.show()

        elif msg_box.clickedButton() == no_button:
            self.show_info('Respuesta', 'No se Selecciono ningun Ingreso de Medios.\nVuelve a Intentarlo Despues.\nMuchas, Gracias.')
            self.video_open_button.show()

    def show_video_player(self, video_path):

        # limpiar reproductor anterior
        while self.video_container.count():
            item = self.video_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.video_player.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.video_player.setStyleSheet("""
            QPushButton{
                background-color: #ffffff;
                border-radius: 4px;
                padding: 3px;
            }

            QLabel{
                color: black;
                background-color: #e8e8e8;
            }
        """)

        # conectar señal de cierre
        self.video_player.request_close.connect(self.close_video_player)

        # cargar video
        self.video_player.open_file(video_path)
        self.video_container.addWidget(self.video_player)

    def close_video_player(self, widget):

        self.video_player.stop()
        widget.setParent(None)

        self.video_open_button.show()
        ##widget.deleteLater()  ## <--- Destruye, y Rompe todo
##-------------------------------------------------------------------------
    # =========================
    # ✨ Metodo para Obtener Cualquier Tecla Pulsada dentro de la App.
    # =========================
    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape: ## Key Board (Teclado - Tecla Escape (ESC))
            self.movie.stop()       ## Stop Rep.
            sys.exit()              ## Exit (Clouse App) Cerrar la Aplicación

        elif event.key() == 79:     ## O
            self.load_imgs_slid()   ## Ingresar Images (Files)

    def show_info(self, titulo, texto):
        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)
        msg.setText(texto)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
            }
        """)

        msg.exec_()

##=========================================================================================================
##=========================================================================================================

class Search_MP4():

    def __init__(self):
        super().__init__()

    def on_browse_MP4(self, e=None):
        """Callback for directory browse"""

        dialog = QFileDialog()
        self.path = dialog.getExistingDirectory(self, 'Slecciona el Directorio')

        if self.path:
            # Path to the root directory
            root_dir = self.path

            resultados = []

            VIDEO_EXT = {
                ".mp4", ".mkv", ".avi", ".mov", ".wmv",
                ".flv", ".webm", ".mpg", ".mpeg"
            }

            for dirpath, _, filenames in os.walk(root_dir):
                for file in filenames:
                    ext = os.path.splitext(file)[1].lower()

                    if ext in VIDEO_EXT:
                        full_path = os.path.join(dirpath, file)
                        resultados.append(full_path)

            #QMessageBox.information(self, 'Info', 'He Conlcuido con la Tarea Asignada\nMuchas Gracias...')
            self.show_info('Info', 'Estoy por Concluir con la Tarea Asignada.\nFabor de Darme Tiempo.\nMuchas Gracias...')
            return resultados

        else:

            self.video_open_button.show()

##=========================================================================================================
##=========================================================================================================

class New_Win2(QWidget):
    def __init__(self, current_video_list, video_player, parent=None):
        super().__init__(parent)
        self.video_player = video_player  # Guardar una referencia a la instancia de AdvancedUI
        self.current_video_list = current_video_list
        self.pages = []
        self.page_widge = []
        self.sb = 0

        self.initUI()
        ##=================================================================================================
        ##=================================================================================================

    def initUI(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Layout para mostrar las páginas
        self.page_layout = QVBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)

        self.page_widget = QStackedWidget()
        self.page_widget.setStyleSheet('background-color: #d1d1d1;')
        self.page_layout.addWidget(self.page_widget)
        main_layout.addLayout(self.page_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.page_widget)
        main_layout.addWidget(scroll)

        # 🔥 BOTONES DE NAVEGACIÓN
        nav_layout = QHBoxLayout()

        self.home_button = QPushButton("🏠 Home")
        self.prev_button = QPushButton("⏪ Anterior")
        self.next_button = QPushButton("⏩ Siguiente")

        self.home_button.clicked.connect(self.go_to_home)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        ##=================================================================================================
        ##=================================================================================================

    def update_pages(self):

        # 🔥 LIMPIAR
        while self.page_widget.count():
            widget = self.page_widget.widget(0)
            self.page_widget.removeWidget(widget)
            widget.deleteLater()

        self.pages.clear()

        # Crear nuevas páginas
        num_pages = (len(self.current_video_list) + 49) // 50  # Redondear hacia arriba
        for i in range(num_pages):

            page = QWidget()
            page_layout = QVBoxLayout()

            for row in range(5):

                row_layout = QHBoxLayout()

                for col in range(10):

                    index = i * 50 + row * 10 + col

                    if index < len(self.current_video_list):

                        video_path = self.current_video_list[index]
                        # Extraer el frame específico del video
                        cap = cv2.VideoCapture(video_path)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 10)  # Ir al frame 10
                        ret, frame = cap.read()
                        cap.release()

                        if ret:

                            # Convertir el frame a QImage y luego a QPixmap
                            height, width, channel = frame.shape
                            bytes_per_line = 3 * width
                            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                            ## pixmap = QPixmap.fromImage(q_img).scaled(70, 160, Qt.KeepAspectRatio)
                            pixmap = QPixmap.fromImage(q_img).scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                            # Crear un label con la miniatura
                            label = QLabel(self)
                            label.setPixmap(pixmap)
                            label.setScaledContents(True)
                            label.setAlignment(Qt.AlignCenter)

                            # Añadir el nombre del video o un número
                            video_name = New_Win2.get_video_name(self, video_path)
                            name_label = QLabel(video_name, self)
                            name_label.setFont(QFont('Arial', 6))
                            name_label.setAlignment(Qt.AlignCenter)

                            # Conectar el clic del label al método de reproducción
                            label.mousePressEvent = lambda event, vp=video_path: New_Win2.play_video(self, vp)

                            # Añadir el label de la miniatura y el nombre del video al layout
                            layout = QVBoxLayout()
                            layout.addWidget(label)
                            layout.addWidget(name_label)
                            row_layout.addLayout(layout)

                page_layout.addLayout(row_layout)

            page.setLayout(page_layout)
            self.pages.append(page)
            self.page_widget.addWidget(page)

        # Ajustar botones de navegación
        self.home_button.setEnabled(num_pages > 1)
        self.prev_button.setEnabled(num_pages > 1)
        self.next_button.setEnabled(num_pages > 1)

        # Ir a la primera página
        self.current_page = 0
        self.page_widget.setCurrentIndex(self.current_page)

    def get_video_name(self, video_path):

        base_name = os.path.basename(video_path)
        name, _ = os.path.splitext(base_name)
        # Limitar el nombre a 25 caracteres
        return name[:25]

    def go_to_home(self):

        self.current_page = 0
        self.page_widget.setCurrentIndex(self.current_page)

    def prev_page(self):

        try:

            if self.current_page > 0:
                self.current_page -= 1
                self.page_widget.setCurrentIndex(self.current_page)

        except Exception as e:
            print(e)

    def next_page(self):

        try:

            if self.current_page < len(self.pages) - 1:
                self.current_page += 1
                self.page_widget.setCurrentIndex(self.current_page)

        except Exception as e:
            print(e)

    def play_video(self, video_path):

        # crear reproductor
        self.video_player.load(video_path)

##---------------------------------------------------------------------------------------------
## --> Información del Software
##---------------------------------------------------------------------------------------------
class app_info(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Acerca de PRO PLAYER X_v2")
        self.setFixedSize(540, 430)

        self.setWindowFlags(
            Qt.Dialog |
            Qt.WindowCloseButtonHint
        )

        self.setModal(True)

        self.init_ui()
        self.apply_style()


    # =========================
    # UI
    # =========================
    def init_ui(self):

        layout = QVBoxLayout(self)

        # 🎧 Título
        title = QLabel("🎧 PRO PLAYER X_v2")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Información del Software")
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)


        # 📜 Texto informativo
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)

        self.info_text.setText(
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎧 PRO PLAYER X_v2
Versión: v2.0

Desarrollado por:
Cristian M. Veliz Cano

Descripción:

PRO PLAYER X_v2 es un reproductor multimedia moderno desarrollado
en Python con PyQt5, diseñado para ofrecer una experiencia
visual atractiva y funcional.

El sistema permite reproducir audio mediante listas dinámicas,
carga de archivos locales y reproducción desde URLs.

Características actuales:

✔ Reproducción de audio (MP3 y compatibles)
✔ Reproducción de Videos (MP4 y compatibles)
✔ Panel con Miniaturas de Video (MP4 y compatibles)
✔ Playlist interactiva
✔ Interfaz moderna con PyQt5
✔ Slider automático de imágenes
✔ Visualizador mediante GIFs
✔ Control de GIFs dinámicos
✔ Navegación por páginas
✔ Sidebar interactivo (Ctrl + P)

Características en desarrollo:

🔧 Visualizador de audio real
🔧 Equalizador de sonido
🔧 Metadata (artista / álbum / portada)
🔧 Mini reproductor flotante
🔧 Drag & Drop
🔧 Base de datos local

Tecnología:

• Python 3
• PyQt5
• Arquitectura modular

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Atajo del teclado:
Ctrl + I  → Abrir esta ventana
Ctrl + k  → Abrir ventana teclas de Atajo
"""
        )

        layout.addWidget(self.info_text)


        # 🔘 Botón
        btn_layout = QHBoxLayout()

        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(36)

        close_btn.clicked.connect(self.close)

        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)


    # =========================
    # Estilo
    # =========================
    def apply_style(self):

        self.setStyleSheet("""

        QDialog {
            background:#121212;
        }

        QLabel {
            color:white;
        }

        QLabel:first {
            font-size:20px;
            font-weight:bold;
            color:#00c3ff;
        }

        QTextEdit {
            background:#1e1e2f;
            color:#f1f1f1;
            border-radius:8px;
            padding:10px;
            font-size:11pt;
        }

        QPushButton {
            background:#1f1f2e;
            color:white;
            border-radius:10px;
            padding:8px;
            font-size:14px;
        }

        QPushButton:hover {
            background:#00c3ff;
            color:black;
        }

        """)

##---------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------
class key_info(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #-> Forma Uno (1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        #-> Forma Dos (2)
        #self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Atajo de Teclas")
        self.setFixedSize(520, 420)
        self.setModal(True)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- Título ---
        title = QLabel("Atajo de Teclas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00A3FF;
            }
        """)
        layout.addWidget(title)

        # --- Texto informativo ---
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText("""
Atajo con Combinación de Teclas:
Con:  -  [CTRL+I]  -  Información del Reproductor.
Con:  -  [CTRL+K]  -  Información del Atajo de Teclas.
Con:  -  [CTRL+P]  -  Ocultar || Desocultar panel Izquierdo.
Con:  -  [CTRL+G]  -  Agregamos más Gif´s, al List-Gif.
Con:  -  [CTRL+F]  -  Regresamos 1 Track Anterior.
Con:  -  [CTRL+N]  -  Adelantamos 1 Track Anterior.
Con:  -  [CTRL+A]  -  Activamos, el Modo Aleatorio.
Con:  -  [Key:  ESC]  -  Cerramos el Soft.
Con:  -  [Key:  O]  -  Agregamos más Imagenes, al List-Slide.

            """)

        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #F1F1F1;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 8px;
                font-size: 10.5pt;
            }
        """)
        layout.addWidget(info_text)

        # --- Botón cerrar ---
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        layout.addWidget(close_button)
##---------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------
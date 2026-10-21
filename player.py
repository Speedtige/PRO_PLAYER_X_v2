
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-01
Nombre del Soft: 🎧 PRO PLAYER X
Distribución: Gratuito  -->OPENSOURCE<--
'''

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QObject, pyqtSignal

class AudioPlayer(QObject):

    track_changed = pyqtSignal(int)

    positionChanged = pyqtSignal(str)

    durationChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()

        self.playlist = []
        self.index = 0

        self.pause = True
        self.name_track = ""

        # detectar cambios de estado
        self.player.mediaStatusChanged.connect(self.handle_status)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    # -----------------------------
    #   Utilidad formato de tiempo
    # -----------------------------
    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def position_changed(self, position):
        position = self.format_time(position)
        self.positionChanged.emit(position)  # 🔥 AVISO AL MAIN

    def duration_changed(self, duration):
        duration = self.format_time(duration)
        self.durationChanged.emit(duration)  # 🔥 AVISO AL MAIN

    def load(self, source):
        self.playlist.append(source)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(source)))

    def play(self, i):
        print(f"Esto es: [play|player] - Index {i}")

        if self.playlist:
            self.index = i

            try:

                if self.player.state() == QMediaPlayer.PlayingState:
                    self.player.pause()

                else:
                    self.player.play()

            except Exception as e:
                print(f"Error-IndexError en: [play-L37|-|IndexError: -L52] {e}")

    def pause(self):
        if self.playlist:
            self.player.pause()

    def stop(self):
        if self.playlist:
            self.player.stop()

    def next(self, i):
        print(f"Esto es Index|Player-next:  {i}")
        if self.playlist:
            self.index = i
            self.load(self.playlist[self.index])
            self.play(self.index)

    def prev(self, i):
        print(f"Esto es Index|Player-prev:  {i}")
        if self.playlist:
            self.index = i
            self.load(self.playlist[self.index])
            self.play(self.index)

    def volumen(self, vol):
        if self.playlist:
            self.player.setVolume(vol)

    def handle_status(self, status):

        try:
            if status == QMediaPlayer.EndOfMedia:
                print(f"Esto es handle_status|Player")

                self.index += 1
                self.track_changed.emit(self.index)  # 🔥 AVISO AL MAIN
                self.next(self.index)

        except Exception as e:
            print(f"Error-IndexError en: [handle_status|Player-L80|-|IndexError: -L91] {e}")

            if status == QMediaPlayer.EndOfMedia:

                self.index = 0
                self.track_changed.emit(0)  # 🔥 AVISO AL MAIN
                self.play(self.index)
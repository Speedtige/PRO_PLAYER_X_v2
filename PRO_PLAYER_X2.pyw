
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎧 PRO PLAYER X
Versión: v1.0
play
Desarrollado por:
Cristian M. Veliz Cano

Descripción:
PRO PLAYER X es un reproductor multimedia moderno desarrollado en Python con PyQt5,
enfocado en ofrecer una experiencia visual atractiva y funcional.

El sistema permite la reproducción de audio mediante listas dinámicas, carga de archivos
locales y reproducción desde URLs (cloud). Incluye una interfaz avanzada con animaciones,
transiciones suaves y un sistema modular preparado para futuras expansiones.

Características actuales:
✔ Reproducción de audio (MP3 y compatibles)
✔ Reproducción de Videos (MP4 y compatibles)
✔ Panel con Miniaturas de Video (MP4 y compatibles)
✔ Carga de archivos locales
✔ Soporte para URLs remotas (streaming básico)
✔ Playlist interactiva
✔ Interfaz moderna con PyQt5
✔ Slider automático de imágenes (logo dinámico)
✔ Transiciones con animaciones (fade)
✔ Panel de visualización con GIFs dinámicos
✔ Control de GIFs en ventana emergente
✔ Sidebar interactivo (ocultable con Ctrl + P)
✔ Navegación por páginas (QStackedWidget)

Características en desarrollo:
🔧 Visualizador de audio real (no GIF)
🔧 Equalizador de sonido
🔧 Lectura de metadata (artista, álbum, portada)
🔧 Mini reproductor flotante
🔧 Drag & Drop (arrastrar y soltar archivos)
🔧 Persistencia de datos (base de datos local)

Tecnología utilizada:
• Python 3.x
• PyQt5 (sin diseñador visual)
• Arquitectura modular (player / loader / UI)

Licencia:
Uso libre para fines educativos y desarrollo personal.

Notas:
Este proyecto forma parte de una evolución progresiva por fases, orientado a alcanzar
un nivel profesional comparable con reproductores reales.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
##=========================================================================================
import sys
from PyQt5.QtWidgets import QApplication
from advanced_ui import AdvancedUI
##=========================================================================================

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = AdvancedUI()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

##=========================================================================================
if __name__ == "__main__":
    App().run()
##=========================================================================================

# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-01
Nombre del Soft: 🎧 PRO PLAYER X
Distribución: Gratuito  -->OPENSOURCE<--
'''

import os

class FileLoader:
    EXT = (".mp4", ".mp3", ".wav", ".ogg")

    def load_folder(self, folder):
        tracks = []
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith(self.EXT):
                    tracks.append({
                        "title": f,
                        "audio": os.path.join(root, f)
                    })
        return tracks
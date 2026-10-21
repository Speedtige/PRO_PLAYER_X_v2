
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Desarrollado Por: Cristian M. Veliz Cano
Verción del Soft: V-01
Nombre del Soft: 🎧 PRO PLAYER X
Distribución: Gratuito  -->OPENSOURCE<--
'''

import os, sys

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

        
i0 = Path.resource_path("assets/logo/logo0.png")
i01 = Path.resource_path("assets/img_slade/M (51).jpg")
i02 = Path.resource_path("assets/img_slade/M (52).jpg")
i03 = Path.resource_path("assets/img_slade/M (53).jpg")

i1 = Path.resource_path("assets/img_slade/M (1).jpg")
i2 = Path.resource_path("assets/img_slade/M (2).jpg")
i3 = Path.resource_path("assets/img_slade/M (3).jpg")
i4 = Path.resource_path("assets/img_slade/M (4).jpg")
i5 = Path.resource_path("assets/img_slade/M (5).jpg")
i6 = Path.resource_path("assets/img_slade/M (6).jpg")
i7 = Path.resource_path("assets/img_slade/M (7).jpg")
i8 = Path.resource_path("assets/img_slade/M (8).jpg")
i9 = Path.resource_path("assets/img_slade/M (9).jpg")
i10 = Path.resource_path("assets/img_slade/M (10).jpg")

i11 = Path.resource_path("assets/img_slade/M (11).jpg")
i12 = Path.resource_path("assets/img_slade/M (12).jpg")
i13 = Path.resource_path("assets/img_slade/M (13).jpg")
i14 = Path.resource_path("assets/img_slade/M (14).jpg")
i15 = Path.resource_path("assets/img_slade/M (15).jpg")
i16 = Path.resource_path("assets/img_slade/M (16).jpg")
i17 = Path.resource_path("assets/img_slade/M (17).jpg")
i18 = Path.resource_path("assets/img_slade/M (18).jpg")
i19 = Path.resource_path("assets/img_slade/M (19).jpg")
i20= Path.resource_path("assets/img_slade/M (20).jpg")

i21 = Path.resource_path("assets/img_slade/M (21).jpg")
i22 = Path.resource_path("assets/img_slade/M (22).jpg")
i23 = Path.resource_path("assets/img_slade/M (23).jpg")
i24 = Path.resource_path("assets/img_slade/M (24).jpg")
i25 = Path.resource_path("assets/img_slade/M (25).jpg")
i26 = Path.resource_path("assets/img_slade/M (26).jpg")
i27 = Path.resource_path("assets/img_slade/M (27).jpg")
i28 = Path.resource_path("assets/img_slade/M (28).jpg")
i29 = Path.resource_path("assets/img_slade/M (29).jpg")
i30= Path.resource_path("assets/img_slade/M (30).jpg")

i31 = Path.resource_path("assets/img_slade/M (31).jpg")
i32 = Path.resource_path("assets/img_slade/M (32).jpg")
i33 = Path.resource_path("assets/img_slade/M (33).jpg")
i34 = Path.resource_path("assets/img_slade/M (34).jpg")
i35 = Path.resource_path("assets/img_slade/M (35).jpg")
i36 = Path.resource_path("assets/img_slade/M (36).jpg")
i37 = Path.resource_path("assets/img_slade/M (37).jpg")
i38 = Path.resource_path("assets/img_slade/M (38).jpg")
i39 = Path.resource_path("assets/img_slade/M (39).jpg")
i40= Path.resource_path("assets/img_slade/M (40).jpg")

i41 = Path.resource_path("assets/img_slade/M (41).jpg")
i42 = Path.resource_path("assets/img_slade/M (42).jpg")
i43 = Path.resource_path("assets/img_slade/M (43).jpg")
i44 = Path.resource_path("assets/img_slade/M (44).jpg")
i45 = Path.resource_path("assets/img_slade/M (45).jpg")
i46 = Path.resource_path("assets/img_slade/M (46).jpg")
i47 = Path.resource_path("assets/img_slade/M (47).jpg")
i48 = Path.resource_path("assets/img_slade/M (48).jpg")
i49 = Path.resource_path("assets/img_slade/M (49).jpg")
i50= Path.resource_path("assets/img_slade/M (50).jpg")

load_images = [
	f"{i0}", f"{i01}", f"{i02}", f"{i03}",
    f"{i1}", f"{i11}", f"{i21}", f"{i31}", f"{i41}", 
    f"{i2}", f"{i12}", f"{i22}", f"{i32}", f"{i42}", 
    f"{i3}", f"{i13}", f"{i23}", f"{i33}", f"{i43}", 
    f"{i4}", f"{i14}", f"{i24}", f"{i34}", f"{i44}", 
    f"{i5}", f"{i15}", f"{i25}", f"{i35}", f"{i45}", 
    f"{i6}", f"{i16}", f"{i26}", f"{i36}", f"{i46}", 
    f"{i7}", f"{i17}", f"{i27}", f"{i37}", f"{i47}", 
    f"{i8}", f"{i18}", f"{i28}", f"{i38}", f"{i48}", 
    f"{i9}", f"{i19}", f"{i29}", f"{i39}", f"{i49}", 
    f"{i10}", f"{i20}", f"{i30}", f"{i40}", f"{i50}"
    ]
def set_button_style(btn, color):
    if color == 'blue':
        btn.setStyleSheet("QPushButton{color:white; background-color: rgb(86, 162, 238); border:2px groove grey;"
                          "border-radius:10px;padding:2px 4px;border-style: outset;}"
                          "QPushButton:hover{background-color:rgb(62, 153, 249)}"
                          "QPushButton:pressed{background-color:rgb(86, 162, 238);border-style: inset;}"
                          "QPushButton:disabled{background-color:rgb(172, 200, 230)}")
    else:
        btn.setStyleSheet("QPushButton{background-color: white;border:2px groove gray;"
                          "border-radius:10px;padding:2px 4px;border-style: outset;}"
                          "QPushButton:hover{background-color:rgb(229, 241, 251)}"
                          "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}"
                          "QPushButton:disabled{background-color:rgb(242, 240, 242)};border-style: inset")

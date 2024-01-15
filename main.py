from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, QStatusBar
from PyQt5 import uic
import sys
import os
import soundfile as sf
import numpy as np

from embed import DSSS_embed
from extract import DSSS_extract


# modes
EMBED = 1
EXTRACT = 2

class UI(QMainWindow):
    def __init__ (self):
        super().__init__()
        

        # load the ui file
        uic.loadUi("gui.ui", self)

        # define widgets to use
        # embedding widgets
        self.embed_open_file_btn = self.findChild(QPushButton, "embed_openFile_btn")
        self.encode_btn = self.findChild(QPushButton, "encode_btn")
        self.embed_file_path_label = self.findChild(QLabel, "embed_fp_label")
        self.key_label = self.findChild(QLabel, "key_label")
        self.embed_password_input = self.findChild(QLineEdit, "embed_password_lineEdit")
        self.message_input = self.findChild(QTextEdit, "message_In_textEdit")
        self.maxchar_label = self.findChild(QLabel, "maxchar_label")

        # extracting widgets
        self.extract_open_file_btn = self.findChild(QPushButton, "extract_openFile_btn")
        self.decode_btn = self.findChild(QPushButton, "decode_btn")
        self.extract_file_path_label = self.findChild(QLabel, "extract_fp_label")
        self.extract_password_input = self.findChild(QLineEdit, "extract_password_lineEdit")
        self.key_input = self.findChild(QLineEdit, "key_lineEdit")
        self.message_output = self.findChild(QTextEdit, "message_Out_textEdit")

        self.embed_password_input.setEchoMode(QLineEdit.Password)
        self.extract_password_input.setEchoMode(QLineEdit.Password)

        # embed variables
        self.audio_file = ""
        self.enc_password = ""
        self.message = ""
        self.char_limit_nopass = 1000   # character limit if no password used
        self.char_limit_pass = 1000     # character limit if password is used
        self.char_limit = 1000          # current character limit
        self.encode_flag = False

        # extract variables
        self.stego_file = ""
        self.dec_password = ""
        self.key = ""

        # click open file button
        self.embed_open_file_btn.clicked.connect(lambda: self.open_file(EMBED))
        self.extract_open_file_btn.clicked.connect(lambda: self.open_file(EXTRACT))

        # click encode/decode button
        self.encode_btn.clicked.connect(self.encode)
        self.decode_btn.clicked.connect(self.decode)

        # password field is edited
        self.embed_password_input.textChanged.connect(lambda: self.password_edit(EMBED))
        self.extract_password_input.textChanged.connect(lambda: self.password_edit(EXTRACT))

        # key field edited
        self.key_input.textChanged.connect(self.key_edit)

        # message field is edited
        self.message_input.textChanged.connect(self.message_edit)
    
        # show app
        self.show()

    def open_file(self, mode):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Audio File", "./", "WAV Files (*.wav)")
        if file_path:
            file_name = os.path.basename(file_path)
            if mode == EMBED:
                self.embed_file_path_label.setText(f'<span style=\" text-decoration: underline;\">{file_name}</span>')
                self.audio_file = file_path

                ### check character limit for the audio
                data, _ = sf.read(self.audio_file)
                # if multi-channel, use channel 1
                if data.ndim > 1:
                    data = data[:, 0]
                data_length = len(data)
                max_segments = data_length//1024
                n = max_segments - (max_segments%8)
                num_bytes = n//8
                self.char_limit_pass = num_bytes - (num_bytes%16)
                self.char_limit_nopass = num_bytes
                if self.enc_password:
                    self.char_limit = self.char_limit_pass
                else:
                    self.char_limit = self.char_limit_nopass
                self.maxchar_label.setText(str(self.char_limit))

                if len(self.message) > self.char_limit:
                    self.statusbar.showMessage("Warning: Exceeding character limit")
                else:
                    self.statusbar.showMessage("")
                
            elif mode == EXTRACT:
                self.extract_file_path_label.setText(f'<span style=\" text-decoration: underline;\">{file_name}</span>')
                self.stego_file = file_path
    
    def password_edit(self, mode):
        if mode == EMBED:
            self.enc_password = self.embed_password_input.text()
            
            if self.enc_password:
                self.char_limit = self.char_limit_pass
            else:
                self.char_limit = self.char_limit_nopass
            self.maxchar_label.setText(str(self.char_limit))
            if len(self.message) > self.char_limit:
                self.statusbar.showMessage("Warning: Exceeding character limit")
            else:
                self.statusbar.showMessage("")
            
        elif mode == EXTRACT:
            self.dec_password = self.extract_password_input.text()
        
    def message_edit(self):
        self.message = self.message_input.document().toPlainText()
        if len(self.message) > self.char_limit:
            self.statusbar.showMessage("Warning: Exceeding character limit")
        else:
            self.statusbar.showMessage("")

    def key_edit(self):
        self.key = self.key_input.text()

    def encode(self):
        if not self.message:
            # if message box is empty
            self.statusbar.showMessage("Error: message box is empty")
            return
        if not self.audio_file:
            # no audio file selected
            self.statusbar.showMessage("Error: select an audio file (.wav)")
            return
        
        if len(self.message) > self.char_limit:
            # max characters exceeded
            self.statusbar.showMessage("Error: Max number of characters exceeded")
            return
        key = DSSS_embed(self.audio_file, self.message, self.enc_password)
        self.key_label.setText(str(key))
        self.statusbar.showMessage("Embedding done! Destination: ./audio/stego_audio.wav")

    def decode(self):
        if not self.key:
            # if key is empty
            self.statusbar.showMessage("Error: input key")
            return
        if not self.stego_file:
            # no stego file selected
            self.statusbar.showMessage("Error: select an audio file (.wav)")
            return
        
        message = DSSS_extract(self.stego_file, self.dec_password, int(self.key))
        self.message_output.setPlainText(message)
        self.statusbar.showMessage("Extraction done! Destination: ./extracted_message.txt")

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
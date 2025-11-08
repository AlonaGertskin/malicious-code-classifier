import PyQt5.QtWidgets
import sys
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
import os
import ctypes


fileTypes = ['.txt','.exe','.php','.pl','.7z','.rar','.m4a','.wma','.avi','.wmv','.csv','.d3dbsp','.sc2save','.sie','.sum','.ibank','.t13','.t12','.qdf','.gdb','.tax','.pkpass','.bc6','.bc7','.bkp','.qic','.bkf','.sidn','.sidd','.mddata','.itl','.itdb','.icxs','.hvpl','.hplg','.hkdb','.mdbackup','.syncdb','.gho','.cas','.svg','.map','.wmo','.itm','.sb','.fos','.mcgame','.vdf','.ztmp','.sis','.sid','.ncf','.menu','.layout','.dmp','.blob','.esm','.001','.vtf','.dazip','.fpk','.mlx','.kf','.iwd','.vpk','.tor','.psk','.rim','.w3x','.fsh','.ntl','.arch00','.lvl','.snx','.cfr','.ff','.vpp_pc','.lrf','.m2','.mcmeta','.vfs0','.mpqge','.kdb','.db0','.mp3','.upx','.rofl','.hkx','.bar','.upk','.das','.iwi','.litemod','.asset','.forge','.ltx','.bsa','.apk','.re4','.sav','.lbf','.slm','.bik','.epk','.rgss3a','.pak','.big','.unity3d','.wotreplay','.xxx','.desc','.py','.m3u','.flv','.js','.css','.rb','.png','.jpeg','.p7c','.p7b','.p12','.pfx','.pem','.crt','.cer','.der','.x3f','.srw','.pef','.ptx','.r3d','.rw2','.rwl','.raw','.raf','.orf','.nrw','.mrwref','.mef','.erf','.kdc','.dcr','.cr2','.crw','.bay','.sr2','.srf','.arw','.3fr','.dng','.jpeg','.jpg','.cdr','.indd','.ai','.eps','.pdf','.pdd','.psd','.dbfv','.mdf','.wb2','.rtf','.wpd','.dxg','.xf','.dwg','.pst','.accdb','.mdb','.pptm','.pptx','.ppt','.xlk','.xlsb','.xlsm','.xlsx','.xls','.wps','.docm','.docx','.doc','.odb','.odc','.odm','.odp','.ods','.odt','.sql','.zip','.tar','.tar.gz','.tgz','.biz','.ocx','.html','.htm','.3gp','.srt','.cpp','.mid','.mkv','.mov','.asf','.mpeg','.vob','.mpg','.fla','.swf','.wav','.qcow2','.vdi','.vmdk','.vmx','.gpg','.aes','.ARC','.PAQ','.tar.bz2','.tbk','.bak','.djv','.djvu','.bmp','.cgm','.tif','.tiff','.NEF','.cmd','.class','.jar','.java','.asp','.brd','.sch','.dch','.dip','.vbs','.asm','.pas','.ldf','.ibd','.MYI','.MYD','.frm','.dbf','.SQLITEDB','.SQLITE3','.asc','.lay6','.lay','.ms11(Securitycopy)','.sldm','.sldx','.ppsm','.ppsx','.ppam','.docb','.mml','.sxm','.otg','.slk','.xlw','.xlt','.xlm','.xlc','.dif','.stc','.sxc','.ots','.ods','.hwp','.dotm','.dotx','.docm','.DOT','.max','.xml','.uot','.stw','.sxw','.ott','.csr','.key','wallet.dat']



class xDecrypter(PyQt5.QtCore.QRunnable):
    def __init__(self, key,filepath):
        super(xDecrypter, self).__init__()
        self.filePath = filepath
        self.threadpool = PyQt5.QtCore.QThreadPool()
        self.key = key
        self.crypto = AES.new(self.key.encode(), AES.MODE_ECB)

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        for root, directories, files in os.walk(self.filePath):
            for filename in files:
                filepath = os.path.join(root, filename)
                for base in fileTypes:
                    if base in filepath:
                        try:
                            self.decryptFile(filepath)
                            print(f"[+] - Decrypting File: {filename}") 
                        except:
                            pass
            ctypes.windll.user32.MessageBoxW(0, f"All Finished", "Success", 0x0 | 0x40)
    def decryptFile(self, file):
        with open(file, 'rb') as infile:
            content = self.crypto.decrypt((infile.read()))
            with open(file, "wb") as outfile:
                outfile.write(content)
                outfile.close()



class Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.threadpool = PyQt5.QtCore.QThreadPool()
        self.setFixedSize(500,250)
        self.setStyleSheet("background-color: #212121;")
        self.setWindowIcon(PyQt5.QtGui.QIcon('assets\\scrypt.ico')) 
        self.setWindowTitle("ScryptDecrypter")
        self.folderPath = PyQt5.QtWidgets.QLineEdit(self)
        self.key = PyQt5.QtWidgets.QLineEdit(self)
        self.decryptButton = PyQt5.QtWidgets.QPushButton('Decrypt', self)
        self.button = PyQt5.QtWidgets.QPushButton('Folder', self)
        self.startDecrypter()

        self.decryptionKey()
        self.pickFolderPath()
        self.locateFile()
        self.show()


    def startDecrypter(self):
        self.decryptButton.resize(475, 40)
        self.decryptButton.move(15, 150)
        self.decryptButton.setStyleSheet("""
                        QPushButton{
                            background-color: #7200ca;
                            border-radius: 15px;
                        }
                        QPushButton::hover {
                            background-color: #aa00ff;
                        }
                         """)
                        
        self.decryptButton.clicked.connect(self.decrypt)
        self.show()


    def decryptionKey(self):
        self.key.resize(475, 30)
        self.key.move(10, 50)
        self.key.setText("ENTER YOUR DECRYPTION KEY HERE")
        self.key.setStyleSheet("""
                        QLineEdit{
                            background-color: #484848;
                            color: #e254ff;
                            border-radius: 7.5px;
                            border-style: hidden;
                        }
            """)
        self.show()

    def pickFolderPath(self):
        self.folderPath.setReadOnly(True)
        self.folderPath.resize(400, 30)
        self.folderPath.move(85, 100)
        self.folderPath.setStyleSheet("""
                        QLineEdit{
                            background-color: #484848;
                            color: #e254ff;
                            border-radius: 7.5px;
                            border-style: hidden;
                        }
            """)
        self.show()

    def locateFile(self):
        self.button.resize(60, 30)
        self.button.move(10,100)
        self.button.setStyleSheet("""
                        QPushButton{
                            background-color: #7200ca;
                            border-radius: 7.5px;
                        }
                        QPushButton::hover {
                            background-color: #aa00ff;
                        }
                         """)
        self.button.clicked.connect(self.findFolder)
        self.show()


    @PyQt5.QtCore.pyqtSlot()
    def findFolder(self):
        filename = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(
               self, "Select Directory"))
        try:
            self.folderPath.setText(filename)
        except:
            pass
    def decrypt(self):
        if len(self.key.text()) == 32:
            self.xDecrypter = xDecrypter(self.key.text(), self.folderPath.text())
            ctypes.windll.user32.MessageBoxW(0, f"Starting Decrypter, please be patient and do not close this application until finished.", "Starting", 0x0 | 0x40)
            self.threadpool.start(self.xDecrypter)
        else:
            ctypes.windll.user32.MessageBoxW(0, "ERROR: The entered key is not valid.","ERROR", 0x0 | 0x10)


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv) 
    D = Main() 
    sys.exit(app.exec()) 



from PyQt5 import QtCore, QtGui, QtWidgets
import pict_rc
import sys
import cv2 as cv
import os

Face_Detector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
Eyes_Detector = cv.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

Current_Image = None
Current_Video = None

def Show_Message(code = 0):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/newPrefix/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    msg.setWindowIcon(icon)
    msg.setWindowTitle("Face And Eye Detector")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    if code == 0:
        msg.setText("An Error Occured While Opening The File")
    if code == 1:
        msg.setText("No File Has Been Selected")
    if code == 2:
        msg.setText("An Error Occured While Processing The File")
    if code == 3:
        msg.setText("Image Is Not Yet Detected")
    if code == 4:
        msg.setText("File Has Been Saved Successfully")
    if code == 5:
        msg.setText("Press 'Esc' To Exit Video")
    msg.exec_()

def Video_Detection(code):
    global Face_Detector, Eyes_Detector
    if code in ["", " ", None]:
        return
    if code == "0":
        video = cv.VideoCapture(0)
        outFile = "Webcam_Output.avi"
    else:
        video = cv.VideoCapture(code)
        outFile = code.split('/')[-1].split('.')[0]+"_Detected.avi"
    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    File = cv.VideoWriter(outFile,cv.VideoWriter_fourcc(*"XVID"),20.0,(width,height))
    Show_Message(5)
    while video.isOpened():
        ret, frame = video.read()
        if ret == False:
            break
        gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        for x,y,w,h in Face_Detector.detectMultiScale(gray_frame,1.1,4):
            cv.rectangle(frame,(x,y),(x+w,y+h),(255,100,150),thickness=4)
            for x1,y1,w1,h1 in Eyes_Detector.detectMultiScale(gray_frame):
                cv.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(100,150,255),thickness=4)
        cv.imshow("Output",frame)
        File.write(frame)
        if cv.waitKey(1) & 0xFF == 27:
            break
    video.release()
    File.release()
    cv.destroyAllWindows()
    Show_Message(4)
    os.system(outFile)

def Image_Detection(code):
    global Face_Detector, Eyes_Detector
    img = cv.imread(code)
    for x,y,w,h in Face_Detector.detectMultiScale(cv.cvtColor(img,6),1.1,4):
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),thickness=4)
    for x1,y1,w1,h1 in Eyes_Detector.detectMultiScale(cv.cvtColor(img,6)):
        cv.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),thickness=4)
    cv.imwrite("output.png",img)

def Image_file_opener():
    fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '',"Image files (*.jpg *.png)")
    return fname[0]

def Video_file_opener():
    fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '',"Video files (*.mp4 *.avi)")
    return fname[0]

class Ui_VideoScreen(object):
    def setupUi(self, VideoScreen):
        VideoScreen.setObjectName("VideoScreen")
        VideoScreen.resize(700, 700)
        VideoScreen.setMinimumSize(QtCore.QSize(700, 700))
        VideoScreen.setMaximumSize(QtCore.QSize(700, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VideoScreen.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(VideoScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(":/newPrefix/Video_Zone.png"))
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.backButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(630, 630, 51, 61))
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/dummy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon1)
        self.backButton.setObjectName("backButton")
        self.chooseButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.chooseButton.setGeometry(QtCore.QRect(210, 300, 311, 51))
        self.chooseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chooseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.chooseButton.setText("")
        self.chooseButton.setIcon(icon1)
        self.chooseButton.setObjectName("chooseButton")
        self.webcamButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.webcamButton.setGeometry(QtCore.QRect(180, 370, 371, 51))
        self.webcamButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.webcamButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.webcamButton.setText("")
        self.webcamButton.setIcon(icon1)
        self.webcamButton.setObjectName("webcamButton")
        VideoScreen.setCentralWidget(self.centralwidget)

        self.backButton.clicked.connect(self.Go_Selection)
        self.chooseButton.clicked.connect(self.Detect_From_Computer)
        self.webcamButton.clicked.connect(self.Detect_From_Cam)

        self.retranslateUi(VideoScreen)
        QtCore.QMetaObject.connectSlotsByName(VideoScreen)

    def Detect_From_Cam(self):
        try:
            Current_Video = "0"
            Video_Detection(Current_Video)
        except:
            Show_Message(0)
            Show_Message(2)
            return

    def Detect_From_Computer(self):
        global Current_Video
        try:
            Current_Video = Video_file_opener()
            Video_Detection(Current_Video)
        except:
            Show_Message(0)
            Show_Message(2)
            return

    def Go_Selection(self):
        global ui1,After_Splash
        ui1.setupUi(After_Splash)
        global Current_Video
        Current_Video = None
        After_Splash.show()
        VideoScreen.hide()

    def retranslateUi(self, VideoScreen):
        _translate = QtCore.QCoreApplication.translate
        VideoScreen.setWindowTitle(_translate("VideoScreen", "Face And Eye Detection"))
        self.backButton.setToolTip(_translate("VideoScreen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Choose File Type</span></p></body></html>"))
        self.chooseButton.setToolTip(_translate("VideoScreen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Choose Video From Computer</span></p></body></html>"))
        self.webcamButton.setToolTip(_translate("VideoScreen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Open Web Camera</span></p></body></html>"))

class Ui_Picture_Screen(object):
    def setupUi(self, Picture_Screen):
        Picture_Screen.setObjectName("Picture_Screen")
        Picture_Screen.resize(700, 700)
        Picture_Screen.setMinimumSize(QtCore.QSize(700, 700))
        Picture_Screen.setMaximumSize(QtCore.QSize(700, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Picture_Screen.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Picture_Screen)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(":/newPrefix/Picture_Zone.png"))
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.backButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(624, 630, 51, 61))
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/dummy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon1)
        self.backButton.setObjectName("backButton")
        self.actual_photo = QtWidgets.QLabel(self.centralwidget)
        self.actual_photo.setGeometry(QtCore.QRect(140, 120, 461, 431))
        self.actual_photo.setText("")
        self.actual_photo.setPixmap(QtGui.QPixmap(":/newPrefix/photo.png"))
        self.actual_photo.setScaledContents(True)
        self.actual_photo.setObjectName("actual_photo")
        self.detectButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.detectButton.setGeometry(QtCore.QRect(270, 590, 221, 31))
        self.detectButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.detectButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.detectButton.setText("")
        self.detectButton.setIcon(icon1)
        self.detectButton.setObjectName("detectButton")
        self.saveButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(280, 630, 185, 31))
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveButton.setText("")
        self.saveButton.setIcon(icon1)
        self.saveButton.setObjectName("saveButton")
        self.chooseButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.chooseButton.setGeometry(QtCore.QRect(140, 120, 461, 431))
        self.chooseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chooseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.chooseButton.setText("")
        self.chooseButton.setIcon(icon1)
        self.chooseButton.setObjectName("chooseButton")
        Picture_Screen.setCentralWidget(self.centralwidget)

        self.backButton.clicked.connect(self.Go_Selection)
        self.chooseButton.clicked.connect(self.Set_From_Computer)
        self.detectButton.clicked.connect(self.Detect_Picture)
        self.saveButton.clicked.connect(self.Save_Picture)

        self.retranslateUi(Picture_Screen)
        QtCore.QMetaObject.connectSlotsByName(Picture_Screen)

    def Save_Picture(self):
        global Current_Image
        if Current_Image in ["", " ", None]:
            Show_Message(1)
            return
        if not os.path.exists("output.png"):
            Show_Message(3)
            return
        outFile = Current_Image.split("/")[-1].split(".")[0]+"_Detected.png"
        os.rename("output.png",outFile)
        Show_Message(4)
        os.system(outFile)

    def Detect_Picture(self):
        global Current_Image
        if Current_Image in [""," ",None]:
            Show_Message(1)
            return
        try:
            Image_Detection(Current_Image)
        except:
            Show_Message(2)
            return
        else:
            self.actual_photo.setPixmap(QtGui.QPixmap("output.png"))

    def Set_From_Computer(self):
        global Current_Image
        try:
            Current_Image = Image_file_opener()
        except:
            Show_Message(0)
        else:
            if Current_Image == "" or Current_Image == " ":
                return
            if os.path.exists(Current_Image.split("/")[-1]):
                self.actual_photo.setPixmap(QtGui.QPixmap(Current_Image.split("/")[-1]))
                return
            self.actual_photo.setPixmap(QtGui.QPixmap(Current_Image))

    def Go_Selection(self):
        global ui1,After_Splash
        ui1.setupUi(After_Splash)
        global Current_Image
        Current_Image = None
        if os.path.exists("output.png"):
            os.remove("output.png")
        After_Splash.show()
        Picture_Screen.hide()

    def retranslateUi(self, Picture_Screen):
        _translate = QtCore.QCoreApplication.translate
        Picture_Screen.setWindowTitle(_translate("Picture_Screen", "Face And Eye Detection"))
        self.backButton.setToolTip(_translate("Picture_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Choose File Type</span></p></body></html>"))
        self.detectButton.setToolTip(_translate("Picture_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Detect Features In Image</span></p></body></html>"))
        self.saveButton.setToolTip(_translate("Picture_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Save Current Picture</span></p></body></html>"))
        self.chooseButton.setToolTip(_translate("Picture_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Choose Image File</span></p></body></html>"))

class Ui_After_Splash(object):
    def setupUi(self, After_Splash):
        After_Splash.setObjectName("After_Splash")
        After_Splash.resize(700, 700)
        After_Splash.setMinimumSize(QtCore.QSize(700, 700))
        After_Splash.setMaximumSize(QtCore.QSize(700, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        After_Splash.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(After_Splash)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(":/newPrefix/Selection_Screen.png"))
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.backButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(630, 630, 51, 61))
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/dummy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon1)
        self.backButton.setObjectName("backButton")
        self.pictureButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.pictureButton.setGeometry(QtCore.QRect(100, 330, 251, 61))
        self.pictureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pictureButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pictureButton.setText("")
        self.pictureButton.setIcon(icon1)
        self.pictureButton.setObjectName("pictureButton")
        self.videoButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.videoButton.setGeometry(QtCore.QRect(420, 330, 181, 61))
        self.videoButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.videoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.videoButton.setText("")
        self.videoButton.setIcon(icon1)
        self.videoButton.setObjectName("videoButton")
        After_Splash.setCentralWidget(self.centralwidget)

        self.videoButton.clicked.connect(self.Go_Video)
        self.pictureButton.clicked.connect(self.Go_Picture)
        self.backButton.clicked.connect(self.Go_Home)

        self.retranslateUi(After_Splash)
        QtCore.QMetaObject.connectSlotsByName(After_Splash)

    def Go_Video(self):
        global ui3, VideoScreen
        ui3.setupUi(VideoScreen)
        VideoScreen.show()
        After_Splash.hide()

    def Go_Picture(self):
        global ui2, Picture_Screen
        ui2.setupUi(Picture_Screen)
        Picture_Screen.show()
        After_Splash.hide()

    def Go_Home(self):
        global ui, Splash_Screen
        ui.setupUi(Splash_Screen)
        Splash_Screen.show()
        After_Splash.hide()

    def retranslateUi(self, After_Splash):
        _translate = QtCore.QCoreApplication.translate
        After_Splash.setWindowTitle(_translate("After_Splash", "Face And Eye Detection"))
        self.backButton.setToolTip(_translate("After_Splash", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Back To Home Screen</span></p></body></html>"))
        self.pictureButton.setToolTip(_translate("After_Splash", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Detect An Image</span></p></body></html>"))
        self.videoButton.setToolTip(_translate("After_Splash", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Detect Video</span></p></body></html>"))

class Ui_Splash_Screen(object):
    def setupUi(self, Splash_Screen):
        Splash_Screen.setObjectName("Splash_Screen")
        Splash_Screen.resize(700, 700)
        Splash_Screen.setMinimumSize(QtCore.QSize(700, 700))
        Splash_Screen.setMaximumSize(QtCore.QSize(700, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Splash_Screen.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Splash_Screen)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(":/newPrefix/Splash_Screen.png"))
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 660, 321, 31))
        self.label.setText("")
        self.label.setObjectName("label")
        self.EnterButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.EnterButton.setGeometry(QtCore.QRect(200, 450, 281, 71))
        self.EnterButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.EnterButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.EnterButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/dummy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.EnterButton.setIcon(icon1)
        self.EnterButton.setObjectName("EnterButton")
        Splash_Screen.setCentralWidget(self.centralwidget)

        self.EnterButton.clicked.connect(self.Take_To_Main)

        self.retranslateUi(Splash_Screen)
        QtCore.QMetaObject.connectSlotsByName(Splash_Screen)

    def Take_To_Main(self):
        global ui1, After_Splash
        ui1.setupUi(After_Splash)
        After_Splash.show()
        Splash_Screen.hide()

    def retranslateUi(self, Splash_Screen):
        _translate = QtCore.QCoreApplication.translate
        Splash_Screen.setWindowTitle(_translate("Splash_Screen", "Face And Eye Detector"))
        self.label.setToolTip(_translate("Splash_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Software Developed By Suraj Vijay [INDIA]</span></p></body></html>"))
        self.EnterButton.setToolTip(_translate("Splash_Screen", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Start Detecting</span></p></body></html>"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    VideoScreen = QtWidgets.QMainWindow()
    ui3 = Ui_VideoScreen()

    Picture_Screen = QtWidgets.QMainWindow()
    ui2 = Ui_Picture_Screen()
    
    After_Splash = QtWidgets.QMainWindow()
    ui1 = Ui_After_Splash()

    Splash_Screen = QtWidgets.QMainWindow()
    ui = Ui_Splash_Screen()
    ui.setupUi(Splash_Screen)
    
    Splash_Screen.show()
    
    sys.exit(app.exec_())
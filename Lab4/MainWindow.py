import time
import random
import sys
import re
from Lab4 import *
import serial


def serial_ports():  # функция, которая возвращает доступные ком порты
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]  # генерирует список, в котором будут строки типа сом1 сом2 ...
    else:
        raise EnvironmentError('Неподдерживаемая ОС')

    result = []  # пустой список
    for port in ports:  # возвращает объект сом1 и тд
        try:
            s = serial.Serial(port)  # открытие порта
            s.close()
            result.append(port)  # добавляем в список портов, если сом порт свооден и найден
        except (OSError, serial.SerialException):
            pass
    return result


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.frame_size = 36
        self.fl_frame = False
        self.frame = ""
        self.buf_to_get = ""
        self.  = 0
        self.is_collision = False
        self.available_keys = [
            Qt.Key_1,
            Qt.Key_0,
            Qt.Key_Enter,
            Qt.Key_Return,
            Qt.Key_Backspace
        ]
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        port_names = serial_ports()
        if ("COM1" not in port_names) and ("COM2" not in port_names):
            QMessageBox.critical(self, "Ошибка", "Отсутствуют порты COM1 и СOM2!")
            sys.exit(-1)
        try:
            self.ui.CD_Message.append("Попытка открытия порта COM1")
            self.s = serial.Serial(port="COM1", baudrate=9600, timeout=0)
            self.s.write(b"")
            self.ui.CD_Message.append("Порт COM1 открыт")
        except(OSError, serial.SerialException):
            try:
                self.ui.CD_Message.append("Невозможно открыть порт COM1")
                self.ui.CD_Message.append("Попытка открытия порта COM2")
                self.s = serial.Serial(port="COM2", baudrate=9600, timeout=0)
                self.s.write(b"")
                self.ui.CD_Message.append("Порт COM2 открыт")
            except(OSError, serial.SerialException):
                self.ui.CD_Message.append("Невозможно открыть порт COM2")
                QMessageBox.critical(self, "ОШИБКА ОТКРЫТИЯ ПОРТОВ", "Невозможно открыть порт\t")
                sys.exit(-1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readComPort)
        self.timer.setInterval(1000)
        self.timer.start()
        self.ui.InputMessage.installEventFilter(self)
        self.ui.CD_Message.cursorPositionChanged.connect(self.on_click)

    def write_port(self, symbol):
        try:
            self.s.write(bytes(symbol.encode("cp1251")))  # функция, которая записывает байтовые строкив ком порт
        except(OSError, serial.SerialException):
            self.ui.CD_Message.append("Невозможно записать в порт " + self.s.port + "\t")

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress:
            if event.key() in self.available_keys:
                if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
                    cursor = self.ui.InputMessage.textCursor().positionInBlock()
                    if (len(self.ui.InputMessage.toPlainText())) != cursor:  # если курсор не в конце строки
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return True
        return super(MainWindow, self).eventFilter(self, event)

    def collision_generation(self):
        rand = bool(random.getrandbits(1))
        if rand:
            return 1
        else:
            return 0

    def is_channel_busy(self):
        rand = random.randint(1, 5)
        if rand == 1:
            return True
        else:
            return False

    def delay_generation(self, k=0):
        return random.randint(1, 2 ** k)

    @Slot()
    def on_InputMessage_textChanged(self):
        input_message = str(self.ui.InputMessage.toPlainText())
        input_bits = input_message[:- 1]
        if input_message.endswith("\n"):
            if input_message == "\n":
                self.ui.InputMessage.clear()
                return
            else:
                input_bits = re.sub("[^0-1]", "", input_bits)
                if len(input_bits) == 0:
                    self.ui.CD_Message.append("Неправильный ввод")
                    self.ui.InputMessage.clear()
                    return
                while len(input_bits) > 0:
                    if len(input_bits) >= self.frame_size:
                        self.frame = input_bits[:self.frame_size]
                        input_bits = input_bits[self.frame_size:]
                    else:
                        amount_to_add = self.frame_size - len(input_bits)
                        self.frame = input_bits + amount_to_add * "0"
                        input_bits = ""
                    self.ui.CD_Message.append("Строка для отправки: \"" + self.frame + "\" ")

                    self.try_counter = 0
                    self.is_collision = False
                    while True:
                        while self.is_channel_busy():
                            self.ui.CD_Message.append("В данный момент канал занят.")
                        self.ui.CD_Message.append("Канал свободен.")
                        self.write_port(self.frame)
                        if self.collision_generation():
                            self.write_port("*")
                            self.is_collision = True
                            self.try_counter += 1
                            self.ui.CD_Message.append(self.frame + ": " + "*" * self.try_counter)
                            self.ui.CD_Message.append("Попытка №{} получения доступа к каналу"
                                                      .format(str(self.try_counter)))
                            if self.try_counter > 10:
                                self.ui.CD_Message.append("ОШИБКА: слишком много попыток доступа к каналу.")
                                break
                            else:
                                delay = self.delay_generation(self.try_counter)
                                self.ui.CD_Message.append("Задержка: " + str(delay / 60) + " сек")
                                time.sleep(delay / 60)
                                self.ui.CD_Message.append("Задержка завершена")
                        else:
                            self.ui.CD_Message.append(self.frame + ": коллизии не было")
                            self.frame = ""
                            break
                self.write_port("\n")
                self.ui.InputMessage.clear()

    def  (self, frame):
        self.fl_frame = False
        self.ui.OutputMessage.insertPlainText(frame)
        self.ui.CD_Message.append("Коллизии не было")

    @Slot()
    def readComPort(self):
        try:
            symbol = self.s.read(1)
            while symbol != b'':
                if "\\" in str(symbol):
                    if self.fl_frame:
                        self.print_into_output(self.buf_to_get)
                        self.buf_to_get = ""
                    if "\\n" in str(symbol):
                        if not self.fl_frame:
                            self.buf_to_get = ""
                            self.ui.OutputMessage.insertPlainText("\n")
                else:
                    symbol = symbol.decode('cp1251')
                    self.buf_to_get += symbol
                    if len(self.buf_to_get) == 36:
                        self.fl_frame = True
                    elif len(self.buf_to_get) == 37:
                        if "*" in self.buf_to_get:
                            self.ui.CD_Message.append("Коллизия")
                            self.buf_to_get = ""
                            self.fl_frame = False
                        else:
                            if self.buf_to_get[-1] == '0' or self.buf_to_get[-1] == '1':
                                self.print_into_output(self.buf_to_get[:-1])
                                self.buf_to_get = self.buf_to_get[-1]
                            else:
                                self.ui.CD_Message.append("ОШИБКА: Произошла неизветная ошибка")
                symbol = self.s.read(1)
        except(OSError, serial.SerialException):
            self.timer.stop()
            self.ui.CD_Message.append("Невозможно прочитать из порта " + self.s.port + "\t")
            self.ui.InputMessage.setReadOnly(1)
            self.ui.CD_BtnClear.setEnabled(0)
            self.ui.OutputBtnClear.setEnabled(0)
            self.ui.CD_CB_PortSpeed.setEnabled(0)

    @Slot()
    def on_OutputBtnClear_clicked(self):
        self.ui.CD_Message.append('Нажата кнопка "Отчистить вывод"')
        self.ui.OutputMessage.clear()

    @Slot()
    def on_CD_BtnClear_clicked(self):
        self.ui.CD_Message.append('Нажата кнопка "Отчистить КЛ"')
        self.ui.CD_Message.clear()

    @Slot(str)
    def on_CD_CB_PortSpeed_currentIndexChanged(self, i):
        self.s.baudrate = int(i)
        self.ui.CD_Message.append(str(self.s.port) + " скорость порта и приема данных изменена на: " + i)

    def on_click(self):
        self.ui.CD_Message.moveCursor(QTextCursor.End)

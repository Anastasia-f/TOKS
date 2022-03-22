from Lab2 import *
from serial import SerialException
import sys
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
        self.buffer_to_send = "0000000"
        self.buffer_to_get = "0000000"
        self.flag = "0010010"
        self.check_len_buffer = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.alarm = 0
        self.needNewLine = 0
        self.is_sub_flag = False
        self.is_sub_flag_debit = False
        self.unprintable_symbol = ""
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
        self.ui.Bit_stuffing.verticalScrollBar().setValue(self.ui.Bit_stuffing.verticalScrollBar().maximum())
        self.available_keys = [
            Qt.Key_1,
            Qt.Key_0,
            Qt.Key_Enter,
            Qt.Key_Return,
            Qt.Key_Backspace
        ]

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

    def write_port(self, symbol):
        try:
            self.s.write(bytes(symbol.encode("cp1251")))  # функция, которая записывает байтовые строкив ком порт
        except(OSError, serial.SerialException):
            self.ui.CD_Message.append("Невозможно записать в порт " + self.s.port + "\t")

    @Slot()
    def on_InputMessage_textChanged(self):
        input_message = str(self.ui.InputMessage.toPlainText())
        output = ""
        if input_message.endswith("\n"):
            if input_message == "\n":
                self.ui.InputMessage.clear()
            else:
                self.ui.CD_Message.append('Введенная строка: "' +
                                          input_message[:-1] + '"')
                self.ui.Bit_stuffing.append('Строка для отправки: "')
                for i in input_message:
                    if i == "\n":
                        self.write_port(i)
                        self.ui.Bit_stuffing.insertPlainText("\"")
                        self.is_sub_flag = False
                    else:
                        self.buffer_to_send = self.buffer_to_send[1:] + i
                        if self.is_sub_flag:
                            self.is_sub_flag = False
                            if i == "0":
                                self.write_port("1")
                                output += "1"
                                self.ui.Bit_stuffing.setTextColor('#ff00ff')
                                self.ui.Bit_stuffing.insertPlainText("1")
                                self.ui.Bit_stuffing.setTextColor(Qt.black)
                        self.ui.Bit_stuffing.insertPlainText(i)
                        self.write_port(i)

                        if self.flag == self.buffer_to_send:
                            self.is_sub_flag = True
                self.ui.InputMessage.clear()

    @Slot()
    def readComPort(self):
        try:
            symbol = self.s.read(1)
            while symbol != b'':
                symbol = symbol.decode('cp1251')
                if symbol == "\n":
                    if self.alarm == 0:
                        if self.is_sub_flag_debit:
                            self.ui.OutputMessage.insertPlainText(self.unprintable_symbol)
                            self.is_sub_flag_debit = False
                            self.unprintable_symbol = ""
                        self.ui.OutputMessage.insertPlainText(symbol)
                    else:
                        self.needNewLine = 1
                else:
                    if self.alarm == 1:
                        self.unprintable_symbol = symbol
                        self.is_sub_flag_debit = True
                        self.alarm = 0
                    else:
                        self.buffer_to_get = self.buffer_to_get[1:] + symbol
                        if self.flag == self.buffer_to_get:
                            self.alarm = 1
                        if self.is_sub_flag_debit:
                            self.is_sub_flag_debit = False
                            if symbol == "1":
                                self.ui.OutputMessage.insertPlainText(self.unprintable_symbol)
                                self.unprintable_symbol = ""
                        self.ui.OutputMessage.insertPlainText(symbol)
                symbol = self.s.read(1)
        except(OSError, SerialException):
            self.timer.stop()
            self.ui.CD_Message.append("Невозможно прочитать из порта " + self.s.port + "\t")
            self.ui.InputMessage.setReadOnly(1)
            self.ui.CD_BtnClear.setEnabled(0)
            self.ui.OutputBtnClear.setEnabled(0)
            self.ui.CD_CB_PortSpeed.setEnabled(0)
            self.ui.CD_BtnClearBitStuff.setEnabled(0)

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

    @Slot()
    def on_CD_BtnClearBitStuff_clicked(self):
        self.ui.CD_Message.append('Нажата кнопка "Отчистить бит стаффинг"')
        self.ui.Bit_stuffing.clear()

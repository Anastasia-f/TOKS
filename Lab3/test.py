import random
import sys
from Lab3 import *
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

        self.d1 = [i for i in range(3, 43, 2)]
        self.d2 = sorted([i for i in range(3, 43, 4)] + [i for i in range(6, 43, 4)])
        self.d3 = [i for i in range(5, 8)] + [i for i in range(12, 16)] + [i for i in range(20, 24)] + \
                  [i for i in range(28, 32)] + [i for i in range(36, 40)]
        self.d4 = [i for i in range(9, 16)] + [i for i in range(24, 32)] + [i for i in range(40, 43)]
        self.d5 = [i for i in range(17, 32)]
        self.d6 = [i for i in range(33, 43)]
        self.dall = [self.d1, self.d2, self.d3, self.d4, self.d5, self.d6]
        self.control_bits = [1, 2, 4, 8, 16, 32]
        self.frame = ""
        self.buf_to_get = ""
        self.pbit = ""
        self.rbits = ""
        self.bits_to_remove = 0
        self.check = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.available_keys = [
            Qt.Key_1,
            Qt.Key_0,
            Qt.Key_Enter,
            Qt.Key_Return,
            Qt.Key_Backspace
        ]
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

    def add_empty_check_bits(self, bit_str):
        bit_str += "00"
        for bit in self.control_bits[2:]:
            bit_str = bit_str[:-1 * bit + 1] + "0" + bit_str[-1 * bit + 1:]
        return bit_str

    def set_check_bits(self, bit_str):
        r_bit = 0
        for d in self.dall:
            value = 0
            for i in d:
                value += int(bit_str[-1 * i])
            value %= 2
            pos = self.control_bits[r_bit]
            if pos != 1:
                bit_str = bit_str[:-1 * pos] + str(value) + bit_str[-1 * pos + 1:]
            else:
                bit_str = bit_str[:-1 * pos] + str(value)
            r_bit += 1
        value = 0
        for i in bit_str:
            value += int(i)
        bit_str = str(value % 2) + bit_str
        return bit_str

    # new+
    def get_info_bits(self, bit_str):
        for i in self.control_bits[::-1]:
            if i != 1:
                bit_str = bit_str[:-1 * i] + bit_str[-1 * i + 1:]
            else:
                bit_str = bit_str[:-1 * i]
        bit_str = bit_str[1:]
        return bit_str

    # new+
    def check_mistakes(self, bit_str):
        self.rbits = ""
        self.pbit = 0
        for i in bit_str:
            self.pbit += int(i)
        self.pbit %= 2
        for i in self.control_bits[::-1]:
            self.rbits += bit_str[-1 * i]
        cbits = ""
        count = -1
        for d in self.dall:
            value = 0
            for i in d:
                value += int(bit_str[-1 * i])
            value += int(self.rbits[count])
            value %= 2
            cbits = str(value) + cbits
            count -= 1
        c = 0
        for i in range(0, 5):
            c += int(cbits[i]) * self.control_bits[-1 * i - 1]
        if c == 0:
            if self.pbit == 0:
                self.outputFRAME(bit_str, "no error", 0, cbits)  # new !!!!
            else:
                self.outputFRAME(bit_str, "p-bit error", 42, cbits)  # new !!!!
        else:
            if self.pbit == 0:
                self.outputFRAME(bit_str, "2-bit error", 0, cbits)  # new !!!!
                return -1
            else:
                self.outputFRAME(bit_str, "error pos: " + str(c), c, cbits)  # new !!!!
                bit_str = self.change_el(bit_str, c)
                string = "corrected string:\n" + bit_str
                self.ui.CD_Message.append(string)
        return bit_str

    # new !!!!
    def outputFRAME(self, bit_str, message, error_pos, cbits):
        for i in range(-42, 0):
            if -1 * i in self.control_bits or i == -42:
                self.ui.CD_Message.setTextBackgroundColor(Qt.yellow)
            if -1 * i == error_pos:
                self.ui.CD_Message.setTextBackgroundColor(Qt.red)
                self.ui.CD_Message.setTextColor(Qt.white)
            self.ui.CD_Message.insertPlainText(bit_str[i])
            self.ui.CD_Message.setTextColor(Qt.black)
            self.ui.CD_Message.setTextBackgroundColor(Qt.white)
        string = ":" + cbits + "\n" + message
        self.ui.CD_Message.insertPlainText(string)

    # new+
    def change_el(self, bit_str, pos):
        elem = int(bit_str[-1 * pos])
        if elem:
            elem = 0
        else:
            elem = 1
        if pos == 1:
            bit_str = bit_str[:-1 * pos] + str(elem)
        else:
            bit_str = bit_str[:-1 * pos] + str(elem) + bit_str[-1 * pos + 1:]
        return bit_str

    # new+
    def add_mistakes(self, bit_str):
        rand = random.randint(0, 1)
        if rand:
            rand = random.randint(1, 42)
            bit_str = self.change_el(bit_str, rand)
            rand2 = random.randint(1, 10)
            if rand2 in range(1, 5):
                rand2 = rand
                while rand == rand2:
                    rand2 = random.randint(1, 42)
                bit_str = self.change_el(bit_str, rand2)
        return bit_str

    @Slot()
    def on_InputMessage_textChanged(self):
        input_message = str(self.ui.InputMessage.toPlainText())
        input_bits = input_message[:len(input_message) - 1]
        if input_message.endswith("\n"):
            if input_message == "\n":
                self.ui.InputMessage.clear()
                pass
            else:
                while len(input_bits) > 0:
                    amount_to_add = 0
                    if len(input_bits) >= self.frame_size:
                        self.frame = input_bits[:self.frame_size]
                        input_bits = input_bits[self.frame_size:]
                    else:
                        amount_to_add = self.frame_size - len(input_bits)
                        self.frame = amount_to_add * "0" + input_bits
                        input_bits = ""
                    self.frame = self.add_empty_check_bits(self.frame)
                    self.frame = self.set_check_bits(self.frame)
                    self.ui.CD_Message.append("String to send: \"" + self.frame + "\"")
                    self.s.write(amount_to_add.to_bytes(1, byteorder='big'))
                    # for i in self.frame:
                    #     self.write_port(i)
                    self.write_port(self.frame)
                    self.frame = ""
                self.write_port("\n")
                self.ui.InputMessage.clear()

    # new
    @Slot()
    def readComPort(self):
        try:
            symbol = self.s.read(1)
            while symbol != b'':
                if "\\" in str(symbol):
                    if "\\n" in str(symbol):  # and self.check != -1:
                        self.ui.OutputMessage.insertPlainText("\n")
                    else:
                        self.bits_to_remove = int.from_bytes(symbol, byteorder='big')
                        # self.check = 0
                else:
                    symbol = symbol.decode('cp1251')
                    self.buf_to_get += str(symbol)
                    if len(self.buf_to_get) == 42:
                        self.ui.CD_Message.append("FRAME: ")
                        self.buf_to_get = self.add_mistakes(self.buf_to_get)
                        self.check = self.check_mistakes(self.buf_to_get)
                        if self.check != -1:
                            self.buf_to_get = self.check
                            string = self.get_info_bits(self.buf_to_get)
                            self.ui.OutputMessage.insertPlainText(string[self.bits_to_remove:])
                        self.buf_to_get = ""
                symbol = self.s.read(1)
        except(OSError, serial.SerialException):
            self.timer.stop()
            self.ui.CD_Message.append("Can't read from " + self.s.port + "\t")
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

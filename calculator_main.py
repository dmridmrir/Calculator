import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout()

        # 수식과 답을 나타낼 QLineEdit 위젯 생성
        self.equation = QLineEdit()
        self.equation.setReadOnly(True)  # 읽기 전용으로 설정하여 사용자가 직접 편집하지 못하도록 함

        # 수식 및 버튼을 그리드 레이아웃에 추가
        main_layout.addWidget(self.equation, 0, 0, 1, 4)

        # 숫자 버튼 생성하고, 그리드 레이아웃에 추가
        # 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력될 수 있도록 시그널 설정
        number_button_dict = {}
        order = [7, 8, 9, 4, 5, 6, 1, 2, 3] 
        for i, number in enumerate(order):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num=number:
                                               self.number_button_clicked(num))
            x, y = divmod(i, 3)
            main_layout.addWidget(number_button_dict[number], x+4, y)

        number_button_dict[0] = QPushButton("0")
        number_button_dict[0].clicked.connect(lambda state, num=0: self.number_button_clicked(num))
        main_layout.addWidget(number_button_dict[0], 7, 1)

        # 소숫점 버튼을 그리드 레이아웃에 추가하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num=".": self.number_button_clicked(num))
        main_layout.addWidget(button_dot, 7, 2)

        # 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("÷")

        # 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation="+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation="-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation="*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation="÷": self.button_operation_clicked(operation))

        # 사칙연산 버튼을 그리드 레이아웃에 추가
        main_layout.addWidget(button_plus, 6, 3)
        main_layout.addWidget(button_minus, 5, 3)
        main_layout.addWidget(button_product, 4, 3)
        main_layout.addWidget(button_division, 3, 3)

        # =, clear, backspace 버튼 생성
        # % 1/x x^2 sqrt(x) +/- 키 생성
        button_mod = QPushButton("%")
        button_fountain = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_sqrt = QPushButton("√x")
        button_sign = QPushButton("+/-")
        button_equal = QPushButton("=")
        button_clear1 = QPushButton("CE")
        button_clear2 = QPushButton("C")
        button_backspace = QPushButton("◁")


        #새로 생성한 버튼 추가
        # =, clear, backspace 버튼을 그리드 레이아웃에 추가
        main_layout.addWidget(button_clear1, 2, 1)
        main_layout.addWidget(button_clear2, 2, 2)
        main_layout.addWidget(button_backspace, 2, 3)
        main_layout.addWidget(button_equal, 7, 3)
        main_layout.addWidget(button_mod, 2, 0)
        main_layout.addWidget(button_fountain, 3, 0)
        main_layout.addWidget(button_square, 3, 1)
        main_layout.addWidget(button_sqrt, 3,2)
        main_layout.addWidget(button_sign, 7, 0)

        # =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear1.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)        
        button_backspace.clicked.connect(self.button_backspace_clicked)


        # 위젯을 설정한 레이아웃으로 설정
        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    arr = [None]
    i = 0

    def number_button_clicked(self, num):
        current_equation = self.equation.text()
        self.equation.setText(current_equation + str(num))

    def button_operation_clicked(self, operation):
        current_equation = self.equation.text()
        self.arr.extend([str(current_equation), str(operation)])
        self.i += 1
        self.equation.setText("")

    def evaluate_expression(self, expression):
        result = eval(expression) if expression else None
        return result

    def button_equal_clicked(self):
        equation = self.equation.text()
        result = self.evaluate_expression(''.join(filter(None, self.arr)))
        self.arr.append(str(equation))
        self.equation.setText(str(result))
        self.arr = [str(result)]

    def button_equal_clicked(self):
        equation = self.equation.text()
        try:
            self.arr.append(str(equation))

            result = self.evaluate_expression(''.join(filter(None, self.arr)))
            self.equation.setText(str(result))

            self.arr = [str(result)]

        except Exception as e:
            error_message = f"에러: {e}"
            QMessageBox.critical(self, "에러", error_message)
            self.equation.setText("")

    def button_clear_clicked(self):
        self.equation.setText("")
        self.arr = []

    def button_backspace_clicked(self):
        current_equation = self.equation.text()
        self.equation.setText(current_equation[:-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
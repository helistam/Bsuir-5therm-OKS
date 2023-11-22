# This is a sample Python script.
import random

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings
#
polynomial = [int(bit) for bit in "100101"]#x5+x2+1

def string_to_bits(string):
    # Преобразование каждого символа в ASCII-код и получение его бинарного представления
    bits = [format(ord(char), '08b') for char in string]
    # Объединение всех бинарных представлений в одну строку
    bit_string = ''.join(bits)
    # Преобразование строки из битов в список целых чисел
    return [int(bit) for bit in bit_string]

def add_modulo_two(allmessage, remains):
    align_len = len(allmessage)- len(polynomial)+1
    remains =[0] * align_len+remains
    #message[24]=1 #для одиночной ошибки
    result = [(x + y) % 2 for x, y in zip(allmessage, remains)]
    return result

def ERROR_FIX(message_bits,crc_hash):
    chek = find_error(message_bits, crc_hash)  # остаток от деления

    count_ones = chek.count(1)
    allmessage = message_bits + crc_hash
    print("Kolich edinnic v ostatke", count_ones)
    cicl_count = 0
    if count_ones == 1:
        message_bits = add_modulo_two(allmessage, chek)
        print("FIX message")
        print(message_bits)
    else:
        if count_ones > 1:
            matrix = compare_func()
            for i in range(24):
                sender = matrix[i]
                new_code = find_error(sender[:24], sender[24:])
                if (chek == new_code):
                    print(matrix[i])
                    for j in range(len(matrix[i])):
                        if matrix[i][j] == 1:
                            if allmessage[j] == 0:
                                allmessage[j] = 1
                            else:
                                if allmessage[j] == 1:
                                    allmessage[j] = 0
    print("Result")
    print(allmessage)
def CRCcode(StrToCode):
    bitstr = ''.join(format(ord(char), '08b') for char in StrToCode)
    message_bits = string_to_bits(StrToCode)
    crc_hash=calculate_hash(message_bits)
    print("CRC_CASH",crc_hash)
    print("Message+CRC_CASH")
    print(message_bits+crc_hash)

    message_bits[1]=0
    print("Message with error")
    print(message_bits + crc_hash)
    random_bit_index = random.randint(0, 23)
    message_bits[random_bit_index] = 0
    ERROR_FIX(message_bits,crc_hash)

def compare_func():
    matrix = []

    for i in range(24):
        vector = [0] * 29
        vector[23-i] = 1
        matrix.append(vector)
    # Выводим результат
    #for vector in matrix:
     #   print(vector)
    return matrix
def calculate_hash(message: list[int]) -> list[int]:#тип возвращаемого значения
    hash_len = len(polynomial) - 1# т.к. строка делаем -1
    align_len = len(message) - 1

    reminder = message.copy() + [0] * hash_len #делимое с доп нулями
    divisor = polynomial.copy() + [0] * align_len# делитель

    for i, _ in enumerate(message):#это функция, которая создает итератор, возвращающий пары (индекс, элемент) для элементов в message
        if reminder[i] == divisor[i] == 1:
            reminder = [x ^ y for x, y in zip(reminder, divisor)]#zip- генератор кортежа: пример [1,0] и [0,1]==[(1,0),(0,1)]                                                                #^- побитовый xor для элементов списка
        divisor.pop() # cдивиг элементов делителя на 1 влево( чтобы делилось в столбик)
        divisor.insert(0, 0)

    return reminder[-hash_len:]

def find_error(message: list[int],CRScode)-> list[int]:
    hash_len = len(polynomial) - 1  # т.к. строка делаем -1
    align_len = len(message) - 1

    reminder = message.copy() + CRScode  # делимое с доп нулями
    divisor = polynomial.copy() + [0] * align_len  # делитель

    #reminder[24]=1#для одиночной ошибки
    for i, _ in enumerate(message):  # это функция, которая создает итератор, возвращающий пары (индекс, элемент) для элементов в message
        if reminder[i] == divisor[i] == 1:
            reminder = [x ^ y for x, y in zip(reminder,divisor)]  # zip- генератор кортежа: пример [1,0] и [0,1]==[(1,0),(0,1)]                                                                #^- побитовый xor для элементов списка
        divisor.pop()  # cдивиг элементов делителя на 1 влево( чтобы делилось в столбик)
        divisor.insert(0, 0)

    return reminder[-hash_len:]

CRCcode("abc")

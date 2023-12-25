# <center> Задания  </center> 
***
### Содержание
  [Лр1](#лабораторная-работа-1) Передача сырого потока по Com-поту
  
  [Лр2](#лабораторная-работа-2) Передача пакетов по Com-порту + байт-стаффинг 

  [Лр3](#лабораторная-работа-3) Циклические коды 
  
  [Лр4](#лабораторная-работа-4) Коллизия, jam-сигналы 
  
  [Лр5](#лабораторная-работа-5) Token Ring
***
### Лабораторная работа 1
1. В качестве ОС была выбрана Windows, язык программирования- Python 
2. Выбрать эмулятор COM-портов. Можно использовать Eterlogic Virtual Serial Ports Emulator. Ознакомиться с возможностями.
3. Создать в эмуляторе топологию, совместимую с показанной на рисунке.
![фото](https://github.com/helistam/Bsuir-5therm-OKS/raw/master/images/topology.png)
4. Написать коммуникационную программу в соответствии с требованиями ниже.

__Требования к наполнению программы:__
+ По одной паре COM-портов программа должна передавать данные в одну сторону, по другой -- в другую.
+ Программа должна быть собственно цельной программой (отдельным приложением), работающей на передачу и на прием (количество потоков и так далее не регламентировано).
+ Номера COM-портов должны выбираться автоматически (по определенному алгоритму) один раз -- при запуске программы.
+ Данные должны передаваться посимвольно, причем как «сырой
поток».

__Требования к интерфейсу программы:__
+ Интерфейс должен состоять из четырех либо пяти окон: окна ввода, окна вывода, окна управления, окна состояния и опционального отладочного
окна.
+ Окна могут быть одного из самых разных стилей (зависит от ОС и так далее).
+ Окно ввода, очевидно, необходимо чтобы вводить символы для передачи. Должны поддерживаться все печатные символы (буквы, цифры и
так далее) плюс Enter. Порция набранных символов должна поступать в канал после нажатия Enter. Программа должна быть постоянно готова к вводу символов (вплоть до закрытия).
+ Окно вывода необходимо чтобы выводить принятые символы. Порция принятых символов должна сразу быть отображена. При этом сообщение в 
окне вывода должно полностью совпадать с сообщением в окне ввода программы-абонента.
+ Окно управления должно содержать следующий элемент (остальные параметры портов должны быть фиксированными)
Форму для выбора варианта проверки паритета
+ В окно состояния необходимо вывести:
Номера COM – портов для передачи и приема;
Количество переданных байт
+ В опциональное отладочное окно можно выводить отладочную информацию («для себя»).

***
### Лабораторная работа 2
Написать программу для пакетной передачи данных через COM-порты,в соответствии с требованиями ниже.

__Требования к наполнению программы:__
1. Взять за основу программу, относящуюся к лабораторной работе №1.
2. Реализовать структуру пакета -- в данном случае кадра, показанную 
на рисунке:
![фото](https://github.com/helistam/Bsuir-5therm-OKS/raw/master/images/package.png)

    Длина поля данных должна быть фиксированной и равной n байтам, где n -- номер по списку группы. В качестве флага использовать символ со значением 'z' + n. В поле Source Address записывать номер передающего COM-порта. Поля Destination Address и FCS предусмотреть, но передавать нулевыми.
3. Реализовать алгоритм байт стаффинга.

__Требования к интерфейсу программы:__
1. Модифицировать окно состояния. Выводить структуру текущего кадра после приема (до де-бит/байт-стаффинга). Один кадр должен соответствовать одной строке. При этом выделять (любым образом) биты (байты), модифицированные в результате бит/байт-стаффинга
***

### Лабораторная работа 3
Дополнить программу пакетной передачи данных через COM-порты возможностью проверки кадров в соответствии с требованиями ниже.

__Требования к наполнению программы:__
1. Взять за основу программу, относящуюся к лабораторной работе 
№2.
2. Реализовать поддержку поля FCS в структуре кадра - для проверки кадра с помощью циклического кода. При этом циклический код применять только к полю Data. Длину поля FCS необходимо рассчитать с учетом исходных требований (в битах, поскольку циклический код имеет битовую природу) и «округлить» (до байтов, поскольку минимальной единицей передаваемых через COM-порт данных является байт). 
3. Исходные требования к циклическому коду: код должен обнаруживать и исправлять одиночные ошибки. В рамках кодирования и декодирования кадров, программно реализовать алгоритм деления полиномов (делить как «на бумаге»). Для некоторого упрощения, циклический код применять только к кадрам, не подверженным байт-стаффингу. Предусмотреть возможность случайного искажения одного случайного бита в одном случайном байте в поле Data каждого кадра перед передачей. 
Вероятность искажения должна составлять 50 %.

__Требования к интерфейсу программы:__
1. Модифицировать окно состояния. По-прежнему периодически выводить структуру текущего кадра после приема, но немного по-другому (до декодирования). Один кадр по-прежнему должен соответствовать одной строке. При этом выделять (подчеркиванием либо другим цветом) поле FCS.
***
### Лабораторная работа 4
Написать программу пакетной передачи данных через COM-порты упрощенным алгоритмом CSMA/CD в соответствии с требованиями.
__Требования к наполнению программы:__
1. Взять за основу программу, относящуюся к лабораторной работе №3.
2. На стороне передатчика, реализовать три ключевых шага алгоритма:
прослушивание канала, обнаружение коллизии и розыгрыш случайной задержки (в соответствующей последовательности).
3. Предусмотреть возможность эмуляции занятости канала. Вероятность занятости канала должна составлять 50 %.
4. Предусмотреть возможность эмуляции коллизии.
Коллизию рассматривать применительно к кадру целиком (не к байту). Вероятность коллизии должна составлять 25%
5. Для расчета случайной задержки использовать стандартную формулу.
6. Из дополнения к алгоритму:
Реализовать поддержку jam-сигнала (дополнительно и правильно; как на стороне передатчика, так и на 
стороне приемника).

__Требования к интерфейсу программы:__
1. Модифицировать окно состояния. По-прежнему периодически выводить структуру текущего кадра (байта) перед передачей, но с 
дополнением (информацией о коллизиях). Один кадр по-прежнему должен соответствовать одной строке
***
### Лабораторная работа 5
Написать коммуникационную программу, реализующую упрощенный вариант алгоритма Token Ring, с учетом следующих пунктов задания.
1. Взять за основу программу, относящуюся к лабораторной работе №3.
2. Программа должна соответствовать однонаправленной кольцевой топологии, охватывающей три пользовательские станции.
3. Программа должна включать по крайней мере две подпрограммы -- передающую и принимающую, если задействуются реальные COM-порты.Либо три пары таковых подпрограмм, если пользовательские станции эмулируются.
4. К каждой станции должны относиться отдельные окна для ввода и вывода текстовых сообщений.
5. На станции-передатчике сообщение должно разбиваться на блоки фиксированной длины. Поскольку алгоритм Token Ring не мыслим без дополнительных служебных полей, блоки должны "обрамляться" этими полями.
6. Для обеспечения возможности выбора станции назначения должна быть предусмотрена юникаст-адресация (дополнительные элементы 
интерфейса для присвоения и указания адресов, одно либо несколько соответствующих полей в структуре пакета).
7. Должны быть предусмотрены два уровня приоритетов станций (дополнительные элементы интерфейса для присвоения приоритетов, одно либо несколько соответствующих полей в структуре пакета).
8. Должна быть реализована суть алгоритма Token Ring: перепасовка маркера и использование маркера для пересылки сообщения с учетом приоритетов. Остальное (например, раннее освобождение маркера) -- опционально.
9. Любая из станций по требованию должна становиться и станцией-монитором -- в дополнение к своему основному назначению. Минимальный набор функций станции-монитора: генерация маркера, контроль маркера, предотвращение циклов.
10. Программа должна иметь отдельное отладочное окно. В этом окне, по крайней мере, должно отражаться продвижение маркера и пакетов с данными.
11. Программа должна работать "циклически"
***

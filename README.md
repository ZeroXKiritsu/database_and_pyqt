1. Реализация метакласса ClientVerifier, выполняющий базовую проверку класса «Клиент» (для некоторых проверок используется модуль dis):
отсутствие вызовов accept и listen для сокетов;
использование сокетов для работы по TCP;
отсутствие создания сокетов на уровне классов, то есть отсутствие конструкций такого вида: class Client: s = socket() ...
2. Реализация метакласса ServerVerifier, выполняющий базовую проверку класса «Сервер»:
отсутствие вызовов connect для сокетов;
использование сокетов для работы по TCP. ### 
3. Реализация дескриптора для класса серверного сокета, а в нем — проверку номера порта. Это должно быть целое число (>=0). Значение порта по умолчанию равняется 7777. Дескриптор надо создать в отдельном классе. Его экземпляр добавить в пределах класса серверного сокета. Номер порта передается в экземпляр дескриптора при запуске сервера.
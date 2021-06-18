**Shared package** `documentation`
=================================================

Пакет общих утилит, использующихся в разных модулях проекта.

**__init__.py**
--------------------
.. automodule:: shared.__init__
   :members:

**wrapper.py**
---------------

.. automodule:: shared.wrapper
   :members:

**descriptors.py**
---------------------

.. autoclass:: shared.descriptors.Port
   :members:

**errors.py**
---------------------

.. autoclass:: shared.errors.ServerError
   :members:

**metaclasses.py**
-----------------------

.. autoclass:: shared.metaclasses.ServerMaker
   :members:



**utils.py**
---------------------


shared.utils. **get_message** (client)

    Функция приёма сообщений от удалённых компьютеров. Принимает сообщения JSON,
    декодирует полученное сообщение и проверяет что получен словарь.

shared.utils. **send_message** (sock, message)

    Функция отправки словарей через сокет. Кодирует словарь в формат JSON и отправляет через сокет.


**variables.py**
---------------------

    Глобальные переменные используемые в проекте
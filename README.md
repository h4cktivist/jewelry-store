# Гайд по воспроизвдению кода

Так как данный проект содержит бэкенд и создан с использованием веб-фреймворка для Python - Flask, то и его запуск будет происходить через запуск сервера на Python.

Следуйте данной небольшой инструкции, чтобы воспроизвести данный проект на своем компьютере.


### Клонирование репозитория
Для начала необходимо склонировать данный репозиторий в нужное вам место на вашем компьютере. Это можно сделать следующей командой в терминале:
```sh
$ git clone https://github.com/h4cktivist/jewelry-store.git
```
Либо выполнить следующие действия, загрузив архив с данным репозиторием и распаковав его в нужном вам месте:

![img2](https://user-images.githubusercontent.com/51692800/98440897-56440a80-211d-11eb-8608-8015397e073b.png)


### Установка Python 3.8.5 и PIP
Перейдем к установке Python. Я рекомендую установить Python версии 3.8.5, так как именно на ней был написан бэкенд проекта. Загрузить установщик Python 3.8.5 можно перейдя по этой [ссылке](https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe) .

После этого необходимо открыть установщик, поставить галочку напротив Add Python 3.8 to PATH (важно) и нажать Install Now.


### Установка необходимых модулей
Следующим шагом нам нужно установить необходимые для работы модули и фреймворки, используя менеджер пакетов Python - PIP. PIP должен был установиться автоматически, после того, как мы установили Python в прошлом шаге.

Все нужные модули собраны в файле requirements.txt, который находится в данном репозитории. Вам лишь необходимо выполнить следующие команды в терминале:

```sh
$ cd 'путь к папке проекта'
$ pip install -r requirements.txt
```
После этого должна пойти установка модулей и фреймворков, прописанных в requirements.txt.


### Запуск сервера на своем компьютере
Мы подходим к самой важной части данного гайда, для которой мы выполняли все предыдущие шаги - запуску сервера.

Для этого вам лишь необходимо выполнить следующую команду: 

```sh
$ app.py
```

Либо
```sh
$ python app.py
```

После этого вы должны увидеть в терминале следующее:
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 506-790-852
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```
 
 Чтобы увидеть результат запуска, перейдите в своем браузере по ссылке http://127.0.0.1:5000/ или http://localhost:5000/
 

 Ссылки, доступные для посещения:
- / (index.html)
- /admin_login (admin_login.html)
- /admin_page (admin_page.html)
- /user_login (user_login.html)
- /feedback (feedback.html)
- /order (order.html)
- /new_product_reg (new_product_reg.html)
- /ordres (orders.html)
- /products (products.html)

Ну вот и все, данными дейстивиями вы смогли запустить данный проект на своем компьютере и можете приступать к разработке. О ее нюансах речь пойдет в другом гайде.

# Гайд по ведению разработки фронтенда в данном проекте
Данный гайд посвящен особенностям написания фронтенда для проекта, в котором задействован Python и веб-фреймворк Flask.

### Расположение файлов
Здесь все предельно просто:
- .html файлы располагаются в папке templates, которая уже создана в данном репозитории;
- .css, .js файлы и картинки располагаются в папке static, которую необходимо будет создать.

### Линковка в HTML файлах
Очередная особенность написания фронтенда для Flask состоит в слегка измененной линковке static файлов, которые мы расположили в соотвествующей папке.

Линковка .css файлов происходит следующим образом:
```html
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='имя_css_файла') }}">
```
.js файлов:
```html
<script src="{{ url_for('static', filename='имя_js_файла') }}"></script>
```
Картинок:
```html
<img src="{{ url_for('static', filename='имя_картинки') }}"
```

В данном небольшом гайде я рассказал о некоторых особенностях разработки фронтенда в данном проекте. Со временем, гайд будет дополняться различными полезными фичами, которые предоставляет Flask, во время разработки фронтенда (надеюсь). 

# Использование системы контроля версий Git

Так как разработка проекта ведется несколькими разработчиками, целесообразно будет использовать систему контроля версий. Мы возьмем Git. Я бы настоятельно рекомендовал ознакомиться с основами его работы в этом [курсе](https://www.youtube.com/playlist?list=PL0lO_mIqDDFUesRNkeg46TDd5I6r7p2PI). (З.Ы: Дударь, где деньги за рекламу?)

Надеюсь, данный гайд поможет вам в разработке. Всем добра и кода без багов. С уважением, h4cktivist.

<br>
Тут был Антоша
<br>И тут он тоже был

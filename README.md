1. Установка:
Убедитесь, что у вас установлены необходимые зависимости:tkinter, pillow, imagehash, opencv-python, multiprocessing.
    1)Вы можете установить эти зависимости с помощью pip : pip install tkinter pillow imagehash opencv-python.
    2)Потом вы можете скачать как через git clone так и ZIP-архив.
Как скачать через git clone: https://github.com/dmitry-nikiforov-psu/Modsen-practice.git.
    3)Потом заходите через консоль в папку, куда вы скачали репазиторий  (cd you_repository).
    4)И прописываете python main.py.

2. Использование
   1.Запустите файл main.py.
   2.В приложении нажмите "Добавить папку" и выберите папки, в которых нужно искать дубликаты.
   3.Нажмите "Найти дубликаты". Приложение начнет сканировать выбранные папки и отображать найденные дубликаты.
   4.Дважды кликните на файл, чтобы увидеть все его дубликаты.
   5.Правый клик на файле, позволяет посмотреть полный путь к оригинальному файлу.

3. Структура проекта
    1)main.py: Основной файл приложения, содержит класс DuplicateFinderApp с GUI и логикой поиска дубликатов.
    2)duplicate_finder.py: Модуль с функциями для поиска дубликатов файлов.
    3)hash.py: Модуль с функциями для вычисления хешей файлов.
    4)multiprocessing_utils.py: Модуль с вспомогательными функциями для параллельной обработки.
4. Возможности
    1.Поиск дубликатов изображений.
    2.Параллельная обработка файлов для ускорения поиска.
    3.Отображение найденных дубликатов в древовидном представлении.
    4.Возможность просмотра дубликатов и оригинальных файлов.
    5.Логирование действий пользователя и процесса поиска.


   Автор: Dmitry Nikiforov (Polotsk State University).
   Version Python: 3.11.

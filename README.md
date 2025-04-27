# Homework 3
## Bohdan Ozarko

### Installation
<mark>```git clone https://github.com/Compi-Craft/software_architecture_1.git```</mark>

### Prerequisites
<mark>```pip install -r requirements.txt```</mark><br>
Also docker
### Usage

Run all services<br>
```docker compose up -d```<br>
```gunicorn -b 127.0.0.1:5001 logging_service:app```<br>
```gunicorn -b 127.0.0.1:5002 logging_service:app```<br>
```gunicorn -b 127.0.0.1:5003 logging_service:app```<br>
```python3 logging_service.py```<br>
```PORT=5004 python3 messages_service.py```<br>
```PORT=5005 python3 messages_service.py```<br>

1. Отримуємо три ноди hazelcast

![Example Image](images/image_1.png)

2. Отримуємо наступну конфігурацію Kafka
![Example Image](images/image_10.png)

1. Записуємо 9 повідомлень через fill_messages.py скрипт

![Example Image](images/image_2.png)

Отримуємо такий розподіл повідомлень у  message services

![Example Image](images/image_11.png)
![Example Image](images/image_12.png)

4. Зробимо get request, отримуємо набір повідомлень з випадково обраного message service
![Example Image](images/image_13.png)
### Перевірка відмовостійкості
1. Вимикаємо message services
![Example Image](images/image_14.png)
2. Надсилаємо 9 повідомлень
![Example Image](images/image_15.png)
![Example Image](images/image_16.png)
3. Вимикаємо одного з лідерів
![alt text](images/image.png)
4. Вмикаємо message service і дивимось чи зчитає
![alt text](images/image_17.png)
Перший запущений сервіс все зчитав і зберіг у пам'ять, отже реплікація працює
![alt text](images/image_18.png)
# Homework 4
## Bohdan Ozarko

### Installation
```git clone https://github.com/Compi-Craft/software_architecture_1.git```
```git checkout micro_consul```
### Prerequisites
<mark>DOCKER</mark><br>

### Usage

Run all services<br>
```chmod +x run.sh```<br>
```run.sh```<br>


1. Отримуємо набір контейнерів
![Example Image](images/image_1.png)

1. Список сервісів у consul<br>
![Example Image](images/image_2.png)
1. Записуємо 10 повідомлень через fill_messages.py скрипт<br>
![Example Image](images/image_3.png)

    Фасад сервіс<br>
    ![Example Image](images/image_4.png)

    Логи logging сервісів<br>
    ![Example Image](images/image_5.png)
    ![Example Image](images/image_6.png)
    ![Example Image](images/image_7.png)

    Розподіл між нодами hazelcast<br>
    ![Example Image](images/image_8.png)

    Логи messages сервісів<br>
    ![Example Image](images/image_9.png)

    GET запит<br>
    ![Example Image](images/image_10.png)

1. Вимкнемо два логінг сервіса та один месадж і запишемо повідомлення знову

    ```docker stop logging_service_1 logging_service_2 messages_service_1```

    ![Example Image](images/image_11.png)
    ![Example Image](images/image_12.png)
    ![Example Image](images/image_13.png)
    ![Example Image](images/image_14.png)

    Все працює як раніше

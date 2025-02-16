# Homework 1
## Bohdan Ozarko

### Installation
<mark>```git clone https://github.com/Compi-Craft/software_architecture_1.git```</mark>

### Prerequisites
<mark>```pip install -r requirements.txt```</mark>

### Usage

Run all services

```python3 facade_service.py```<br>
```python3 logging_service.py```<br>
```python3 messages_service.py```<br>

Post request to facade service

```curl -X POST http://localhost:5000/post -H "Content-Type: application/json" -d '{"msg": <your_message_here>}'```

![Example Image](images/example_1.png)

Logging service console

![Example Image](images/example_2.png)

Get request to facade service

![Example Image](images/example_3.png)

### Additional task: retry and deduplicate mechanisms

Retry mechanism if logging service is off for post request

![Example Image](images/example_5.png)

Facade service console

![Example Image](images/example_4.png)

Logging service console

![Example Image](images/example_8.png)

Retry mechanism if logging or messaging service is off for get request

![Example Image](images/example_6.png)

Facade service console

![Example Image](images/example_7.png)

Deduplicate protection for logging service example (we will use direct post request to logging service with existing uuid)

```curl -X POST http://localhost:5001/log -H "Content-Type: application/json" -d '{"id": "EXISTING_UUID", "msg": "message 5"}'```

![Example Image](images/example_9.png)
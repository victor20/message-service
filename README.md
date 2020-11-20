# Message Service

## Hur man kör applikationen:

1. Klona repot:
```
git clone https://github.com/victor20/message-service.git
```

2. Skapa en virtual environment. I root-mappen (message-service) kör:
```
python3 -m venv venv
```

3. Aktivera virtual environment. I root-mappen kör:
```
source venv/bin/activate
```

4. Installera requirements. I root-mappen kör: 
```
pip3 install -r requirements.txt
```

5. Starta applikationen. I root-mappen kör: 
```
python run.py
```

Kör tester (när run.py inte kör). I root-mappen kör: 
```
pytest
```

## Hur man använder applikationen:

1. För att kunna skicka meddelanden måste man först lägga till användare.
```
curl --location --request POST 'localhost:5000/api/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_name": "Victor10",
    "first_name": "Victor",
    "last_name": "Eriksson"
}'
```

```
curl --location --request POST 'localhost:5000/api/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_name": "Carl20",
    "first_name": "Carl",
    "last_name": "Eriksson"
}'
```

2. Skicka ett meddelande från Carl20 till Victor10.
```
curl --location --request POST 'localhost:5000/api/users/Carl20/messages' \
--header 'Content-Type: application/json' \
--data-raw '{
    "receiver": "Victor10",
    "message_text": "Hej"
}'
```

3. Hämta nya mottagna meddelanden. Servern håller reda på det högsta id:et som har hämtats av användaren genom anrop 3 eller 4.
```
curl --location --request GET 'localhost:5000/api/users/Victor10/messages/received/new'
```

4. Hämta tidsordnade meddelanden från ett start och stop index. Indexen är ordnings-index för en specifik användare (inte databas index) Meddelande nummer 1 är det senaste meddelandet som användaren mottagit. För att hämta Victor10s mottagna meddelanden från 1 till 3 körs:
```
curl --location --request GET 'localhost:5000/api/users/Victor10/messages/received?from=1&to=3'
```

För att hämta Carl20s skickade tidsordnade meddelanden från 1 till 3 körs:

```
curl --location --request GET 'localhost:5000/api/users/Carl20/messages/sent?from=1&to=3'
```

5. Radera meddelanden. Användaren kan radera meddelanden som denna har mottagit eller skickat genom att skicka en lista med meddelande-id. För att radera Victor10s mottagna meddelande med id 1 körs:
```
curl --location --request DELETE 'localhost:5000/api/users/Victor10/messages/received' \
--header 'Content-Type: application/json' \
--data-raw '{
    "messages": [1, 10]
}'
```

Vill man istället radera Carl20s skickade meddelande med id 1 körs:

```
curl --location --request DELETE 'localhost:5000/api/users/Carl20/messages/sent' \
--header 'Content-Type: application/json' \
--data-raw '{
    "messages": [1]
}'
```

## Övriga anrop
1. Hämta alla användare i databasen
```
curl --location --request GET 'localhost:5000/api/users'
```
2. Hämta alla meddelanden i databasen
```
curl --location --request GET 'localhost:5000/api/messages'
# Message Service

## Hur man kör applikationen:

1. Klona repot
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

4. Installera requirements. I rootmappen kör: 
```
pip3 install -r requirements.txt
```

5. Starta applikationen. I rootmappen kör: 
```
python run.py
```

Kör tester (när run.py inte kör). I rootmappen kör: 
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

4. Hämta tidsordnade meddelanden från ett start och stop index. Indexen är ordnings-index för en specifik användare (inte databas index) Meddelande nummer 1 är det första meddelandet som användaren mottagit sen registrering. För att hämta meddelande 1 till 3 körs:
```
curl --location --request GET 'localhost:5000/api/users/Victor10/messages/received?from=1&to=3'
```

5. Radera meddelanden. Användaren kan radera meddelande som denna har mottagit genom att skicka en lista med meddelande-id. För att radera meddelande 1 och 10 skickar man:
```
curl --location --request DELETE 'localhost:5000/api/users/Victor10/messages' \
--header 'Content-Type: application/json' \
--data-raw '{
    "messages": [1, 10]
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
```
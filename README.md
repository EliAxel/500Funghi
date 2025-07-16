# 500Funghi
Ricerca avanzata per il libro di Umberto Nonis "500 Funghi"

Installazione:
1. Clonare l'intero progetto in una cartella
2. Installare python ad una versione uguale o superiore alla 3.13
3. Installare pipenv
4. Eseguire da riga di comando nella stessa cartella contenente Pipfile e Pipfile.lock "pipenv install"
5. Eseguire "pipenv shell"
6. Successivamente se su Windows, digitare "cd .\funghi500\", altrimenti su Linux/GNU "cd ./funghi500/"
7. Andare a ./funghi500/urls.py e commentare sia delete_db() che init_db()
8. Digitare se su Windows "python.exe .\manage.py migrate" o se su Linux/GNU "python3 ./manage.py migrate"
9. Ritornare a ./funghi500/urls.py e decommentare sia #delete_db() che #init_db()
10. Infine digitare, se su Windows "python.exe .\manage.py runserver" o se su Linux/GNU "python3 ./manage.py runserver"
11. Sul browser, cercare nella barra degli indirizzi localhost:8000

AVVERTENZE:
1. Il programma non è stato fatto a fini di lucro
2. Non è ben protetto a lato server se non un minimo sindacale, l'importante è non tentare di forzare il sito con strumenti per la creazione di post fittizi.
3. Dovrebbe essere uno strumento da usare per fini personali come strumento da aggiungere al libro
4. Potrebbero esserci errori data la natura della rappresentazione dei dati o per svista mia
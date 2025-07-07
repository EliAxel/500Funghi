from main.models import Fungo, Valore, Mese
import json
def delete_db():
    Fungo.objects.all().delete()
    Valore.objects.all().delete()
    Mese.objects.all().delete()

def init_db():
    for i in range(1,101):
        Valore.objects.create(
            id=i
        )
    
    for i in range(1,13):
        Mese.objects.create(
            id=i
        )
    
    with open('static/json/dati.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data['funghi']:
        fungo = Fungo.objects.create(
            id=item['id'],
            diametroMIN=item['diametroMIN'],
            diametroMAX=item['diametroMAX'],
            altezzaMIN=item['altezzaMIN'],
            altezzaMAX=item['altezzaMAX'],
            altitudineMIN=item['altitudineMIN'],
            altitudineMAX=item['altitudineMAX']
        )
        fungo.mesi.set(item['mesi'])
        fungo.valori.set(item['valori'])
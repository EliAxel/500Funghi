from main.models import Fungo, Valore, Mese
import json
from django.core.exceptions import ValidationError

def delete_db():
    Fungo.objects.all().delete()
    Valore.objects.all().delete()
    Mese.objects.all().delete()

def validate_sequence(values, field_name, min_val, max_val):
    """
    Validate that values are:
    - in ascending order
    - non-duplicate
    - within min/max range
    - integers
    """
    if not values:
        raise ValidationError(f"{field_name} cannot be empty")
    
    # Check all items are integers
    if not all(isinstance(x, int) for x in values):
        raise ValidationError(f"{field_name} must contain only integers")
    
    # Check for duplicates
    if len(values) != len(set(values)):
        raise ValidationError(f"{field_name} contains duplicate values")
    
    # Check range
    if any(x < min_val or x > max_val for x in values):
        raise ValidationError(f"{field_name} values must be between {min_val} and {max_val}")
    
    # Check ascending order
    if values != sorted(values):
        raise ValidationError(f"{field_name} must be in ascending order")

def init_db():
    # Create Valore objects
    for i in range(1, 101):
        Valore.objects.create(id=i)
    
    # Create Mese objects
    for i in range(1, 13):
        Mese.objects.create(id=i)
    
    with open('static/json/dati.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data['funghi']:
        try:
            # Validate mesi
            validate_sequence(item['mesi'], 'mesi', 1, 12)
            
            # Validate valori
            validate_sequence(item['valori'], 'valori', 1, 100)
            
            # Create the Fungo object
            fungo = Fungo.objects.create(
                id=item['id'],
                diametroMIN=item['diametroMIN'],
                diametroMAX=item['diametroMAX'],
                altezzaMIN=item['altezzaMIN'],
                altezzaMAX=item['altezzaMAX'],
                altitudineMIN=item['altitudineMIN'],
                altitudineMAX=item['altitudineMAX']
            )
            
            # Set many-to-many relationships
            fungo.mesi.set(item['mesi'])
            fungo.valori.set(item['valori'])
            
        except (ValidationError, KeyError) as e:
            # Include the ID in the error message
            error_id = item.get('id', 'UNKNOWN')
            raise ValidationError(f"Error in fungo ID {error_id}: {str(e)}") from e
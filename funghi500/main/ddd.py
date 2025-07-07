template = """
        {{
            "id": {id},
            "diametroMIN": 10,
            "diametroMAX": 20,
            "altezzaMIN": 30,
            "altezzaMAX": 40,
            "altitudineMIN": 500,
            "altitudineMAX": 600,
            "mesi": [10,11,12],
            "valori": [50,60,70]
        }},"""

with open('output.json', 'w') as file:
    file.write(
"""{
    "funghi": [""")
    for i in range(1, 500):
        file.write(template.format(id=i))
    file.write("""
        {
            "id": 500,
            "diametroMIN": 10,
            "diametroMAX": 20,
            "altezzaMIN": 30,
            "altezzaMAX": 40,
            "altitudineMIN": 500,
            "altitudineMAX": 600,
            "mesi": [10,11,12],
            "valori": [50,60,70]
        }
    ]
}""")
print("File 'output.json' creato con successo!")
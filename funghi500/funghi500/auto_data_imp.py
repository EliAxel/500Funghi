template = """
        {{
            "id": {id},
            "diametroMIN": ,
            "diametroMAX": ,
            "altezzaMIN": ,
            "altezzaMAX": ,
            "altitudineMIN": 0,
            "altitudineMAX": 00,
            "mesi": [10,11],
            "valori": []
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
            "diametroMIN": ,
            "diametroMAX": ,
            "altezzaMIN": ,
            "altezzaMAX": ,
            "altitudineMIN": 0,
            "altitudineMAX": 00,
            "mesi": [10,11],
            "valori": []
        }
    ]
}""")
print("File 'output.json' creato con successo!")
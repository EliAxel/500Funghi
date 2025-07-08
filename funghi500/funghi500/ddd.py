template = """
        {{
            "id": {id},
            "diametroMIN": ,
            "diametroMAX": ,
            "altezzaMIN": ,
            "altezzaMAX": ,
            "altitudineMIN": ,
            "altitudineMAX": ,
            "mesi": [],
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
            "altitudineMIN": ,
            "altitudineMAX": ,
            "mesi": [],
            "valori": []
        }
    ]
}""")
print("File 'output.json' creato con successo!")
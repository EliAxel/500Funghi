template = """
        {{
            "id": {id},
            "diametroMIN": XX,
            "diametroMAX": XX,
            "altezzaMIN": XX,
            "altezzaMAX": XX,
            "altitudineMIN": XXX,
            "altitudineMAX": XXX,
            "mesi": [XX,XX,XX],
            "valori": [XX,XX,XX]
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
            "diametroMIN": XX,
            "diametroMAX": XX,
            "altezzaMIN": XX,
            "altezzaMAX": XX,
            "altitudineMIN": XXX,
            "altitudineMAX": XXX,
            "mesi": [XX,XX,XX],
            "valori": [XX,XX,XX]
        }
    ]
}""")
print("File 'output.json' creato con successo!")
import os
import csv

base_dir = "C:/Users/Natalia/Desktop/PADIA/endansys/dataset/training"
output_csv = "etiquetas_animales.csv"

with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["filename", "species", "status"])

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        status = 1 if "peligro" in folder_name.lower() else 0
        species = folder_name.lower().replace("_peligro", "").replace("_", " ").strip()

        for img_file in os.listdir(folder_path):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(folder_path, img_file)
                writer.writerow([img_path.replace("\\", "/"), species, status])

print(f"CSV creado: {output_csv}")
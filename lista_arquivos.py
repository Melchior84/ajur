import os
import shutil
import re

def process_pdfs(source_folder, destination_folder):
    # Cria a pasta de destino se ela não existir
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Lista todos os arquivos na pasta de origem
    files = os.listdir(source_folder)

    # Processa cada arquivo
    for file in files:
        # Verifica se o arquivo é um PDF
        if file.endswith('.pdf'):
            # Extrai o número do processo do nome do arquivo usando regex
            match = re.search(r'\d+', file)
            if match:
                process_number = match.group(0)
                new_file_name = f"process_{process_number}.pdf"
                source_file_path = os.path.join(source_folder, file)
                destination_file_path = os.path.join(destination_folder, new_file_name)
                
                # Renomeia e move o arquivo para a pasta de destino
                shutil.move(source_file_path, destination_file_path)
                print(f"Renamed and moved: {file} -> {new_file_name}")

# Define as pastas de origem e destino
source_folder = "source_pdfs"
destination_folder = "processed_pdfs"

# Chama a função para processar os PDFs
process_pdfs(source_folder, destination_folder)
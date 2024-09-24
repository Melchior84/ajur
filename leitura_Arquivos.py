import os
import shutil

def rename_and_move_pdfs(source_dir, dest_dir, new_names):
    # List all files in the source directory
    files = os.listdir(source_dir)
    
    # Filter out PDF files
    pdf_files = [file for file in files if file.lower().endswith('.pdf')]
    
    # Check if the number of new names matches the number of PDF files
    if len(new_names) != len(pdf_files):
        raise ValueError("O número de novos nomes não corresponde ao número de arquivos PDF.")
    
    # Rename and move each PDF file
    for i, pdf_file in enumerate(pdf_files):
        new_name = new_names[i] + '.pdf'
        source_path = os.path.join(source_dir, pdf_file)
        dest_path = os.path.join(dest_dir, new_name)
        
        # Move and rename the file
        shutil.move(source_path, dest_path)
        print(f"Renomeado e movido: {pdf_file} -> {new_name}")

# Exemplo de uso
source_directory = os.path.expanduser('~/Downloads')
destination_directory = os.path.expanduser('~/Documents/RenamedPDFs')
new_file_names = ['Documento1', 'Documento2', 'Documento3']  # Lista de novos nomes

# Cria o diretório de destino se não existir
os.makedirs(destination_directory, exist_ok=True)

# Chama a função para renomear e mover arquivos PDF
rename_and_move_pdfs(source_directory, destination_directory, new_file_names)

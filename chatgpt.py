import PyPDF2 
from gensim.summarization import summarize

def ler_pdf(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text()
    return texto

def resumir_texto(texto):
    try:
        resumo = summarize(texto, ratio=0.2)  # Ajuste a razão conforme necessário
        return resumo
    except ValueError:
        return "Texto muito curto para resumir."

def main():
    caminho_arquivo = 'seu_arquivo.pdf'  # Substitua pelo caminho do seu arquivo PDF
    texto = ler_pdf(caminho_arquivo)
    resumo = resumir_texto(texto)
    print("Resumo do PDF:")
    print(resumo)

if __name__ == "__main__":
    main()

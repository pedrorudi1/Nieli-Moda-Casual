from PIL import Image

def converter_ico_para_png(caminho_ico, caminho_png):
    """
    Converte um arquivo ICO para PNG.

    Args:
        caminho_ico (str): Caminho para o arquivo ICO.
        caminho_png (str): Caminho para salvar o arquivo PNG.
    """
    try:
        imagem = Image.open(caminho_ico)
        imagem.save(caminho_png, "PNG")
        print(f"Conversão concluída: {caminho_ico} -> {caminho_png}")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_ico}")
    except Exception as e:
        print(f"Erro durante a conversão: {e}")

# Exemplo de utilização:
caminho_ico = "/home/pedro/Projetos/Nieli-Moda-Casual/Assets/icone.ico"
caminho_png = "/home/pedro/Projetos/Nieli-Moda-Casual/Assets/icone.png"

converter_ico_para_png(caminho_ico, caminho_png)
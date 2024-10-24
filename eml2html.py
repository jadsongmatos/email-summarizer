from email import policy
from email.parser import BytesParser

def eml_para_html(caminho_eml, caminho_html):
    # Abrir e ler o arquivo EML em modo binário
    with open(caminho_eml, 'rb') as arquivo_eml:
        msg = BytesParser(policy=policy.default).parse(arquivo_eml)

    # Inicializar variável para armazenar o conteúdo HTML
    html = None

    # Verificar se o e-mail é multipart
    if msg.is_multipart():
        # Iterar sobre as partes do e-mail
        for parte in msg.iter_parts():
            # Verificar se a parte é do tipo texto/html
            if parte.get_content_type() == 'text/html':
                html = parte.get_content()
                break
    else:
        # Se não for multipart, verificar o tipo de conteúdo
        if msg.get_content_type() == 'text/html':
            html = msg.get_content()

    # Se encontrou conteúdo HTML, salvar no arquivo
    if html:
        with open(caminho_html, 'w', encoding='utf-8') as arquivo_html:
            arquivo_html.write(html)
        print(f"Conversão concluída. Arquivo HTML salvo em: {caminho_html}")
    else:
        # Caso não encontre HTML, tentar converter texto simples para HTML
        if msg.is_multipart():
            for parte in msg.iter_parts():
                if parte.get_content_type() == 'text/plain':
                    texto = parte.get_content()
                    break
        else:
            if msg.get_content_type() == 'text/plain':
                texto = msg.get_content()
            else:
                texto = None

        if texto:
            # Simples conversão de texto para HTML
            html_convertido = f"<html><body><pre>{texto}</pre></body></html>"
            with open(caminho_html, 'w', encoding='utf-8') as arquivo_html:
                arquivo_html.write(html_convertido)
            print(f"Conversão de texto simples para HTML concluída. Arquivo salvo em: {caminho_html}")
        else:
            print("Nenhum conteúdo HTML ou texto encontrado para converter.")

# Exemplo de uso
caminho_do_eml = 'exemplo.eml'
caminho_do_html = 'resultado.html'

eml_para_html(caminho_do_eml, caminho_do_html)

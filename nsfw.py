import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

imagens_retornadas = {
    "yandere": set(),
    "curvy": set(),
    "anime": set(),
    "breasts": set(),
    "bdsm": set(),
    "loli": set(),
    "funamusea": set(),
    "mogeko_castle": set(),
    "doki_doki_literature_club": set(),
    "zettai": set()
}

def buscar_imagens(tag):
    url = f"https://rule34.xxx/index.php?page=post&s=list&tags={tag}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    resposta = requests.get(url, headers=headers)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.content, "html.parser")
        imagens = soup.find_all("span", class_="thumb")
        
        lista_imagens = []
        for img in imagens:
            link_imagem = img.find("a")["href"]
            post_url = f"https://rule34.xxx/{link_imagem}"
            
            post_resposta = requests.get(post_url, headers=headers)
            if post_resposta.status_code == 200:
                post_soup = BeautifulSoup(post_resposta.content, "html.parser")
                imagem_direta = post_soup.find("img", id="image")
                if imagem_direta:  
                    lista_imagens.append(imagem_direta["src"])

        return lista_imagens
    else:
        return []  

@app.route('/')
def home():
    return "Servidor Flask NSFW rodando!"

@app.route('/imagem-yandere')
def imagem_yandere():
    return buscar_imagem_por_tag("yandere")

@app.route('/imagem-bdsm')
def imagem_bdsm():
    return buscar_imagem_por_tag("bdsm")

@app.route('/imagem-loli')
def imagem_loli():
    return buscar_imagem_por_tag("loli")

@app.route('/imagem-zettai')
def imagem_zettai():
    return buscar_imagem_por_tag("zettai")

@app.route('/imagem-funamusea')
def imagem_funamusea():
    return buscar_imagem_por_tag("funamusea")

@app.route('/imagem_doki_doki_literature_club')
def imagem_doki_doki():
    return buscar_imagem_por_tag("doki_doki_literature_club")

@app.route('/mogeko_castle')
def imagem_mogeko_castle():
    return buscar_imagem_por_tag("mogeko_castle")

@app.route('/imagem-curvy')
def imagem_curvy():
    return buscar_imagem_por_tag("curvy")

@app.route('/imagem-aleatoria')
def imagem_aleatoria():
    todas_as_tags = list(imagens_retornadas.keys())
    tag_aleatoria = random.choice(todas_as_tags)
    return buscar_imagem_por_tag(tag_aleatoria)

def buscar_imagem_por_tag(tag):
    imagens = buscar_imagens(tag)

    if imagens:
        imagens_filtradas = [img for img in imagens if img not in imagens_retornadas[tag]]

        if not imagens_filtradas:
            return jsonify({"mensagem": "Todas as imagens já foram retornadas.", "tag_usada": tag}), 404

        url_imagem = random.choice(imagens_filtradas)

        imagens_retornadas[tag].add(url_imagem)

        return jsonify({"imagem": url_imagem, "tag_usada": tag, "status": "sucesso"}), 200
    else:
        return jsonify({"mensagem": "Nenhuma imagem encontrada.", "tag_usada": tag}), 404

@app.route('/imagem-aleatoria-geral')
def imagem_aleatoria_geral():
    todas_as_tags = list(imagens_retornadas.keys())
    tag_aleatoria = random.choice(todas_as_tags)
    
    imagens = buscar_imagens(tag_aleatoria)

    if imagens:
        imagens_filtradas = [img for img in imagens if img not in imagens_retornadas[tag_aleatoria]]

        if not imagens_filtradas:
            return jsonify({"mensagem": "Todas as imagens já foram retornadas.", "tag_usada": tag_aleatoria}), 404

        url_imagem = random.choice(imagens_filtradas)

        imagens_retornadas[tag_aleatoria].add(url_imagem)

        return jsonify({"imagem": url_imagem, "tag_usada": tag_aleatoria, "status": "sucesso"}), 200
    else:
        return jsonify({"mensagem": "Nenhuma imagem encontrada.", "tag_usada": tag_aleatoria}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)

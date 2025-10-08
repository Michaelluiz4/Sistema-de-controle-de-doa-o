from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os

# configuração
app = Flask(__name__)
DB_NAME = "donations.db" # nome do banco de dados

def init_db():
    # função para inicializar o banco de dados.
    if not os.path.exists(DB_NAME): # se o banco de dado não existir, ele irá ser criado.
        conn = sqlite3.connect(DB_NAME) # conectar ao banco de dados.
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        conn.commit() # salvar dados.
        conn.close() # fechar banco de dados.


@app.route("/")
def home():
    # rota inicial, responsável por exibir o resumo das doações.
    conn = sqlite3.connect(DB_NAME) # conectar ao banco de dados.
    cursor = conn.cursor() # criar cursor.

    # exibição dos dados por cada produto cadastrado.
    cursor.execute("SELECT item, SUM(quantidade) FROM donations GROUP BY item")
    products = cursor.fetchall()

    # exibição dos dados por cada categoria cadastrada. 
    cursor.execute("SELECT tipo, SUM(quantidade) FROM donations GROUP BY tipo")
    categorias = cursor.fetchall()

    conn.close() # fechar conexão com o banco de dados.

    labels_produtos = [row[0] for row in products] # extrai os nomes dos produtos da consulta.
    valores_produtos = [row[1] for row in products] # extrai a quantidade total de cada produtos.

    labels_categorias = [row[0] for row in categorias] # extrai os nomes das categorias da consulta.
    valores_categorias = [row[1] for row in categorias] # extrai as quantidades totais de cada categoria.

    return render_template(
        "index.html",
        labels_produtos=labels_produtos,
        valores_produtos=valores_produtos,
        labels_categorias=labels_categorias,
        valores_categorias=valores_categorias
    ) # renderiza a página inicial com os dados de produtos e categorias paara exibição.


@app.route("/register_donate", methods=["GET", "POST"])
def register_donate():
    # Página de registro de doações
    if request.method == "POST":
        # verifica se a requisição é do tipo POST. 
        item = request.form["item"].strip().capitalize()
        quantidade = int(request.form["quantidade"])
        tipo = request.form["tipo"]

        conn = sqlite3.connect(DB_NAME) # conecta ao banco de dados.
        cursor = conn.cursor()

        # verifica se já existe o mesmo item e tipo no banco de dados.
        cursor.execute("""
            SELECT quantidade FROM donations 
            WHERE item = ? AND tipo = ?
        """, (item, tipo))
        result = cursor.fetchone() # retorna o primeiro resultado correspondente ou None

        if result:
            # se já existir o item no banco de dados, soma a quantidade de itens.
            nova_quantidade = result[0] + quantidade
            cursor.execute("""
                UPDATE donations
                SET quantidade = ?
                WHERE item = ? AND tipo = ?
            """, (nova_quantidade, item, tipo))
        else:
            # caso não exista o item no banco de dados, o item é inserido.
            from datetime import datetime
            data = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO donations (item, quantidade, tipo, data)
                VALUES (?, ?, ?, ?)
            """, (item, quantidade, tipo, data))

        conn.commit() # salva as alterações no banco de dados.
        conn.close() # fechar conexão com o banco de dados.

        return redirect(url_for("donations")) # redireciona para a página donations

    return render_template("register_donate.html") # renderiza a página register_donate.html


@app.route("/donations")
def donations():
    # função responsável por listar doações registradas.
    conn = sqlite3.connect(DB_NAME) # realiza a conexão com o banco de dados.
    cursor = conn.cursor() # criar um cursor para comandos SQL.
    cursor.execute("SELECT item, quantidade, tipo, data FROM donations") # realiza a consulta no banco de dados
    donations_list = cursor.fetchall() # recupera todos os resultados de uma consulta SQL.
    conn.close() # fechar conexão com o banco de dados.

    # transforma os dados em lista de dicionários para facilitar o uso no template HTML.
    donations_data = [
        {
            "item": d[0], 
            "quantidade": d[1], 
            "tipo": d[2], 
            "data": datetime.strptime(d[3], "%Y-%m-%d").strftime("%d/%m/%Y")
        }
        for d in donations_list
    ]

    return render_template("donations.html", donations=donations_data) # renderiza a página donations.html


@app.route("/reset_all", methods=["POST"])
def reset_all():
    # resetar todos os registros salvos no banco de dados.
    conn = sqlite3.connect(DB_NAME) # conectar ao banco de dados.
    cursor = conn.cursor() # criar um cursor.
    cursor.execute("DELETE FROM donations") # executar o comando delete no banco de dados
    conn.commit() # salvar alterações feitas.
    conn.close() # fechar conexão com o banco de dados.
    return redirect(url_for("donations")) # redirecionar a página para donations.


@app.route("/reset_category", methods=["POST"])
def reset_category():
    # função para apagar dados de uma categoria específica.
    categoria = request.form["categoria"] # selecionar a categoria
    conn = sqlite3.connect(DB_NAME) # conectar ao banco de dados.
    cursor = conn.cursor() # criar cursor.
    cursor.execute("DELETE FROM donations WHERE tipo = ?", (categoria,)) # deletar item de uma categoria específica.
    conn.commit() # salvar alterações.
    conn.close() # fechar conexão com o banco de dados.
    return redirect(url_for("donations")) # redirecionar para a página donations


if __name__ == "__main__":
    # garante que o app será executado apenas se esse for o arquivo principal.
    init_db() # inicializa o banco de dados.
    app.run(debug=True) # inicializando o servidor Flask.

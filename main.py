from flask import Flask, render_template, request, redirect, session, flash, url_for
import json
import datetime
import os

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self,  nome, nickname, senha):
        self.nome = nome
        self.senha = senha
        self.nickname = nickname



jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Sonic', 'Rpg', 'Ps2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'Ps2')

usuario1 = Usuario('Eduardo', 'Boldy', '123')
usuario2 = Usuario('Bruno', 'BD', 'alohomora')
usuario3 = Usuario('Lay', 'Devil', '321')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3}

lista = [jogo1, jogo2, jogo3]
app = Flask(__name__)
app.secret_key = 'jorge'


@app.route('/')
def index():
    return render_template('lista.html', titulo='jogos', jogos=lista)

@app.route('/novo')
def novo():
    # Possibilidade pegar a sessão tbm 'if usuario_logado' not in session:
    if session.get('logado'):
        return render_template('adicionar.html', titulo='Novo jogo')
    else:
        flash("Acesso negado. Faça o login primeiro.", "error")
        return redirect(url_for('login', proxima=url_for('novo')))

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        if request.form['senha'] == usuarios[request.form['usuario']].senha:
            flash(usuarios[request.form['usuario']].nome + ' Logado com sucesso!')
            proxima_pagina = request.form['proxima']
            session['logado'] = True
            if proxima_pagina == 'None':
                return redirect(url_for('index'))
            elif proxima_pagina and proxima_pagina != 'None':
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('index'))
    else:
        path = os.getcwd()
        URL = os.path.join(path, 'log.json')
        try:
            with open(URL, 'r') as file:
                dados = json.load(file)
        except FileNotFoundError:
            dados = {'logs_de_acesso': []}
        except json.decoder.JSONDecodeError:
            dados = {
                "logs_de_acesso": []
            }
        novo_log = {
            'Data/Hora': f'{datetime.datetime.now()}',
            'Erro': 'Senha ou Usuário inválido',
            'Usuario': session.get('usuario_logado')
        }
        dados['logs_de_acesso'].append(novo_log)
        with open(URL, 'w') as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
        flash('login ou senha invalido, tente novamente.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session['logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)

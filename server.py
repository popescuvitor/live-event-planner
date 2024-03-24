from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('eventos.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS eventos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome TEXT,
              dia TEXT,
              start TEXT,
              fim TEXT,
              local TEXT,
              pretende_participar INTEGER)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    dia = request.form['dia']
    hora_inicio = request.form['inicio']  
    hora_fim = request.form['fim']
    local = request.form['local']
    
    # Verificar se o checkbox foi marcado
    pretende_participar = 1 if 'pretende_participar' in request.form else 0

    # Formatando data e hora para o formato necessário
    start = f"{dia}T{hora_inicio}:00"
    fim = f"{dia}T{hora_fim}:00"

    # Insere os dados na tabela SQLite
    c.execute("INSERT INTO eventos (nome, dia, start, fim, local, pretende_participar) VALUES (?, ?, ?, ?, ?, ?)", (nome, dia, start, fim, local, pretende_participar))
    conn.commit()

    return redirect('/')


@app.route('/eventos')
def eventos():
    # Conectar-se ao banco de dados SQLite
    conn = sqlite3.connect('eventos.db')
    c = conn.cursor()

    # Buscar os dados dos eventos
    c.execute("SELECT * FROM eventos")
    eventos = c.fetchall()

    # Ordenar os eventos por hora de início
    eventos.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%dT%H:%M:%S'))

    # Fechar a conexão com o banco de dados
    conn.close()

    # Renderizar o template com os dados dos eventos
    return render_template('eventos.html', eventos=eventos)

if __name__ == '__main__':
    # Defina o endereço e a porta desejados
    endereco = '0.0.0.0'  # Para tornar o servidor acessível em todas as interfaces de rede
    porta = 10000  # Porta padrão do Flask
    
    # Inicie o aplicativo Flask
    app.run(host=endereco, port=porta, debug=True)
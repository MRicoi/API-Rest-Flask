# Grupo: Marcos Kayser, Matheus Ricoi, Pedro Bastos e Vittor Brittis
# Turma: 10
# Entrega: 05/05

# imports
import pandas as pd
from flask import Flask, request, abort, make_response, jsonify

# Tarefa 1 – Criação de uma API Rest (70%)
# Dataset = https://www.kaggle.com/code/nitindatta/students-performance-in-exams-eda-in-depth/input

bd = pd.read_csv("StudentsPerformance.csv")

app = Flask(__name__)

# Nao precisa, mas metodo para pegar todos os estudantes
# Inserir
@app.route('/estudantes', methods=['GET', 'POST'])
def estudantes():
    global bd

    if request.method == 'GET':
        return make_response(jsonify(bd.to_dict(orient='records')))
    elif request.method == 'POST': # Colocar que precisa ter todos os campos e oque precisa ser cada resposta
        dados = request.get_json()
        novo = pd.DataFrame([dados])
        bd = pd.concat([bd, novo], ignore_index=True)
        return make_response(jsonify("Estudante inserido com sucesso!"), 200)
    else:
        abort(404)

# Inserir, Atualizar e Deletar.


if __name__ == "__main__":
    app.run(debug=True)
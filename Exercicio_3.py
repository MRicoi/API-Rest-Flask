# Grupo: Davi Alcantara, Matheus Ricoi e Pedro Bastos
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
    
    elif request.method == 'POST':
        dados = request.get_json()
        colunas_invalidas = [col for col in dados.keys() if col not in bd.columns]
        if colunas_invalidas:
            return make_response(jsonify(f"Colunas inválidas: {colunas_invalidas}"), 400)
        novo = pd.DataFrame([dados])
        bd = pd.concat([bd, novo], ignore_index=True)
        return make_response(jsonify("Estudante inserido com sucesso!"), 200)
    
    else:
        abort(404)



# Ver, Atualizar e Deletar
@app.route('/estudante/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def estudante(id):
    global bd

    if id < 0 or id >= len(bd):
        return make_response(jsonify("Id nao existe"), 400)
    
    else:
        if request.method == "GET":
            return make_response(jsonify(bd.iloc[id].to_dict()), 200)
        
        elif request.method == "PUT":
            dados = request.get_json()
            colunas_invalidas = [col for col in dados.keys() if col not in bd.columns]
            if colunas_invalidas:
                return make_response(jsonify(f"Colunas inválidas: {colunas_invalidas}"), 400)
            for coluna, valor in dados.items():
                bd.at[id, coluna] = valor
                return make_response(jsonify("Estudante atualizado com sucesso!"), 200)
            
        elif request.method == "DELETE":
            bd.drop(index=id, inplace=True)
            bd.reset_index(drop=True, inplace=True) # Na duvida se deixa ou arruma os index
            return make_response(jsonify("Estudante removido com sucesso!"), 200)
        else:
            abort(400)



# Consulta: Devem ser implementados tres tipos de consulta
# Retornar os n primeiros elementos do dataset
@app.route('/estudantes/n/<int:n>', methods=['GET'])
def get_n_primeiros(n):
    global bd

    return make_response(jsonify(bd.head(n).to_dict(orient='records')), 200)

# consulta que que receba um dos campos string do dataset (o grupo pode definir
# qual o campo) como parâmetro e retorna somente os dados que possuem valor
# do campo escolhido igual ao valor informado
# localhost:5000/<endpoint>/João da Silva → retorna somente as linhas onde
# campo é igual a João da Silva
@app.route('/estudantes/gender/<valor>', methods=['GET'])
def get_por_genero(valor):
    global bd

    filtrado = bd[bd['gender'].str.lower() == valor.lower()]
    return make_response(jsonify(filtrado.to_dict(orient='records')), 200)

# uma consulta que recebe um json que permita filtrar por mais de um campo
# do dataset ao mesmo tempo. Os campos não devem ser fixos, ou seja, deve ser
# possível fazer a consulta por quaisquer campos desejados.
@app.route('/estudantes/filtros', methods=['POST'])
def consulta_filtros():
    global bd

    filtros = request.get_json()
    df_filtrado = bd.copy()

    for campo, valor in filtros.items():
        if campo not in bd.columns:
            return make_response(jsonify("Campo '{campo}' nao existe no dataset."), 400)
        df_filtrado = df_filtrado[df_filtrado[campo] == valor]
    return make_response(jsonify(df_filtrado.to_dict(orient='records')), 200)

if __name__ == "__main__":
    app.run(debug=True)

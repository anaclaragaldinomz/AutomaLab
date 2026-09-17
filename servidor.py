import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

from organizador import organizar
from backup import fazer_backup
from monitor import monitorar
from faxineiro import limpar
from relatorios import gerar_relatorio

app = Flask(__name__, static_folder=".", static_url_path="")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")

def registrar_log(mensagem):
    os.makedirs(LOG_DIR, exist_ok=True)
    arquivo = os.path.join(LOG_DIR, f"automalab_{datetime.now():%Y%m%d}.log")
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {mensagem}\n")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/executar/<modulo>", methods=["POST"])
def executar(modulo):
    dados = request.get_json(force=True) or {}
    linhas = []

    def logger(msg):
        linhas.append(msg)
        registrar_log(msg)

    try:
        if modulo == "organizador":
            resultado = organizar(
                origem=dados.get("origem", ""),
                destino=dados.get("destino", ""),
                modo=dados.get("modo", "mover"),
                simular=bool(dados.get("simular", True)),
                logger=logger,
            )
            resumo = f"{resultado['total']} arquivo(s) processado(s)."

        elif modulo == "backup":
            resultado = fazer_backup(
                origem=dados.get("origem", ""),
                destino=dados.get("destino", ""),
                extensoes=dados.get("extensoes", ""),
                simular=bool(dados.get("simular", True)),
                logger=logger,
            )
            resumo = f"{resultado['copiados']} copiado(s), {resultado['ignorados']} ignorado(s)."

        elif modulo == "monitor":
            monitorar(caminho_disco=dados.get("disco", "C:/"), logger=logger)
            resumo = "Relatorio do sistema gerado."

        elif modulo == "faxineiro":
            resultado = limpar(
                pasta=dados.get("pasta", ""),
                dias_antigos=int(dados.get("dias", 30)),
                extensoes=dados.get("extensoes", ""),
                simular=bool(dados.get("simular", True)),
                logger=logger,
            )
            resumo = f"{resultado['apagados']} arquivo(s) apagado(s)."

        elif modulo == "relatorios":
            resultado = gerar_relatorio(
                pasta_logs=LOG_DIR,
                arquivo_saida=dados.get("saida", ""),
                logger=logger,
            )
            resumo = f"{resultado['total_linhas']} linha(s) analisada(s)."

        else:
            return jsonify({"sucesso": False, "log": "Modulo desconhecido."})

        registrar_log(f"RESULTADO [{modulo}]: {resumo}")
        return jsonify({"sucesso": True, "log": "\n".join(linhas), "resumo": resumo})

    except FileNotFoundError as erro:
        registrar_log(f"ERRO: {erro}")
        return jsonify({
            "sucesso": False,
            "log": "Uma das pastas informadas nao foi encontrada. Confira o caminho e tente de novo.",
        })
    except PermissionError as erro:
        registrar_log(f"ERRO: {erro}")
        return jsonify({
            "sucesso": False,
            "log": str(erro),
        })
    except Exception as erro:
        registrar_log(f"ERRO INESPERADO: {erro}")
        return jsonify({
            "sucesso": False,
            "log": "Ocorreu um erro inesperado. Veja o arquivo de log para mais detalhes.",
        })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
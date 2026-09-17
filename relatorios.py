from datetime import datetime
from pathlib import Path

MODULOS = {
    "MOVIDO": "Organizador",
    "SIMULACAO": "Simulacoes",
    "COPIADO": "Backup",
    "APAGADO": "Faxineiro",
    "IGNORADO": "Ignorados",
    "ERRO": "Erros",
}

def gerar_relatorio(pasta_logs, arquivo_saida="", logger=print):
    pasta = Path(pasta_logs)

    if not pasta.exists():
        raise FileNotFoundError("A pasta de logs nao foi encontrada.")

    arquivos = sorted(pasta.glob("*.log")) + sorted(pasta.glob("*.txt"))

    if not arquivos:
        logger("Nenhum log encontrado para consolidar.")
        return {"total_linhas": 0, "contagem": {}}

    contagem = {v: 0 for v in MODULOS.values()}
    total_linhas = 0
    detalhes = []

    for arq in arquivos:
        linhas = arq.read_text(encoding="utf-8", errors="ignore").splitlines()
        total_linhas += len(linhas)
        detalhes.append(f"- {arq.name}: {len(linhas)} linha(s)")

        for linha in linhas:
            linha_maiuscula = linha.upper()
            for chave, nome in MODULOS.items():
                if chave in linha_maiuscula:
                    contagem[nome] += 1
                    break

    logger("======== RELATORIO CONSOLIDADO ========")
    logger(f"Gerado em: {datetime.now():%d/%m/%Y %H:%M}")
    logger(f"Arquivos analisados: {len(arquivos)}")
    logger(f"Total de linhas: {total_linhas}")
    logger("Arquivos:")
    for d in detalhes:
        logger("  " + d)
    logger("Resumo por tipo:")
    for nome, qtd in contagem.items():
        logger(f"  {nome}: {qtd}")
    logger("======================================")

    if arquivo_saida:
        caminho = Path(arquivo_saida)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        conteudo = [f"RELATORIO CONSOLIDADO - {datetime.now():%d/%m/%Y %H:%M}", ""]
        conteudo += detalhes + ["", "Resumo por tipo:"]
        conteudo += [f"{nome}: {qtd}" for nome, qtd in contagem.items()]
        caminho.write_text("\n".join(conteudo), encoding="utf-8")
        logger(f"Relatorio salvo em: {caminho}")

    return {"total_linhas": total_linhas, "contagem": contagem}
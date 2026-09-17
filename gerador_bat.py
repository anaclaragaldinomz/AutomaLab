import subprocess
from datetime import datetime
from pathlib import Path

def _salvar(nome, conteudo):
    caminho = Path("C:/Users/USUARIO/AutomaLabTeste/bats") / nome
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="latin-1")
    return caminho

def gerar_bat(modulo, grupo, **params):
    data = datetime.now().strftime("%Y%m%d")
    nome = f"automalab_grupo{grupo}_{modulo}_{data}.bat"

    if modulo == "organizador":
        conteudo = f"""@echo off
setlocal
set "ORIGEM={params.get('origem', '')}"
set "DESTINO={params.get('destino', '')}"
if not exist "%ORIGEM%" ( echo ERRO: origem inexistente. & exit /b 1 )
for %%C in (imagens documentos videos musicas compactados outros) do if not exist "%DESTINO%\%%C" mkdir "%DESTINO%\%%C"
for %%E in (jpg png pdf txt mp4 zip) do if exist "%ORIGEM%\*.%%E" move /Y "%ORIGEM%\*.%%E" "%DESTINO%\documentos\" >nul 2>&1
echo Organizacao concluida.
exit /b 0
"""

    elif modulo == "backup":
        conteudo = f"""@echo off
setlocal
set "ORIGEM={params.get('origem', '')}"
set "DESTINO={params.get('destino', '')}"
if not exist "%ORIGEM%" ( echo ERRO: origem inexistente. & exit /b 1 )
if not exist "%DESTINO%" mkdir "%DESTINO%"
xcopy "%ORIGEM%" "%DESTINO%" /E /I /Y /D >nul
echo Backup concluido.
exit /b 0
"""

    elif modulo == "monitor":
        conteudo = """@echo off
setlocal
echo === RELATORIO DO SISTEMA ===
echo --- Disco ---
wmic logicaldisk get size,freespace,caption
echo --- Memoria ---
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value
echo --- Processos ---
tasklist /FO TABLE
exit /b 0
"""

    elif modulo == "faxineiro":
        conteudo = f"""@echo off
setlocal
set "PASTA={params.get('pasta', 'C:\Users\USUARIO\AutomaLabTeste\temporarios')}"
if not exist "%PASTA%" ( echo ERRO: pasta inexistente. & exit /b 1 )
forfiles /P "%PASTA%" /S /M *.* /D -{params.get('dias', 30)} /C "cmd /c del /Q @path" >nul 2>&1
echo Limpeza concluida.
exit /b 0
"""

    else:
        conteudo = """@echo off
setlocal
set "LOGS=%~dp0logs"
set "SAIDA=%LOGS%\relatorio_consolidado.txt"
if not exist "%LOGS%" ( echo ERRO: pasta de logs inexistente. & exit /b 1 )
echo RELATORIO CONSOLIDADO > "%SAIDA%"
for %%F in ("%LOGS%\*.log") do (
    echo --- %%~nxF --- >> "%SAIDA%"
    type "%%F" >> "%SAIDA%"
)
echo Relatorio gerado em %SAIDA%
exit /b 0
"""

    return _salvar(nome, conteudo)

def executar_bat(caminho_bat):
    resultado = subprocess.run(
        ["cmd", "/c", str(caminho_bat)],
        capture_output=True, text=True, encoding="latin-1",
    )
    return resultado.returncode, resultado.stdout
@echo off
setlocal
echo ============================================
echo  AutomaLab - Teste de comandos em lote
echo ============================================
echo.

set "BASE=C:\AutomaLabTeste"

echo [PASSO 1] Garantindo a pasta de teste...
if not exist "%BASE%" mkdir "%BASE%"
echo Pasta garantida em %BASE%
echo.

echo [PASSO 2] Criando arquivos de exemplo...
if not exist "%BASE%\origem" mkdir "%BASE%\origem"
echo Conteudo A > "%BASE%\origem\arquivo1.txt"
echo Conteudo B > "%BASE%\origem\arquivo2.txt"
echo Conteudo C > "%BASE%\origem\foto.jpg"
echo Arquivos criados em %BASE%\origem
echo.

echo [PASSO 3] Copiando .txt para a pasta de backup...
if not exist "%BASE%\backup" mkdir "%BASE%\backup"
copy /Y "%BASE%\origem\*.txt" "%BASE%\backup\" >nul
if %errorlevel%==0 (
    echo Copia concluida com sucesso.
) else (
    echo ERRO: falha na copia dos arquivos.
)
echo.

echo [PASSO 4] Listando os arquivos .txt com FOR...
for %%f in ("%BASE%\origem\*.txt") do (
    echo Encontrado: %%~nxf
)
echo.

echo [PASSO 5] Removendo um arquivo e verificando...
del /Q "%BASE%\backup\arquivo1.txt"
if exist "%BASE%\backup\arquivo1.txt" (
    echo ERRO: o arquivo ainda existe.
) else (
    echo Arquivo removido corretamente.
)
echo.

echo ============================================
echo  Teste finalizado com sucesso.
echo ============================================
endlocal
pause
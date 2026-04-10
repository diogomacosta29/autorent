from datetime import datetime
 
# Caminho para o ficheiro de log
CAMINHO_LOG = "log.txt"
 
 
def registar_log(assunto: str, mensagem: str):
    """
    Regista uma entrada no ficheiro log.txt.
    Cada linha tem o formato: [DATA HORA] | ASSUNTO | MENSAGEM
    Parâmetros:
        assunto  (str): Categoria do evento (ex: 'ERRO', 'ALUGUER', 'CLIENTE')
        mensagem (str): Descrição detalhada do evento
    """
    try:
        momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{momento}] | {assunto.upper()} | {mensagem}\n"
 
        with open(CAMINHO_LOG, "a", encoding="utf-8") as ficheiro:
            ficheiro.write(linha)
 
    except Exception as e:
        # Se o log falhar, mostrar no terminal para não perder o erro
        print(f"[AVISO] Não foi possível escrever no log: {e}")
 
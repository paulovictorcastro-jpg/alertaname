import os
import json
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÕES ---
URL_API = "https://sisdocs.tce.rn.gov.br/api/v1/DiarioEletronico?publicado=true"
TERMO_BUSCA = "JALES"

# O GitHub Actions vai preencher essas variáveis dinamicamente através dos Secrets
EMAIL_REMETENTE = os.environ.get("m4th3m4t1c0@gmail.com")
SENHA_APP_GMAIL = os.environ.get("hile uosn hbhw vpyl")
EMAIL_DESTINATARIO = os.environ.get("raonicl@gmail.com")

def enviar_email(termo):
    if not all([EMAIL_REMETENTE, SENHA_APP_GMAIL, EMAIL_DESTINATARIO]):
        print("Erro: Credenciais de e-mail não configuradas no ambiente.")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = f"🚨 ALERTA: Termo encontrado no Diário Oficial TCE-RN!"
    
    corpo = f"O termo '{termo}' foi localizado nos dados publicados hoje na API do TCE-RN."
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP('://gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP_GMAIL)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("E-mail de alerta enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def verificar_diario():
    try:
        # Usando urllib nativo em vez de requests (economiza instalação)
        req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode('utf-8'))
                texto_completo = json.dumps(dados, ensure_ascii=False).lower()
                
                if TERMO_BUSCA.lower() in texto_completo:
                    print(f"Termo '{TERMO_BUSCA}' encontrado!")
                    enviar_email(TERMO_BUSCA)
                else:
                    print("Busca realizada. O termo não foi encontrado hoje.")
            else:
                print(f"Erro ao acessar API. Status: {response.status}")
                
    except Exception as e:
        print(f"Falha na conexão com a API: {e}")

if __name__ == "__main__":
    verificar_diario()

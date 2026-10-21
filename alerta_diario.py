import os
import json
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÕES ---
URL_API = "https://sisdocs.tce.rn.gov.br/api/v1/DiarioEletronico?publicado=true"

# Mudamos para buscar os termos separados, garantindo que ache mesmo com espaços extras
TERMOS_BUSCA = ["antonio", "gilberto", "jales"]

# O GitHub Actions vai preencher essas variáveis dinamicamente através dos Secrets
EMAIL_REMETENTE = os.environ.get("m4th3m4t1c0@gmail.com")
SENHA_APP_GMAIL = os.environ.get("hile uosn hbhw vpyl")
EMAIL_DESTINATARIO = os.environ.get("raonicl@gmail.com")

def enviar_email():
    if not all([EMAIL_REMETENTE, SENHA_APP_GMAIL, EMAIL_DESTINATARIO]):
        print("❌ ERRO CRÍTICO: As variáveis de ambiente (Secrets) não estão preenchidas no GitHub!")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = f"🚨 ALERTA: Nome localizado no Diário Oficial TCE-RN!"
    
    corpo = "Os termos buscados foram localizados nos dados publicados hoje na API do TCE-RN."
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        print("🔄 Tentando conectar ao servidor SMTP do Gmail...")
        server = smtplib.SMTP('://gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP_GMAIL)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("✅ E-mail de alerta enviado com sucesso!")
    except Exception as e:
        print(f"❌ ERRO AO ENVIAR E-MAIL: O Gmail recusou a conexão. Detalhes: {e}")

def verificar_diario():
    try:
        print(f"🔄 Acessando a API: {URL_API} ...")
        req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode('utf-8'))
                texto_completo = json.dumps(dados, ensure_ascii=False).lower()
                
                # Verifica se TODOS os pedaços do nome estão presentes no JSON
                achou_todos = all(termo in texto_completo for termo in TERMOS_BUSCA)
                
                if achou_todos:
                    print("🎯 Sucesso! Todos os termos do nome foram encontrados na API.")
                    enviar_email()
                else:
                    print("ℹ️ Busca realizada. O nome completo não foi localizado nos dados de hoje.")
                    # Linha de debug para você ver o que a API respondeu no log do GitHub:
                    print(f"Trecho inicial dos dados capturados: {texto_completo[:500]}")
            else:
                print(f"❌ Erro ao acessar API. Status retornado: {response.status}")
                
    except Exception as e:
        print(f"❌ Falha de conexão com o servidor da API: {e}")

if __name__ == "__main__":
    verificar_diario()

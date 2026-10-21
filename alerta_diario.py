import json
import urllib.request
import sys

URL_API = "https://sisdocs.tce.rn.gov.br/api/v1/DiarioEletronico?publicado=true"

TERMOS_BUSCA = ["jales"]

def verificar_diario():
    try:
        print(f"🔄 Acessando a API do TCE-RN...")
        req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode('utf-8'))
                texto_completo = json.dumps(dados, ensure_ascii=False).lower()
                
                achou_todos = all(termo in texto_completo for termo in TERMOS_BUSCA)
                
                if achou_todos:
                    print("🎯 Sucesso! Termo encontrado.")
                    # sys.exit(0) indica sucesso ao GitHub Actions
                    sys.exit(0)
                else:
                    print("ℹ️ O termo não foi localizado nos dados de hoje.")
                    # sys.exit(1) cancela os próximos passos pois não há o que alertar
                    sys.exit(1)
            else:
                print(f"❌ Erro na API. Status: {response.status}")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Falha de conexão: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verificar_diario()

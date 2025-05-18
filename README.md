# Servidor MCP WAHA WhatsApp

Este projeto implementa um servidor MCP para envio de mensagens via WhatsApp utilizando o WAHA (WhatsApp HTTP API).

## Funcionalidades

- **Tool `send_whatsapp`**: envia texto para um número no formato internacional (+5511...).
- **Resource `contacts_list`**: retorna uma lista de três contatos pré-definidos.

## Pré-requisitos

1. Python 3.10 ou superior
2. uv (`pip install uv`)
3. Servidor WAHA rodando localmente em `http://localhost:3000` e sessão autenticada (veja https://waha.devlike.pro/docs/overview/quick-start/).

## Instalação

```bash
# Clone o repositório
git clone <URL_DO_REPO>
cd mcpwaha

# Instale dependências
uv pip install mcp httpx
```

## Configuração (opcional)

Se o endereço ou nome da sessão do WAHA forem diferentes, ajuste em `waha_mcp_server.py`:

```python
WAHA_API_URL = "http://seu-host:porta"
WAHA_SESSION_NAME = "nome-da-sessao"
```

## Executando o servidor MCP

```bash
uv run python waha_mcp_server.py
```

## Uso com Cursor

1. Crie ou edite o arquivo `.cursor/mcp.json` apontando para o servidor:

```json
{
  "mcpServers": {
    "waha-whatsapp-server": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "C:\\Users\\rvirg\\projects\\mcpwaha\\waha_mcp_server.py"
      ]
    }
  }
}
```

2. Reinicie o Cursor.
3. Exemplos de comandos:

- **Enviar mensagem**:
  ```
  @waha-whatsapp-server send_whatsapp +5511999999999 "Olá do Cursor!"
  ```

- **Listar contatos**:
  ```
  @waha-whatsapp-server contacts_list
  ```

- **Enviar mensagem para contato**:
  ```
  Envie "Bom dia" para João.
  ```

## Exemplo de chamada direta via HTTP

```python
import httpx

url = "http://localhost:3000/api/sendText"
payload = {
    "chatId": "5511999999999@c.us",
    "text": "Teste",
    "session": "default"
}
resp = httpx.post(url, json=payload)
print(resp.json())
```

## Observações

- Números devem iniciar com `+` e incluir código do país.
- Em caso de falha, verifique se o WAHA está rodando e autenticado.
- O resource `contacts_list` retorna um dicionário `{nome: número}`.

## Entregável

- Repositório Git com o código do servidor MCP.
- Relatório básico de uso com captura de tela demonstrando o envio de mensagem via MCP.

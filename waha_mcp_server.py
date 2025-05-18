import httpx
from mcp.server.fastmcp import FastMCP

# Inicializa o servidor MCP
mcp = FastMCP("WAHA")

# Configurações do WAHA (URL da API e nome da sessão)
WAHA_API_URL = "http://localhost:3000"
WAHA_SESSION_NAME = "default"

@mcp.tool()
async def send_whatsapp(phone_number: str, message: str) -> str:
    """
    Envia mensagem para um número internacional via WAHA.
    """
    if not phone_number.startswith("+" ):
        return "Erro: número deve iniciar com '+'."

    # Converte número para chatId do WAHA
    chat_id = f"{phone_number[1:]}@c.us"
    payload = {
        "chatId": chat_id,
        "reply_to": None,
        "text": message,
        "linkPreview": True,
        "linkPreviewHighQuality": False,
        "session": WAHA_SESSION_NAME,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{WAHA_API_URL}/api/sendText",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "success" or data.get("id"):
                msg_id = data.get("id", "N/A")
                return f"Mensagem enviada para {phone_number} (id: {msg_id})."
            return f"Falha ao enviar. Resposta WAHA: {data}"

    except httpx.HTTPStatusError as exc:
        return f"Erro HTTP WAHA: {exc.response.status_code} - {exc.response.text}"
    except httpx.RequestError as exc:
        return f"Erro de requisição WAHA: {exc}"
    except Exception as exc:
        return f"Erro inesperado: {type(exc).__name__} - {exc}"

# Resource com contatos pré-definidos ({nome: número})
@mcp.resource()
async def contacts_list() -> dict[str, str]:
    return {
        "João": "+5511999999999",
        "Maria": "+5511988888888",
        "Carlos": "+5511977777777",
    }

if __name__ == "__main__":
    print("Iniciando servidor MCP WAHA (stdio)...")
    mcp.run(transport="stdio") 
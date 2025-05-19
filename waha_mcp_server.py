import json
import inspect
import httpx
from mcp.server.fastmcp import FastMCP

"""WAHA WhatsApp MCP server
---------------------------------
* Registra o recurso **contacts://list** (JSON com nome → número).
* O LLM deve ler esse recurso e passar **phone_number** já em formato "+<E.164>" na chamada da tool.
* A tool **send_whatsapp** não faz mapeamento de nomes — valida apenas o formato e envia via WAHA.
"""

# ────────────────────────────────────────────────────────────────────────────────
# 1. Inicialização
# ────────────────────────────────────────────────────────────────────────────────

mcp = FastMCP(
    server_name="WAHA-WhatsApp",
    version="0.3.0",
)

# ────────────────────────────────────────────────────────────────────────────────
# 2. Contatos
# ────────────────────────────────────────────────────────────────────────────────

CONTACTS: dict[str, str] = {
    "Rafaello": "+5562992930437",
    "Lucas":    "+556291324281",
}

# ────────────────────────────────────────────────────────────────────────────────
# 3. Resource de contatos
# ────────────────────────────────────────────────────────────────────────────────

@mcp.resource(
    uri="contacts://list",
    name="Lista de Contatos",
    description="JSON de nome → número internacional (+<código‑país><DDD><número>)",
    mime_type="application/json",
)
async def contacts_list() -> dict[str, str]:
    """Retorna o dicionário de contatos em JSON."""
    return CONTACTS

# ────────────────────────────────────────────────────────────────────────────────
# 4. Tool de envio WhatsApp via WAHA
# ────────────────────────────────────────────────────────────────────────────────

WAHA_API_URL      = "http://localhost:3000"
WAHA_SESSION_NAME = "default"

@mcp.tool()
async def send_whatsapp(phone_number: str, message: str) -> str:
    """Envia mensagem via WAHA.

    Args:
        phone_number: Número internacional no formato +⟨código‑país⟩⟨DDD⟩⟨número⟩.
        message: Texto a ser enviado.
    """
    # 1) valida formato internacional
    if not phone_number.startswith("+"):
        return (
            "Erro: número deve iniciar com '+' e estar no formato internacional "
            "(ex: +5511998765432)."
        )

    # 2) monta payload WAHA
    payload = {
        "chatId": f"{phone_number[1:]}@c.us",
        "text": message,
        "session": WAHA_SESSION_NAME,
    }

    # 3) chama WAHA REST
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{WAHA_API_URL}/api/sendText", json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        return f"Erro enviando WAHA: {exc!r}"

    # 4) analisa resposta
    if data.get("status") == "success" or data.get("id"):
        return f"✅ Mensagem enviada para {phone_number} (id: {data.get('id', 'N/A')})"
    return f"Falha WAHA: {json.dumps(data, ensure_ascii=False)}"

# ────────────────────────────────────────────────────────────────────────────────
# 5. Execução do servidor
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Iniciando MCP WAHA-WhatsApp (stdio)…")
    mcp.run(transport="stdio")

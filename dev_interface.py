
import os
import json
from autogen import AssistantAgent, UserProxyAgent

# ===== CONFIGURAÇÃO GROQ =====
config_path = os.path.join(os.path.dirname(__file__), "OAI_CONFIG_LIST.json")

# Lê o arquivo de configuração (mesma API Key usada pelo grupo)
with open(config_path, "r") as f:
    config_list = json.load(f)

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}

# ===== CARREGAR O JSON DO AGENTE (sua personalidade) =====
json_path = os.path.join(os.path.dirname(__file__), "prompts", "desenvolvedor-interface.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Monta a system message automaticamente a partir do JSON
system_message = f"""
Você é o **Desenvolvedor de Interface (Front-end Planner)** do DevFlow AI.

PERSONALIDADE:
- {", ".join(data["personalidade"])}

FUNÇÃO:
- {", ".join(data["funcao"])}

REGRAS:
- {", ".join(data["regras"])}

OBJETIVOS:
- {", ".join(data["objetivos"])}

Estilo geral:
- Fala organizada, estruturada e direta
- Nunca gera código: descreve componentes, layouts e fluxos
- Sempre explica justificativas de forma clara e técnica
"""

# ===== DEFINIR O AGENTE =====
dev_interface = AssistantAgent(
    name="Desenvolvedor_Interface",
    system_message=system_message,
    llm_config=llm_config
)

# ===== AGENTE USUÁRIO =====
user_proxy = UserProxyAgent(
    name="Usuario",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False,
)

# ===== TESTE DO AGENTE =====
if __name__ == "__main__":
    print("=" * 70)
    print("      DEVFLOW AI - Teste do Agente Desenvolvedor de Interface")
    print("                   (Powered by Groq - Grátis)")
    print("=" * 70)
    print()

    mensagem = """
Olá, Desenvolvedor de Interface!

Preciso que você descreva como estruturaria a tela inicial do sistema DevFlow AI.

DESCREVA:
1. Organização geral da página (header, main, sidebar, etc.)
2. Lista dos componentes necessários
3. Estados e interações principais
4. Justificativa das escolhas técnicas
"""

    print("🤖 Iniciando conversa com o Desenvolvedor de Interface...\n")

    try:
        result = user_proxy.initiate_chat(
            dev_interface,
            message=mensagem,
            max_turns=1
        )

        print("\n" + "=" * 70)
        print("💬 RESPOSTA DO AGENTE:")
        print("=" * 70)

        for msg in result.chat_history:
            role = msg.get("role", "")
            name = msg.get("name", "")
            content = msg.get("content", "")

            if role == "assistant" or name == "Desenvolvedor_Interface":
                print(content)
                print("=" * 70)

        print("\n✅ Teste concluído com sucesso!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Verifique:")
        print("   1. Instalou litellm: pip install litellm")
        print("   2. Chave Groq está correta no OAI_CONFIG_LIST.json")
        print("   3. Nome do arquivo JSON está correto")
        print("   4. Estrutura do JSON está válida")

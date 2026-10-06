import random
import gradio as gr

# Base de Dados expandida com artes oficiais em HD (PokeAPI)
POKEMON_DB = {
    # --- GERAÇÃO 1 ---
    "Pikachu": {
        "id": 25,
        "tipo": "Elétrico ⚡",
        "hp": 35,
        "ataque": 55,
        "defesa": 40,
        "velocidade": 90,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "desc": "Quando se enfurece, liberta a energia acumulada pelas bolsas de suas bochechas.",
    },
    "Charizard": {
        "id": 6,
        "tipo": "Fogo / Voador 🔥🦅",
        "hp": 78,
        "ataque": 84,
        "defesa": 78,
        "velocidade": 100,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "desc": "Voa pelo céu em busca de oponentes fortes. Suas chamas ficam mais quentes à medida que ganha experiência.",
    },
    "Blastoise": {
        "id": 9,
        "tipo": "Água 💧",
        "hp": 79,
        "ataque": 83,
        "defesa": 100,
        "velocidade": 78,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "desc": "Os jatos d'água dos canhões em seu casco conseguem perfurar aço com facilidade.",
    },
    "Venusaur": {
        "id": 3,
        "tipo": "Planta / Veneno 🌿☠️",
        "hp": 80,
        "ataque": 82,
        "defesa": 83,
        "velocidade": 80,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
        "desc": "A flor em suas costas cresce absorvendo a energia solar, exalando um aroma relaxante.",
    },
    "Gengar": {
        "id": 94,
        "tipo": "Fantasma / Veneno 👻☠️",
        "hp": 60,
        "ataque": 65,
        "defesa": 60,
        "velocidade": 110,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "desc": "Esconde-se nas sombras das cidades. Dizem que quando a temperatura cai repentinamente, um Gengar está por perto.",
    },
    "Mewtwo": {
        "id": 150,
        "tipo": "Psíquico 🔮",
        "hp": 106,
        "ataque": 110,
        "defesa": 90,
        "velocidade": 130,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "desc": "Um Pokémon criado por manipulação genética. Suas habilidades de combate foram elevadas ao nível máximo.",
    },
    "Snorlax": {
        "id": 143,
        "tipo": "Normal 💤",
        "hp": 160,
        "ataque": 110,
        "defesa": 65,
        "velocidade": 30,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png",
        "desc": "Come cerca de 400 kg de comida por dia. Depois de comer, adormece e é difícil de acordar.",
    },
    "Eevee": {
        "id": 133,
        "tipo": "Normal 🦊",
        "hp": 55,
        "ataque": 55,
        "defesa": 50,
        "velocidade": 55,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "desc": "Possui um código genético irregular que permite evoluir para diversas formas de acordo com o ambiente.",
    },
    "Dragonite": {
        "id": 149,
        "tipo": "Dragão / Voador 🐉🦅",
        "hp": 91,
        "ataque": 134,
        "defesa": 95,
        "velocidade": 80,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
        "desc": "Dizem que vive em algum lugar do oceano. Consegue dar uma volta ao mundo em apenas 16 horas.",
    },
    "Gyarados": {
        "id": 130,
        "tipo": "Água / Voador 🌊🐉",
        "hp": 95,
        "ataque": 125,
        "defesa": 79,
        "velocidade": 81,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/130.png",
        "desc": "Extremamente agressivo. Diz a lenda que ele aparece em tempos de conflito para destruir tudo ao seu redor.",
    },
    "Arcanine": {
        "id": 59,
        "tipo": "Fogo 🔥",
        "hp": 90,
        "ataque": 110,
        "defesa": 80,
        "velocidade": 95,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/59.png",
        "desc": "Conhecido por sua imensa velocidade e graciosidade. Corre como se estivesse voando sobre as terras.",
    },
    "Lapras": {
        "id": 131,
        "tipo": "Água / Gelo ❄️🌊",
        "hp": 130,
        "ataque": 85,
        "defesa": 80,
        "velocidade": 60,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/131.png",
        "desc": "Possui uma índole dócil e adora transportar pessoas e outros Pokémon sobre o oceano.",
    },
    "Alakazam": {
        "id": 65,
        "tipo": "Psíquico 🔮",
        "hp": 55,
        "ataque": 50,
        "defesa": 45,
        "velocidade": 120,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png",
        "desc": "Seu cérebro nunca para de crescer, dando-lhe um QI de mais de 5.000. Lembra de tudo o que acontece.",
    },
    "Machamp": {
        "id": 68,
        "tipo": "Lutador 🥊",
        "hp": 90,
        "ataque": 130,
        "defesa": 80,
        "velocidade": 55,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/68.png",
        "desc": "Com seus quatro braços musculosos, consegue desferir mil soco em apenas dois segundos.",
    },
    "Mew": {
        "id": 151,
        "tipo": "Psíquico ✨",
        "hp": 100,
        "ataque": 100,
        "defesa": 100,
        "velocidade": 100,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/151.png",
        "desc": "Dizem que possui o DNA de todos os Pokémon. É capaz de aprender qualquer técnica existente.",
    },

    # --- GERAÇÃO 2 ---
    "Umbreon": {
        "id": 197,
        "tipo": "Sombrio 🌙",
        "hp": 95,
        "ataque": 65,
        "defesa": 110,
        "velocidade": 65,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/197.png",
        "desc": "Quando exposto à luz do luar, os anéis em seu corpo brilham levemente, despertando seu poder oculto.",
    },
    "Tyranitar": {
        "id": 248,
        "tipo": "Pedra / Sombrio 🪨🌑",
        "hp": 100,
        "ataque": 134,
        "defesa": 110,
        "velocidade": 61,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/248.png",
        "desc": "Sua carcaça é invulnerável a praticamente qualquer ataque. Consegue demolir montanhas inteiras.",
    },
    "Scizor": {
        "id": 212,
        "tipo": "Inseto / Aço 🦞⚙️",
        "hp": 70,
        "ataque": 130,
        "defesa": 100,
        "velocidade": 65,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/212.png",
        "desc": "Tem o corpo duro como aço. Suas garras possuem marcas semelhantes a olhos para assustar inimigos.",
    },

    # --- GERAÇÃO 3 ---
    "Gardevoir": {
        "id": 282,
        "tipo": "Psíquico / Fada 🔮🧚",
        "hp": 68,
        "ataque": 65,
        "defesa": 65,
        "velocidade": 80,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "desc": "Protege seu Treinador com a própria vida. Tem a capacidade psicocinética de criar pequenos buracos negros.",
    },
    "Blaziken": {
        "id": 257,
        "tipo": "Fogo / Lutador 🔥🥊",
        "hp": 80,
        "ataque": 120,
        "defesa": 70,
        "velocidade": 80,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/257.png",
        "desc": "Possui pernas incrivelmente fortes. Consegue saltar facilmente por cima de edifícios de 30 andares.",
    },
    "Metagross": {
        "id": 376,
        "tipo": "Aço / Psíquico ⚙️🔮",
        "hp": 80,
        "ataque": 135,
        "defesa": 130,
        "velocidade": 70,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/376.png",
        "desc": "Formado pela fusão de quatro Beldum. Seus quatro cérebros superam o processamento de um supercomputador.",
    },
    "Rayquaza": {
        "id": 384,
        "tipo": "Dragão / Voador 🐉🌩️",
        "hp": 105,
        "ataque": 150,
        "defesa": 90,
        "velocidade": 95,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/384.png",
        "desc": "Vive na camada de ozônio bem acima das nuvens. Dizem que desceu para acalmar o conflito entre Kyogre e Groudon.",
    },

    # --- GERAÇÃO 4 ---
    "Lucario": {
        "id": 448,
        "tipo": "Lutador / Aço 🥊⚙️",
        "hp": 70,
        "ataque": 110,
        "defesa": 70,
        "velocidade": 90,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "desc": "Consegue sentir a Aura emitida por todos os seres vivos e prever os movimentos de seus adversários.",
    },
    "Garchomp": {
        "id": 445,
        "tipo": "Dragão / Terrestre 🐉🏜️",
        "hp": 108,
        "ataque": 130,
        "defesa": 95,
        "velocidade": 102,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/445.png",
        "desc": "Voa em velocidades sônicas para caçar presas. Suas asas criam lâminas de ar cortantes ao voar.",
    },
    "Infernape": {
        "id": 392,
        "tipo": "Fogo / Lutador 🔥🥊",
        "hp": 76,
        "ataque": 104,
        "defesa": 71,
        "velocidade": 108,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/392.png",
        "desc": "Usa um estilo de artes marciais único envolvendo todos os seus membros. Suas chamas na cabeça nunca se apagam.",
    },
    "Togekiss": {
        "id": 468,
        "tipo": "Fada / Voador 🧚🦅",
        "hp": 85,
        "ataque": 50,
        "defesa": 95,
        "velocidade": 80,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/468.png",
        "desc": "Aparece apenas em locais pacíficos, espalhando bênçãos e alegrias para as pessoas de coração puro.",
    },

    # --- GERAÇÕES 6 e 7 ---
    "Greninja": {
        "id": 658,
        "tipo": "Água / Sombrio 🥷🌊",
        "hp": 72,
        "ataque": 95,
        "defesa": 67,
        "velocidade": 122,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/658.png",
        "desc": "Cria shurikens de água comprimida capazes de fatiar metal. Desaparece e reaparece como um ninja.",
    },
    "Sylveon": {
        "id": 700,
        "tipo": "Fada 🧚",
        "hp": 95,
        "ataque": 65,
        "defesa": 65,
        "velocidade": 60,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/700.png",
        "desc": "Envia ondas pacificadoras a partir de suas fitas sensitivas para acalmar os sentimentos de hostilidade.",
    },
    "Mimikyu": {
        "id": 778,
        "tipo": "Fantasma / Fada 👻🧚",
        "hp": 55,
        "ataque": 90,
        "defesa": 80,
        "velocidade": 96,
        "imagem": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/778.png",
        "desc": "Esconde sua verdadeira aparência sob um disfarce de Pikachu na esperança de fazer amigos.",
    },
}

# --- LÓGICA DAS FUNÇÕES ---


def buscar_pokedex(nome_pokemon):
    """Retorna a imagem e os dados formatados do Pokémon selecionado"""
    p = POKEMON_DB[nome_pokemon]

    info_markdown = f"""
    ### #{p['id']:03d} — {nome_pokemon}
    * **Tipo:** {p['tipo']}
    * **HP:** `{p['hp']}`
    * **Ataque:** `{p['ataque']}`
    * **Defesa:** `{p['defesa']}`
    * **Velocidade:** `{p['velocidade']}`
    
    > *"{p['desc']}"*
    """
    return p["imagem"], info_markdown


def iniciar_quiz():
    """Sorteia um Pokémon para o mini-jogo"""
    nome_secreto = random.choice(list(POKEMON_DB.keys()))
    p = POKEMON_DB[nome_secreto]

    dica = f"💡 **Dica:** É do tipo `{p['tipo']}` e {p['desc'].lower()}"
    status = "🎮 *Sorteando novo Pokémon... Tente adivinhar quem é!*"

    return nome_secreto, dica, status, ""


def checar_resposta_quiz(palpite, nome_secreto):
    """Valida o palpite do usuário"""
    if not nome_secreto:
        return (
            "⚠️ Clique em **Sortear Pokémon** para começar uma rodada!",
            None,
        )

    if palpite and palpite.strip().lower() == nome_secreto.lower():
        imagem_revelada = POKEMON_DB[nome_secreto]["imagem"]
        resultado = f"🎉 **ACERTOU!** É o **{nome_secreto}**! 🔥"
        return resultado, imagem_revelada
    else:
        return (
            f"❌ **Incorreto!** Tente novamente. Seu palpite foi: `{palpite}`",
            None,
        )


def montar_equipe(estilo):
    """Gera um time aleatório de 6 Pokémon baseado na preferência"""
    todos = list(POKEMON_DB.keys())

    if estilo == "Ofensivo ⚔️":
        equipe_nomes = sorted(
            todos, key=lambda x: POKEMON_DB[x]["ataque"], reverse=True
        )[:6]
    elif estilo == "Tanque/Defensivo 🛡️":
        equipe_nomes = sorted(
            todos,
            key=lambda x: POKEMON_DB[x]["defesa"] + POKEMON_DB[x]["hp"],
            reverse=True,
        )[:6]
    else:
        equipe_nomes = random.sample(todos, min(6, len(todos)))

    cards_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;'>"
    for nome in equipe_nomes:
        p = POKEMON_DB[nome]
        cards_html += f"""
        <div style='background-color: #1e293b; border: 2px solid #3b82f6; border-radius: 10px; padding: 10px; width: 140px; text-align: center; color: white;'>
            <img src='{p['imagem']}' width='90'/>
            <h4 style='margin: 5px 0;'>{nome}</h4>
            <span style='font-size: 0.8em; background-color: #334155; padding: 2px 6px; border-radius: 5px;'>{p['tipo']}</span>
        </div>
        """
    cards_html += "</div>"

    return cards_html


# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
custom_css = """
.pokeball-header {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    border-bottom: 6px solid #111827;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}
.pokeball-header h1 {
    font-size: 2.2em;
    font-weight: 800;
    margin: 0;
}
.stat-box {
    border: 2px solid #f59e0b;
    border-radius: 12px;
    padding: 15px;
}
"""

theme = gr.themes.Soft(
    primary_hue="red", secondary_hue="amber", neutral_hue="slate"
)

with gr.Blocks(css=custom_css, theme=theme, title="Pokédex Gradio") as app:

    # Cabeçalho Temático
    gr.HTML(
        """
        <div class="pokeball-header">
            <h1>🔴 POKÉDEX GRADIO INTERACTIVE ⚪</h1>
            <p style="margin-top: 5px; opacity: 0.9;">Explore Pokémon, jogue o Quiz e monte sua Equipe Campeã!</p>
        </div>
    """
    )

    with gr.Tabs():

        # --- ABA 1: POKÉDEX CENTRAL ---
        with gr.Tab("📱 Pokédex Central"):
            with gr.Row():
                with gr.Column(scale=1):
                    pokemon_select = gr.Dropdown(
                        choices=list(POKEMON_DB.keys()),
                        value="Pikachu",
                        label="Selecione um Pokémon:",
                    )
                    btn_consultar = gr.Button("🔍 Consultar Pokédex", variant="primary")

                with gr.Column(scale=1):
                    poke_img = gr.Image(
                        value=POKEMON_DB["Pikachu"]["imagem"],
                        label="Arte Oficial",
                        height=280,
                    )

                with gr.Column(scale=1):
                    poke_info = gr.Markdown(
                        buscar_pokedex("Pikachu")[1], elem_classes=["stat-box"]
                    )

            pokemon_select.change(
                fn=buscar_pokedex,
                inputs=pokemon_select,
                outputs=[poke_img, poke_info],
            )
            btn_consultar.click(
                fn=buscar_pokedex,
                inputs=pokemon_select,
                outputs=[poke_img, poke_info],
            )

        # --- ABA 2: QUIZ "QUEM É ESSE POKÉMON?" ---
        with gr.Tab("❓ Quem é esse Pokémon?"):
            secret_state = gr.State("")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### ❓ Quem é esse Pokémon?")
                    quiz_dica = gr.Markdown("Clique no botão abaixo para sortear!")
                    btn_sortear = gr.Button("🎲 Sortear Pokémon", variant="secondary")

                    input_palpite = gr.Textbox(
                        placeholder="Digite o nome do Pokémon...",
                        label="Seu Palpite:",
                    )
                    btn_responder = gr.Button("🔥 Enviar Resposta", variant="primary")

                with gr.Column():
                    quiz_status = gr.Markdown("### Aguardando início...")
                    quiz_revelacao_img = gr.Image(
                        label="Pokémon Revelado",
                        height=260,
                        interactive=False,
                    )

            btn_sortear.click(
                fn=iniciar_quiz,
                outputs=[secret_state, quiz_dica, quiz_status, input_palpite],
            )

            btn_responder.click(
                fn=checar_resposta_quiz,
                inputs=[input_palpite, secret_state],
                outputs=[quiz_status, quiz_revelacao_img],
            )

        # --- ABA 3: GERADOR DE EQUIPE ---
        with gr.Tab("🛡️ Gerador de Equipe"):
            gr.Markdown("### Monte seu Esquadrão para a Liga Pokémon!")

            with gr.Row():
                estilo_input = gr.Radio(
                    choices=[
                        "Equilibrado ⚖️",
                        "Ofensivo ⚔️",
                        "Tanque/Defensivo 🛡️",
                    ],
                    value="Equilibrado ⚖️",
                    label="Estilo de Batalha:",
                )
                btn_gerar_team = gr.Button(
                    "⚡ Criar Equipe de 6", variant="primary"
                )

            display_team = gr.HTML()

            btn_gerar_team.click(
                fn=montar_equipe, inputs=estilo_input, outputs=display_team
            )

if __name__ == "__main__":
    app.launch()
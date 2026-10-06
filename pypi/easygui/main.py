import random
import easygui as eg

TITLE = "Jorge Ben Jor - O Rei do Samba Rock 🎸✨"


def run_quiz():
    """Quiz de perguntas sobre Jorge Ben Jor"""
    pontos = 0

    # Pergunta 1
    q1 = eg.choicebox(
        "1. Em qual álbum histórico de 1974 está a faixa 'Os Alquimistas Estão Chegando'?",
        title=TITLE + " - Quiz",
        choices=[
            "A Tábua de Esmeralda",
            "Samba Esquema Novo",
            "África Brasil",
            "Força Bruta",
        ],
    )
    if q1 == "A Tábua de Esmeralda":
        eg.msgbox(
            "Certíssimo! Os alquimistas estão chegando, estão chefiando! 🧪✨",
            title=TITLE,
        )
        pontos += 1
    elif q1 is not None:
        eg.msgbox(
            "Ops! A resposta correta era 'A Tábua de Esmeralda'.", title=TITLE
        )

    # Pergunta 2
    q2 = eg.choicebox(
        "2. Qual jogador de futebol inspirou a canção 'Fio Maravilha'?",
        title=TITLE + " - Quiz",
        choices=[
            "Pelé (Santos)",
            "Garrincha (Botafogo)",
            "João Baptista Sales (Flamengo)",
            "Zico (Flamengo)",
        ],
    )
    if q2 == "João Baptista Sales (Flamengo)":
        eg.msgbox(
            "Gol de anjo! Um gol de placa, de deusa, de mestre! ⚽🔥",
            title=TITLE,
        )
        pontos += 1
    elif q2 is not None:
        eg.msgbox(
            "Errou! Foi o jogador do Flamengo João Baptista Sales, o 'Fio Maravilha'.",
            title=TITLE,
        )

    # Pergunta 3
    q3 = eg.choicebox(
        "3. Quem é o famoso 'Síndico' citado no sucesso 'W/Brasil'?",
        title=TITLE + " - Quiz",
        choices=["Erasmo Carlos", "Tim Maia", "Roberto Carlos", "Gilberto Gil"],
    )
    if q3 == "Tim Maia":
        eg.msgbox("Chama o Síndico! Tim Maia! 🎙️⚡", title=TITLE)
        pontos += 1
    elif q3 is not None:
        eg.msgbox("Não foi dessa vez! O Síndico é o grande Tim Maia.", title=TITLE)

    eg.msgbox(
        f"Fim do Quiz!\nVocê acertou {pontos} de 3 perguntas.", title=TITLE
    )


def run_jukebox():
    """Jukebox com histórias e curiosidades dos maiores hits"""
    historias = {
        "Mas, que Nada! (1963)": (
            "Lançada no álbum de estreia 'Samba Esquema Novo', é uma das músicas "
            "brasileiras mais conhecidas e regravadas no mundo, imortalizada também por Sérgio Mendes."
        ),
        "Taj Mahal (1972)": (
            "O famoso refrão 'Tete teteretê' marcou época. Curiosidade: o cantor britânico "
            "Rod Stewart admitiu que o refrão de 'Da Ya Think I'm Sexy?' foi plagia do/inspirado nesta música."
        ),
        "Jorge da Capadócia (1975)": (
            "Inspirada na oração e devoção a São Jorge. Foi regravada com enorme sucesso "
            "pela banda Racionais MC's na música 'Jorge da Capadócia' / 'Capítulo 4, Versículo 3'."
        ),
        "País Tropical (1969)": (
            "Um dos maiores hinos da MPB. Composta em um momento de pura celebração da brasilidade: "
            "'Mora num país tropical, abençoado por Deus e bonito por natureza!'"
        ),
    }

    escolha = eg.choicebox(
        "Escolha uma música para descobrir a história:",
        title=TITLE + " - Jukebox",
        choices=list(historias.keys()),
    )

    if escolha in historias:
        eg.msgbox(f"🎧 {escolha}\n\n{historias[escolha]}", title=TITLE)


def run_hit_generator():
    """Sorteia a música do dia"""
    hits = [
        "Chove Chuva — 'Chove chuva, chove sem parar...'",
        "Banda do Zé Pretinho — 'Chegou a Banda do Zé Pretinho!'",
        "Que Pena — 'Que pena, que pena que você não me quer...'",
        "Santa Clara Clareou — 'Santa Clara clareou, e o sol surgiu...'",
        "Bebete Vãobora — 'Bebete vãobora, que o samba já vai começar...'",
    ]

    hit = random.choice(hits)
    eg.msgbox(
        f"Sua música Ben Jor do dia para dar energia é:\n\n🎵 {hit}",
        title=TITLE,
    )


def main():
    eg.msgbox(
        "Bem-vindo ao Universo de Jorge Ben Jor!\n\n"
        "Mora num país tropical, abençoado por Deus e bonito por natureza! 🇧🇷🎸",
        title=TITLE,
        ok_button="Apertar o Passo! 🕺",
    )

    while True:
        menu_choices = [
            "🎵 Quiz Ben Jor (Testar conhecimentos)",
            "📜 Jukebox & Histórias das Músicas",
            "🎲 Hit do Dia (Gerador de Energia)",
            "❌ Sair",
        ]

        opcao = eg.buttonbox(
            "Escolha uma opção para curtir o ritmo do Samba Rock:",
            title=TITLE,
            choices=menu_choices,
        )

        if not opcao or opcao == "❌ Sair":
            eg.msgbox(
                "Fica com Deus, Fio Maravilha!\n'Mas que nada, sai da minha frente que eu quero passar...'",
                title=TITLE,
            )
            break

        if opcao == "🎵 Quiz Ben Jor (Testar conhecimentos)":
            run_quiz()
        elif opcao == "📜 Jukebox & Histórias das Músicas":
            run_jukebox()
        elif opcao == "🎲 Hit do Dia (Gerador de Energia)":
            run_hit_generator()


if __name__ == "__main__":
    main()
import os
from gtts import gTTS

# Texto com a frase icônica
texto = "Quem é esse Pokémon? ... É o Pikachu!"

# Gerar o áudio com a gTTS em português (pt)
tts = gTTS(text=texto, lang="pt", slow=False)

# Salvar o áudio no formato MP3
arquivo_audio = "quem_e_esse_pokemon.mp3"
tts.save(arquivo_audio)

print(f"Áudio salvo com sucesso como '{arquivo_audio}'!")

# Executar o arquivo de áudio automaticamente de acordo com o sistema operacional
if os.name == "nt":  # Windows
    os.system(f"start {arquivo_audio}")
elif os.name == "posix":  # macOS / Linux
    os.system(f"open '{arquivo_audio}' || xdg-open '{arquivo_audio}'")
import random
import re
from typing import List

class SatireEngine:
    # Frases absurdas exigidas no projeto e adicionais
    NONSENSE_PHRASES = [
        "inclusive os pombos já sabem disso",
        "segundo especialistas em abacates",
        "isso merece uma CPI dos guarda-chuvas",
        "mas ninguém perguntou aos jacarés",
        "estatisticamente falando, talvez",
        "conforme a associação internacional de comedores de pastel",
        "de acordo com a física quântica dos chinelos de dedo",
        "e afirmo isso com 327% de certeza absoluta",
        "embora a rotação da Terra discorde educadamente",
        "que é, inclusive, o esporte nacional em Netuno"
    ]

    # Analogias absurdas
    ABSURD_ANALOGIES = [
        "isso é tão útil quanto um cinzeiro em uma motocicleta",
        "isso faz tanto sentido quanto colocar uma capota em um submarino",
        "isso é mais confuso que cachorro em dia de mudança",
        "isso é como tentar escovar os dentes de um furacão com um cotonete",
        "isso é tão garantido quanto comprar um terreno na Lua de um vendedor de praia",
        "é igual a passar catchup no teclado para programar em Python mais rápido"
    ]

    # Transições confiantes/mudanças de assunto
    SUBJECT_SHIFTS = [
        "Falando nisso, você sabia que a capivara média passa 40% do tempo julgando a humanidade em silêncio?",
        "Mas esquecendo isso por um segundo, precisamos discutir seriamente por que a tomada de três pinos foi inventada.",
        "Mudei de ideia: vamos falar sobre o império romano e por que a berinjela é, na verdade, uma fruta incompreendida.",
        "De qualquer forma, a Lua é feita de queijo prato e ninguém pode me provar o contrário.",
        "Aliás, acabei de decidir que o esporte mais perigoso do mundo é tentar abrir um pote de palmito sob pressão.",
        "O que nos leva a pensar: onde estão guardados todos os pés esquerdos dos chinelos perdidos?"
    ]

    # Frases de excesso de confiança
    OVERCONFIDENCE_PHRASES = [
        "Como a única entidade viva que compreende o segredo dos dinossauros de plástico...",
        "Com certeza absoluta (e quem discordar é claramente financiado pela guilda dos patinetes)...",
        "É cientificamente comprovado pela minha própria mente brilhante...",
        "Sem sombra de dúvida, e afirmo isso sob juramento perante os pinguins da Patagônia..."
    ]

    # Erros leves de português
    TYPOS = {
        r"\bcom certeza\b": "comcerteza",
        r"\bmas\b": "mais",
        r"\bnada a ver\b": "nada haver",
        r"\bproblema\b": "probrema",
        r"\bpor que\b": "porque",
        r"\bporque\b": "por que",
        r"\batrás\b": "atras",
        r"\banalisar\b": "analizar",
        r"\bexcesso\b": "exesso",
        r"\bviagem\b": "viajem",
        r"\bbrainstorm\b": "breinstorm",
        r"\bparalelo\b": "pararelo",
    }

    @classmethod
    def apply_typos(cls, text: str, probability: float) -> str:
        """Aplica erros leves de português com base em uma probabilidade."""
        for pattern, replacement in cls.TYPOS.items():
            if random.random() < probability:
                # Substitui respeitando maiúsculas/minúsculas de forma básica
                def replace_case(match):
                    word = match.group(0)
                    if word.istitle():
                        return replacement.title()
                    return replacement
                text = re.sub(pattern, replace_case, text, flags=re.IGNORECASE)
        return text

    @classmethod
    def satirize_sentence(cls, sentence: str, level: int) -> str:
        """Satiriza uma única sentença dependendo do nível de intensidade."""
        if level <= 0 or not sentence.strip():
            return sentence

        # Limpa espaços
        sentence = sentence.strip()

        # Nível 1: Leve
        if level == 1:
            # 15% de chance de erro de português
            sentence = cls.apply_typos(sentence, 0.15)
            # 10% de chance de anexar uma frase nonsense no final
            if random.random() < 0.10:
                phrase = random.choice(cls.NONSENSE_PHRASES)
                if sentence.endswith(('.', '!', '?')):
                    sentence = f"{sentence[:-1]}, {phrase}{sentence[-1]}"
                else:
                    sentence = f"{sentence}, {phrase}."
            return sentence

        # Nível 2: Moderado
        elif level == 2:
            # 30% de chance de erros de português
            sentence = cls.apply_typos(sentence, 0.30)
            
            rand = random.random()
            # 15% de chance de introduzir analogia absurda
            if rand < 0.15:
                analogy = random.choice(cls.ABSURD_ANALOGIES)
                sentence = f"{sentence} (afinal, {analogy})."
            # 15% de chance de adicionar excesso de confiança
            elif rand < 0.30:
                intro = random.choice(cls.OVERCONFIDENCE_PHRASES)
                sentence = f"{intro} {sentence[0].lower()}{sentence[1:]}"
            # 15% de chance de frase nonsense no final
            elif rand < 0.45:
                phrase = random.choice(cls.NONSENSE_PHRASES)
                if sentence.endswith(('.', '!', '?')):
                    sentence = f"{sentence[:-1]}, {phrase}{sentence[-1]}"
                else:
                    sentence = f"{sentence}, {phrase}."
            return sentence

        # Nível 3: Totalmente Nonsense (Intensidade Máxima)
        else:
            # 50% de chance de erros de português
            sentence = cls.apply_typos(sentence, 0.50)
            
            rand = random.random()
            # 25% de chance de mudar completamente de assunto
            if rand < 0.25:
                shift = random.choice(cls.SUBJECT_SHIFTS)
                sentence = f"{sentence}. {shift}"
            # 25% de chance de enfiar analogia absurda
            elif rand < 0.50:
                analogy = random.choice(cls.ABSURD_ANALOGIES)
                sentence = f"{sentence}, o que {analogy}."
            # 25% de chance de botar excesso de confiança no início e nonsense no final
            else:
                intro = random.choice(cls.OVERCONFIDENCE_PHRASES)
                phrase = random.choice(cls.NONSENSE_PHRASES)
                sentence = f"{intro} {sentence[0].lower()}{sentence[1:]}, {phrase}."

            return sentence

    @classmethod
    def satirize_text(cls, text: str, level: int) -> str:
        """Satiriza um texto completo dividindo-o em sentenças e remontando."""
        if level <= 0 or not text.strip():
            return text

        # Separa o texto por pontuação, mantendo-a
        sentences = re.split(r'([.!?\n]+)', text)
        
        result = []
        i = 0
        while i < len(sentences):
            part = sentences[i]
            # Se for pontuação ou quebra de linha
            if re.match(r'^[.!?\n]+$', part):
                result.append(part)
                i += 1
            else:
                # Pega a parte do texto e a pontuação seguinte se houver
                next_part = sentences[i+1] if i+1 < len(sentences) else ""
                satirized = cls.satirize_sentence(part, level)
                # Se a frase satirizada já adicionou pontuação própria, removemos a original se colidir
                if satirized.endswith(('.', '!', '?')) and next_part in ('.', '!', '?'):
                    next_part = ""
                result.append(satirized)
                if next_part:
                    result.append(next_part)
                i += 2
                
        return "".join(result)

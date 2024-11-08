import streamlit as st
import re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))
from utils.db import MongoHandler

TOTAL_NUMBERS = 500
PROJECT = "rifa-sonhar-acordado"

def is_valid_phone_number(phone: str):
    """Checa via regex se o telefone segue um certo padrão.

    Padrão utilizado: XX XXXXX-XXXX.

    Examples
    --------
    >>> is_valid_phone_number("81 98888-8888")
    True
    >>> is_valid_phone_number("11 12345-6789")
    True
    >>> is_valid_phone_number("123 12345-6789")
    False

    """
    pattern = r"^\d{2} \d{5}-\d{4}$"
    return bool(re.match(pattern, phone))

st.set_page_config(
    page_title="Rifa do Sonhar Acordado",
    layout="centered",
    initial_sidebar_state="auto", menu_items=None)

# Initialize connection.
db = MongoHandler(set_project_name=PROJECT)

st.title("🎄✝️ Rifa do Sonhar Acordado!")

st.markdown("""Em dezembro faremos mais uma Grande Festa de Natal para as instituições que atendemos durante o ano pelo Sonhar Acordado! Estamos vendendo essa rifa pra ajudar nos custos do evento. Topam participar?

- Escolhe a quantidade 
- Me diz o número que queres (entre 1 e 500)
- Me envia o comprovante do Pix
- Fica na torcida para ganhar!

Em breve, abriremos as inscrições para quem quiser ser voluntário na Festa. Caso queira participar, será super bem-vindo(a)! ❤️

Ah, e fica ligado nos prêmios da rifa:
    
    - 1° PRÊMIO: R$ 100 Reais
    - 2° PRÊMIO: Um rodízio no restaurante 'Entre Amigos - O Bode'
    - 3° PRÊMIO: Um Kit de Cosméticos
    - 4° PRÊMIO: Uma Air Fryer.""")

name = st.text_input(
    "Só precisamos de 2 dados! Primeiro, por favor digite seu nome completo, para "
    "que possamos te identificar:")
phone = st.text_input(
    "Por fim, seu telefone com DDD (exemplo: `81 91234-1234`):")

if len(phone) > 0 and not is_valid_phone_number(phone):
    st.error("Número de telefone inválido. Por favor, escreva nesse formato de exemplo: 81 91234-1234, com o espaço e hífen.")

elif len(name) > 0 and len(phone) > 0:
    vocativo = f"Olá, {name}!"
    you_picked = db.nums_you_picked(name)
    if len(you_picked) > 0:
        st.subheader(
            "{} Você já pegou esse(s) número(s): {}. Se quiser "
            "pegar ainda outros, prossiga "
            "adiante.".format(
                vocativo,
                str(you_picked).replace("[", "").replace("]", "")
                )
            )
    else:
        st.subheader(
            "{} Pronto, agora qual número você gostaria "
            "de pegar para a Rifa?".format(vocativo))

    remaining = db.remaining_numbers(total_numbers=TOTAL_NUMBERS)
    option = st.selectbox(
        f"Selecione um número dentre os {len(remaining)} "
        "que não foram selecionados ainda.",
        tuple(["Nenhum"] + remaining))
    st.write('Valor selecionado:', option)

    if option != "Nenhum":
        st.markdown(
            "**Calma! Você pode voltar e escolher outro número, se "
            "quiser. Sua escolha só vai se efetivar após clicar "
            "em *Confirmar*.**")
        if st.button('Confirmar'):
            db.write_new_item(
                name=name,
                num=int(option),
                kwargs={"phone_number": phone}
            )
            st.markdown(
                "**Muito obrigado!** Para concluir a "
                "reserva da rifa, você precisa **transferir os R$5 para "
                "o seguinte PIX**:")

            st.subheader("Pix: hamiltonmmf@hotmail.com")

            st.markdown(
                "Fique ligado no Sorteio: 04/12/2024 às 20h. "
                "Para escolher um novo valor, por favor "
                "**recarregue** a página.")

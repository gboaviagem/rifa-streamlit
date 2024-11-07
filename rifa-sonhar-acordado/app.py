import streamlit as st
from utils.db import MongoHandler

st.set_page_config(
    page_title="Rifa do Sonhar Acordado",
    layout="centered",
    initial_sidebar_state="auto", menu_items=None)

# Initialize connection.
db = MongoHandler()

st.title("Rifa do Sonhar Acordado!")

st.markdown(
    """Olá! Obrigado por querer contribuir com a Rifa Solidária do SA! Fica ligado nos prêmios:
    
    - 1° PRÊMIO: R$ 100 Reais
    - 2° PRÊMIO: Um rodízio no restaurante 'Entre Amigos - O Bode'
    - 3° PRÊMIO: Um Kit de Cosméticos
    - 4° PRÊMIO: Uma Air Fryer.""")

name = st.text_input(
    "São só 2 passos! Primeiro, por favor digite seu nome, para "
    "que possamos te identificar:")

if len(name) > 0:
    vocativo = f"Olá, {name}!"
    you_picked = db.nums_you_picked(name)
    if len(you_picked) > 0:
        st.subheader(
            "{} Você **já pegou** os números: **{}**. Se quiser "
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

    remaining = db.remaining_numbers()
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
            db.write_new_number(name, int(option))
            st.markdown(
                "**Muito obrigado!** Para concluir a "
                "reserva da rifa, você precisa **transferir os R$5 para "
                "o seguinte PIX**:")

            st.subheader("Pix: hamiltonmmf@hotmail.com")

            st.markdown(
                "Fique ligado no Sorteio: 04/12/2024 às 20h. "
                "Para escolher um novo valor, por favor "
                "**recarregue** a página.")

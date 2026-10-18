
import streamlit as st

st.set_page_config(
    page_title="Meu Imposto",
    page_icon="💚",
    layout="centered"
)

# ESTILO DO SITE
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 8% 12%,
            rgba(94, 163, 113, 0.22), transparent 28%),
        radial-gradient(ellipse at 92% 35%,
            rgba(125, 190, 140, 0.20), transparent 30%),
        radial-gradient(ellipse at 15% 88%,
            rgba(94, 163, 113, 0.18), transparent 28%),
        #FFFFFF;
}

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #204D3A !important;
}

.subtitle {
    color: #637568;
    font-size: 1.05rem;
    text-align: center;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid #E0E9E0;
    border-radius: 18px;
    padding: 20px;
}

div.stButton > button {
    background: #26734D;
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 48px;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background: #1D5A3B;
    color: white;
    border: none;
}

div[data-testid="stNumberInput"] input {
    border-radius: 9px;
}

.footer {
    color: #748277;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 28px;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# TÍTULO DO SITE
st.markdown(
    "<h1 style='text-align:center;'>💚 Meu Imposto</h1>",
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Uma maneira simples de simular '
    'o seu imposto de renda.</p>',
    unsafe_allow_html=True
)

st.divider()


# CAIXA VERDE CENTRALIZADA
st.markdown("""
<div style="
    background-color: #204D3A;
    padding: 16px 24px;
    border-radius: 14px;
    margin: 0 auto 20px auto;
    width: fit-content;
    max-width: 100%;
    box-sizing: border-box;
    text-align: center;
">
    <h3 style="
        color: white !important;
        margin: 0;
        font-size: 22px;
    ">Seus dados</h3>
    <p style="
        color: #DCEBE0;
        margin: 8px 0 0 0;
        font-size: 16px;
    ">Preencha as informações abaixo.</p>
</div>
""", unsafe_allow_html=True)


# CAMPOS DA CALCULADORA
with st.container(border=True):
    salario = st.number_input(
        "Salário mensal (R$)",
        min_value=0.0,
        value=3000.0,
        step=100.0,
        format="%.2f"
    )

    inss = st.number_input(
        "Contribuição ao INSS (R$)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f"
    )

    dependentes = st.number_input(
        "Quantidade de dependentes",
        min_value=0,
        value=0,
        step=1
    )

    pensao = st.number_input(
        "Pensão alimentícia (R$)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f"
    )

    calcular = st.button(
        "Calcular meu imposto  →",
        type="primary",
        use_container_width=True
    )


# CÁLCULO
if calcular:
    base = (
        salario
        - inss
        - (dependentes * 189.59)
        - pensao
    )

    if base <= 2428.80:
        aliquota, parcela = 0, 0
    elif base <= 2826.65:
        aliquota, parcela = 7.5, 182.16
    elif base <= 3751.05:
        aliquota, parcela = 15, 394.16
    elif base <= 4664.68:
        aliquota, parcela = 22.5, 675.49
    else:
        aliquota, parcela = 27.5, 908.73

    imposto_inicial = max(
        0,
        base * (aliquota / 100) - parcela
    )

    if salario <= 5000:
        redutor = imposto_inicial
    elif salario <= 7350:
        redutor = max(
            0,
            978.62 - (0.133145 * salario)
        )
    else:
        redutor = 0

    imposto_final = max(
        0,
        imposto_inicial - redutor
    )

    # FORMATAÇÃO EM REAIS
    def reais(valor):
        texto = f"{valor:,.2f}"
        texto = texto.replace(",", "X")
        texto = texto.replace(".", ",")
        texto = texto.replace("X", ".")
        return f"R$ {texto}"

    st.markdown("### 📊 Resultado da simulação")

    with st.container(border=True):
        st.caption("Imposto final estimado")

        st.markdown(
            f"<h1 style='color:#26734D !important;'>"
            f"{reais(imposto_final)}</h1>",
            unsafe_allow_html=True
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Base de cálculo",
                reais(base)
            )

        with col2:
            st.metric(
                "Alíquota",
                f"{aliquota:.1f}%".replace(".", ",")
            )

        st.write(
            f"**Imposto antes do redutor:** "
            f"{reais(imposto_inicial)}"
        )

    st.warning(
        "Esta é uma simulação de demonstração. "
        "As faixas, deduções e regras de redução precisam "
        "ser conferidas e atualizadas conforme a legislação "
        "vigente. Não utilize o resultado como valor oficial."
    )


# RODAPÉ
st.markdown(
    '<p class="footer">Desenvolvido por Lorena Piotto 💚</p>',
    unsafe_allow_html=True
)

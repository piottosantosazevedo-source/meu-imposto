
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
    background-color: #FFFFFF;
    background-image:
        radial-gradient(ellipse 65px 42px at 8% 14%,
            #6FA780 0%, #6FA780 65%, transparent 68%),
        radial-gradient(ellipse 43px 58px at 91% 25%,
            #3F8057 0%, #3F8057 65%, transparent 69%),
        radial-gradient(ellipse 58px 34px at 13% 52%,
            #5D986D 0%, #5D986D 65%, transparent 69%),
        radial-gradient(ellipse 48px 38px at 94% 65%,
            #6FA780 0%, #6FA780 65%, transparent 69%),
        radial-gradient(ellipse 68px 42px at 7% 87%,
            #3F8057 0%, #3F8057 65%, transparent 69%),
        radial-gradient(ellipse 42px 55px at 88% 94%,
            #5D986D 0%, #5D986D 65%, transparent 69%);
    background-attachment: fixed;
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
    background: rgba(255, 255, 255, 0.96);
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
    color: #526B5B;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 28px;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# TÍTULO
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


# CABEÇALHO VERDE
st.markdown("""
<div style="
    background-color: #204D3A;
    padding: 16px 24px;
    border-radius: 14px;
    margin: 0 auto 20px auto;
    width: fit-content;
    max-width: 100%;
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
        value=None,
        step=100.0,
        placeholder="Digite seu salário bruto mensal (R$)",
        format="%.2f"
    )

    inss = st.number_input(
        "Contribuição ao INSS (R$)",
        min_value=0.0,
        value=None,
        step=50.0,
        placeholder="Digite o valor que você contribui no INSS",
        format="%.2f"
    )

    dependentes = st.number_input(
        "Quantidade de dependentes",
        min_value=0,
        value=None,
        step=1,
        placeholder="Digite a quantidade de dependentes"
    )

    pensao = st.number_input(
        "Pensão alimentícia (R$)",
        min_value=0.0,
        value=None,
        step=50.0,
        placeholder="Digite o valor da pensão alimentícia. Se você não tiver, digite 0",
        format="%.2f"
    )

    calcular = st.button(
        "Calcular meu imposto  →",
        type="primary",
        use_container_width=True
    )



# CÁLCULO DO IR MENSAL - REGRAS DE 2026
if calcular:
    if (
        salario is None
        or inss is None
        or dependentes is None
        or pensao is None
    ):
        st.error(
            "Preencha todos os campos. Se não tiver "
            "dependentes ou pensão dedutível, digite 0."
        )

    elif inss > salario or pensao > salario:
        st.error(
            "Confira os valores informados: os descontos "
            "não podem ser maiores que o salário neste simulador."
        )

    else:
        # Deduções legais
        deducoes_legais = (
            inss
            + dependentes * 189.59
            + pensao
        )

        # Desconto simplificado mensal de 2026
        desconto_simplificado = 607.20

        # Escolhe a opção de dedução mais vantajosa
        deducao_aplicada = max(
            deducoes_legais,
            desconto_simplificado
        )

        base = max(0, salario - deducao_aplicada)

        # Tabela progressiva mensal de 2026
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

        imposto_tabela = max(
            0,
            base * (aliquota / 100) - parcela
        )

        # Redução mensal de 2026
        if salario <= 5000:
            reducao = min(imposto_tabela, 312.89)

        elif salario <= 7350:
            reducao = max(
                0,
                978.62 - (0.133145 * salario)
            )
            reducao = min(imposto_tabela, reducao)

        else:
            reducao = 0

        imposto_final = max(
            0,
            imposto_tabela - reducao
        )

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
                st.metric("Base de cálculo", reais(base))

            with col2:
                st.metric(
                    "Alíquota",
                    f"{aliquota:.1f}%".replace(".", ",")
                )

            st.write(
                f"**Dedução aplicada:** {reais(deducao_aplicada)}"
            )
            st.write(
                f"**Imposto pela tabela:** {reais(imposto_tabela)}"
            )
            st.write(
                f"**Redução aplicada:** {reais(reducao)}"
            )

        st.warning(
            "Simulação mensal simplificada para 2026. "
            "Considere apenas pensão legalmente dedutível. "
            "O resultado pode variar conforme outros rendimentos, "
            "deduções e circunstâncias individuais. Não substitui "
            "o cálculo oficial da fonte pagadora ou orientação fiscal."
        )


# RODAPÉ
st.markdown(
    '<p class="footer">Desenvolvido por Lorena Piotto 💚</p>',
    unsafe_allow_html=True
)

from pymongo import MongoClient
import streamlit as st

# Conectando com o MongoDB
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

# Atribuindo variáveis que correspondem ao banco de dados e a collection
db = client["meuBanco"]
collection = db["clientesCadastrados"]


# Função para apresentar todos clientes e suas informações no streamlit (opcional)
def get_data():
    items = db.clienteCadastrados.find()
    items = list(items)
    return items


data = get_data()

# Tela de cadastro do cliente
with st.form(key='Include_Cliente'):
    st.title('Cadastro de clientes')
    input_firstname = st.text_input('NOME')
    input_lastname = st.text_input('SOBRENOME')
    input_cpf = st.text_input('CPF', max_chars=11, )
    input_age = st.number_input("IDADE", format="%d", step=1)
    input_gender = st.selectbox('SEXO',
                                options=['Indefinido', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
    input_uf = st.selectbox('UF',
                            options=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                                     'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                                     'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'], index=24)
    input_email = st.text_input('DIGITE SEU E-MAIL')
    input_password = st.text_input('CRIE UMA SENHA (Min. 8 caracteres)', type='password')
    input_password_confirm = st.text_input('DIGITE NOVAMENTE A SENHA', type='password')
    input_agree = st.checkbox('Eu li e concordo com os Termos de Uso e Política de Privacidade.')
    input_button_submit = st.form_submit_button('Enviar')

# Verificando algumas condições para que o cadastro possa ser realizado
if input_button_submit and len(input_password) < 8:  # A senha deve conter no mínimo 8 caracteres
    st.write('Sua senha deve conter no mínimo 8 caracteres.')
elif input_button_submit and input_password != input_password_confirm:  # As senhas devem ser idênticas
    st.write('As senhas inseridas não são iguais.')
elif input_button_submit and not input_agree:  # É necessário concordar os Termos de Uso
    st.write('Para continuar, é necessário ler e concordar com os nossos Termos de Uso e Política de Privacidade.')
elif input_button_submit:
    st.success('Cadastro realizado com sucesso!')

    # Armazenando as informações do cliente no banco de dados
    db.clientesCadastrados.insert_one(
        {"Nome": input_firstname,
         "Sobrenome": input_lastname,
         "CPF": input_cpf,
         "Idade": input_age,
         "Sexo": input_gender,
         "UF": input_uf,
         "E-mail": input_email}
    )

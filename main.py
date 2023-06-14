import streamlit as st
from streamlit_option_menu import option_menu
from pymongo import MongoClient
from datetime import datetime

# Conectando com o MongoDB
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

# Atribuindo variáveis que correspondem ao banco de dados e a collection
db = client["meuBanco"]
collection = db["clientes"]

st.set_page_config(
    page_title=" App 8 Code",
    page_icon="desktop_computer",
    layout="centered"
)

# Barra lateral com as opções do aplicativo
with st.sidebar:
    selected = option_menu(
        menu_title="Selecione a tarefa",
        options=["Cadastrar clientes", "Gerenciar clientes"],
        icons=["person-plus-fill", "pencil-square"],
        menu_icon="cast"
    )

# Tela de cadastro do cliente
if selected == "Cadastrar clientes":
    with st.form(key='Include_Cliente', clear_on_submit=True):
        st.title('Cadastrar novo cliente')
        input_nome = st.text_input('Nome')
        input_cpf = st.text_input('CPF', max_chars=11, )
        input_rg = st.text_input('RG', max_chars=9)
        input_data_nasc = st.date_input('Data de nascimento',
                                        min_value=(datetime(1990, 1, 1)), max_value=(datetime.today()))
        input_sexo = st.selectbox('Sexo',
                                  options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
        input_mae = st.text_input('Mãe')
        input_pai = st.text_input('Pai')
        input_estado = st.selectbox('Estado',
                                    options=['', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                                             'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                                             'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'], index=0)
        input_cidade = st.text_input('Cidade')
        input_cep = st.text_input('CEP', max_chars=8)
        input_endereco = st.text_input('Endereço')
        input_numero = st.number_input('Número', step=1)
        input_bairro = st.text_input('Bairro')
        input_celular = st.text_input('Celular', max_chars=11)
        input_email = st.text_input('E-mail')
        input_senha = st.text_input('Crie uma senha (Min. 8 caracteres)', type="password")
        input_senhaConfirm = st.text_input('Digite a senha novamente', type="password")
        input_button_submit = st.form_submit_button('Enviar', disabled=False,
                                                    help='Preencha todos os campos para finalizar a inscrição',
                                                    type='primary')

        # Verificando algumas condições para que o cadastro possa ser realizado
        if input_button_submit and len(input_senha) < 8:  # A senha deve conter no mínimo 8 caracteres
            st.error('A senha deve conter no mínimo 8 caracteres')
        elif input_button_submit and input_senha != input_senhaConfirm:  # As senhas digitadas devem ser idênticas
            st.error('As senhas não eram compativeis')
        elif input_button_submit:
            st.success('Cadastro realizado com sucesso!')

            # Ajustando algumas informações para serem passadas ao banco de dados

            # Ajustando o formato da data de nascimento
            hoje = datetime.today()
            idade = hoje.year - input_data_nasc.year - (
                    (hoje.month, hoje.day) < (input_data_nasc.month, input_data_nasc.day))

            input_data_nasc = input_data_nasc.strftime("%d/%m/%Y")

            # Ajustando o formato do CPF
            if len(input_cpf) == 11:
                input_cpf = '{}.{}.{}-{}'.format(input_cpf[:3], input_cpf[3:6], input_cpf[6:9], input_cpf[9:])

            # Ajustando o formato do RG
            if len(input_rg) == 9:
                input_rg = '{}.{}.{}-{}'.format(input_rg[:2], input_rg[2:5], input_rg[5:8], input_rg[8:])

            # Ajustando o formato do CEP
            if len(input_cep) == 8:
                input_cep = '{}-{}'.format(input_cep[:5], input_cep[5:])

            # Ajustando o formato do celular
            if len(input_celular) == 9:
                input_celular = '{}-{}'.format(input_celular[:5], input_celular[5:])
            elif len(input_celular) == 11:
                input_celular = '({}) {}-{}'.format(input_celular[:2], input_celular[2:7], input_celular[7:])

            # Armazenando as informações do cliente no banco de dados
            db.clientes.insert_one(
                {"nome": input_nome,
                 "idade": idade,
                 "cpf": input_cpf,
                 "rg": input_rg,
                 "data_nasc": input_data_nasc,
                 "sexo": input_sexo,
                 "mae": input_mae,
                 "pai": input_pai,
                 "email": input_email,
                 "senha": input_senha,
                 "cep": input_cep,
                 "endereço": input_endereco,
                 "numero": input_numero,
                 "bairro": input_bairro,
                 "cidade": input_cidade,
                 "estado": input_estado,
                 "celular": input_celular
                 }
            )

# Tela de gerenciamento de clientes (pesquisa, edição e exclusão)
if selected == "Gerenciar clientes":
    tab1, tab2, tab3 = st.tabs(["Filtrar", "Resultados", "Editar/Deletar"])

    busca: [str] = [0 for x in range(3)]

    # Caso a opção "Filtrar" seja selecionada
    with tab1:

        options = st.multiselect(
            'Selecione os filtros de pesquisa (máximo 3):',
            ['idade', 'nome', 'sexo', 'estado', 'cidade', 'bairro'])

        # Determinando as opções de input de acordo com as opções de filtros selecionadas

        if len(options) == 1 and 'idade' in options:
            buscaIdade = st.slider(
                'Selecione a margem de idade:',
                0, 100, (18, 40))

            resultadof = collection.find(
                {'$and': [{'idade': {'$gte': buscaIdade[0]}}, {'idade': {'$lte': buscaIdade[1]}}]})

        elif len(options) == 1 and 'idade' not in options:
            if options[0] == 'sexo':
                busca = st.selectbox('Sexo',
                                     options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
            else:
                busca = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[0]))

            resultadof = collection.find({'{:s}'.format(options[0]): {'$regex': busca}})

        elif len(options) == 2 and 'idade' in options:
            if options[1] == 'idade':
                trade = options[0]
                options[0] = 'idade'
                options[1] = trade

            buscaIdade = st.slider(
                'Selecione a margem de idade:',
                0, 100, (18, 40))
            if 'sexo' in options:
                busca = st.selectbox('Sexo',
                                     options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
            else:
                busca = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))

            resultado = collection.find({'{:s}'.format(options[1]): {'$regex': busca}})
            resultadof = collection.find(
                {'$and': [{'{:s}'.format(options[1]): {'$regex': busca}},
                          {'idade': {'$gte': buscaIdade[0]}}, {'idade': {'$lte': buscaIdade[1]}}]})

        elif len(options) == 2 and 'idade' not in options:
            if 'sexo' in options:
                if options[1] == 'sexo':
                    trade = options[0]
                    options[0] = 'sexo'
                    options[1] = trade

                busca[0] = st.selectbox('Sexo',
                                        options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))
            else:
                busca[0] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[0]))
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))

            resultadof = collection.find(
                {'$and': [{'{:s}'.format(options[0]): {'$regex': busca[0]}},
                          {'{:s}'.format(options[1]): {'$regex': busca[1]}}]})

        elif len(options) == 3 and 'idade' in options:
            if options[1] == 'idade':
                trade = options[0]
                options[0] = 'idade'
                options[1] = trade
            if options[2] == 'idade':
                trade = options[0]
                options[0] = 'idade'
                options[2] = trade

            buscaIdade = st.slider(
                'Selecione a margem de idade:',
                0, 100, (18, 40))

            if 'sexo' in options:
                if options[2] == 'sexo':
                    trade2 = options[1]
                    options[1] = 'sexo'
                    options[2] = trade2

                busca[0] = st.selectbox('Sexo',
                                        options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[2]))
            else:
                busca[0] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[2]))

            resultadof = collection.find(
                {'$and': [{'idade': {'$gte': buscaIdade[0]}}, {'idade': {'$lte': buscaIdade[1]}},
                          {'{:s}'.format(options[1]): {'$regex': busca[0]}},
                          {'{:s}'.format(options[2]): {'$regex': busca[1]}}]})

        elif len(options) == 3 and 'idade' not in options:
            if 'sexo' in options:
                if options[1] == 'sexo':
                    trade = options[0]
                    options[0] = 'sexo'
                    options[1] = trade
                if options[2] == 'sexo':
                    trade = options[0]
                    options[0] = 'sexo'
                    options[2] = trade

                busca[0] = st.selectbox('Sexo',
                                        options=['', 'Masculino', 'Feminino', 'Prefiro não informar'], index=0)
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))
                busca[2] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[2]))
            else:
                busca[0] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[0]))
                busca[1] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[1]))
                busca[2] = st.text_input('Qual {:s} você deseja adicionar na busca:'.format(options[2]))

            resultadof = collection.find(
                {'$and': [{'{:s}'.format(options[0]): {'$regex': busca[0]}},
                          {'{:s}'.format(options[1]): {'$regex': busca[1]}},
                          {'{:s}'.format(options[2]): {'$regex': busca[2]}}]})

        # Quando o botão "Pesquisar" for pressionado, os clientes que correspondem com os filtros aparecerão em "Resultados"
        if st.button('Pesquisar'):
            with tab2:
                key = 1
                for dado in resultadof:
                    st.write(dado)

    # Caso a opção "Editar/Deletar" seja selecionada
    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            cont = 1
            nomeQuery = st.text_input('Digite o nome completo do cliente')
            if nomeQuery:
                st.write(collection.find_one({'nome': nomeQuery}))
                atualizar = st.button(':arrows_counterclockwise: Atualizar ')

        # Extraindo as informações para as alterações
        with col2:
            acao = st.selectbox('Selecione uma ação', (' ', 'Editar dados', 'Deletar cliente'))
            if acao == 'Editar dados':
                with st.form(key='Acao', clear_on_submit=True):
                    opcaoTroca = st.selectbox('Qual informação você irá alterar?', (
                        ' ', 'nome', 'cpf', 'rg', 'data_nasc', 'sexo', 'mae', 'pai', 'email', 'senha',
                        'cep', 'endereço', 'numero', 'bairro', 'cidade', 'estado', 'celular'))
                    infoAtt = st.text_input('Digite a nova informação')
                    confirma = st.form_submit_button('Confirmar ação', use_container_width=True)
                    if confirma:
                        if opcaoTroca == 'data_nasc':
                            dataWork = datetime.strptime(infoAtt, '%d/%m/%Y')
                            hoje = datetime.today()
                            idadenova = hoje.year - dataWork.year - (
                                (hoje.month, hoje.day) < (dataWork.month, dataWork.day))
                            collection.update_one({'nome': nomeQuery}, {'$set': {'idade': idadenova}})
                        collection.update_one({'nome': nomeQuery}, {'$set': {opcaoTroca: infoAtt}})

            if acao == 'Deletar cliente':
                with st.form(key='excluir'):
                    st.warning(
                        'Atenção! Ao excluir um cliente do banco de dados, não será possível recuperar os dados!')
                    st.write('Você tem certeza que deseja excluir o cliente?')
                    st.write('')
                    deletar = st.form_submit_button('Sim, tenho certeza', use_container_width=True)
                    if deletar:
                        st.info('Cliente deletado')
                        collection.delete_one({'nome': nomeQuery})

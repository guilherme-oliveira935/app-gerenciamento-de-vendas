import requests
from kivy.app import App
from urllib.parse import quote, unquote

class MyFirebase:

    API_KEY = ''
    link_cadastro = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    link_login = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    base_URL = ''
    logout_URL = F"https://identitytoolkit.googleapis.com/v1/accounts:signOut?Key={API_KEY}"


    def __init__(self):
        self.my_app = App.get_running_app()
        
    def _handle_response(self, response):
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print(f'Erro na requisição: {response.status_code}')
            return response.json()

    def cadastrar_usuario(self, email, senha, nome_usuario):
        try:
            #criar usuário
            dados = {"email": email,
                "password": senha,
                "returnSecureToken": True}
            
            requisicao = requests.post(self.link_cadastro, data=dados)
            requisicao_dic = self._handle_response(requisicao)
            nome_usuario = quote(nome_usuario)

            if 'error' in requisicao_dic:
                self.my_app.root.ids['cadastro_page'].ids['label_status'].text = f'{requisicao_dic["error"]["message"]}'
                return False
            
            else:
                self.refresh_token, self.local_id, self.id_token = requisicao_dic["refreshToken"], requisicao_dic["localId"], requisicao_dic["idToken"]

                self.headers = {'Authorization': f'Bearer {self.id_token}',
                                'Content-Type': 'application/json'}
                
                self.params = {'auth': self.id_token}

                requisicao = requests.get(f'{self.base_URL}proximo_code.json', headers=self.headers, params=self.params)
                requisicao_dic = self._handle_response(requisicao)
                code = requisicao_dic

                #criar informações default no realtime database no firebase
                info_user = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "nome_usuario": "{nome_usuario}", "codigo_compartilhavel": "#BR{code}"}}'
                requests.patch(f'{self.base_URL}{self.local_id}.json', data=info_user, headers=self.headers, params=self.params)
                
                self.my_app.local_id = self.local_id
                self.my_app.id_token = self.id_token
                self.my_app.refresh_token = self.refresh_token
                self.atualizar_code(code)
                   
        except requests.exceptions.RequestException as e:
            return print(f'Erro ao cadastrar usuário: {e}')
        
    def login_usuario(self, email, senha):
        try:     
            info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
            
            requisicao = requests.post(self.link_login, data=info)
            requisicao_dic = self._handle_response(requisicao)

            if 'error' in requisicao_dic:
                self.my_app.root.ids['login_page'].ids['label_status'].text = f'{requisicao_dic["error"]["message"]}'
                return False
            
            else:
                self.refresh_token, self.local_id, self.id_token = requisicao_dic["refreshToken"], requisicao_dic["localId"], requisicao_dic["idToken"]

                self.headers = {'Authorization': f'Bearer {self.id_token}',
                                'Content-Type': 'application/json'}
                
                self.params = {'auth': self.id_token}

                self.my_app.local_id = self.local_id
                self.my_app.id_token = self.id_token
                self.my_app.refresh_token = self.refresh_token
                self.my_app.mudar_tela('home_page')

        except requests.exceptions.RequestException as e:
            return print(f"Erro ao fazer login: {e}")
        
    def carregar_equipe(self, local_id):
        dados = self.carregar_informacoes(local_id)
        codigos_equipe = dados['equipe'].split(',')
        l = 0
        if codigos_equipe[0] != '':
            lista_dados_equipe = []
            
            for id_vendedor_equipe in codigos_equipe:
                id_vendedor_equipe_encoded = quote(f'#BR{id_vendedor_equipe}')
                requisicao = requests.get(f'{self.base_URL}.json?orderBy="codigo_compartilhavel"&equalTo="{id_vendedor_equipe_encoded}"')
                requisicao_dic = self._handle_response(requisicao)
                lista_dados_equipe.append(list(requisicao_dic.values()))
                lista_dados_equipe[l][0]['nome_usuario'] = unquote(lista_dados_equipe[l][0]['nome_usuario'])
                l += 1

            return lista_dados_equipe
        else:
            return None
        
    def carregar_informacoes(self, local_id):
        try:
            requisicao = requests.get(f'{self.base_URL}{local_id}.json', headers=self.headers, params=self.params)
            requisicao_dic = self._handle_response(requisicao)
            
            return requisicao_dic

        except requests.exceptions.RequestException as e:
            return print(f"Erro ao carregar informações: {e}")
        
    def salvar_informacoes(self, local_id, tabela, info):
        try:
            requisicao = requests.post(f'{self.base_URL}{local_id}/{tabela}.json', data=info, headers=self.headers, params=self.params)

        except requests.exceptions.RequestException as e:
            return print(f"Erro ao salvar informações: {e}")
        
    def adicionar_vendedor(self, local_id, id_vendedor):
        dados = self.carregar_informacoes(local_id)
        codigos_equipe = dados['equipe'].split(',')

        if (id_vendedor not in codigos_equipe) or id_vendedor == "":
            id_vendedor_encoded = quote(id_vendedor)
            requisicao = requests.get(f'{self.base_URL}.json?orderBy="codigo_compartilhavel"&equalTo="{id_vendedor_encoded}"')
            requisicao_dic = requisicao.json()

            if len(requisicao_dic) == 0:
                return 'USUÁRIO NÃO ENCONTRADO'
            
            else: 
            
                if codigos_equipe[0] == '':
                    equipe = id_vendedor.replace('#BR', '')
                else:
                    equipe = ','.join(codigos_equipe) + ',' + id_vendedor.replace('#BR', '')

                requests.patch(f'{self.base_URL}{local_id}.json', json={'equipe': equipe}, headers=self.headers, params=self.params)
                return True

        else:
            return 'USUÁRIO JÁ ADICIONADO'
    
    def atualizar_total_vendas(self, local_id, info):
        try:
            requisicao = requests.get(f'{self.base_URL}{local_id}/total_vendas.json', headers=self.headers, params=self.params)
            requisicao_dic = self._handle_response(requisicao)
            total_vendas = float(requisicao_dic)
            total_vendas += info
            total_vendas = str(total_vendas)

            requests.patch(f'{self.base_URL}{local_id}.json', json={'total_vendas': total_vendas}, headers=self.headers, params=self.params)

        except requests.exceptions.RequestException as e:
            return print(f"Erro ao carregar informações: {e}")
        
    def atualizar_foto_perfil(self, local_id, foto):
        try: 
            requests.patch(f'{self.base_URL}{local_id}.json', json={'avatar': foto}, headers=self.headers, params=self.params)

        except requests.exceptions.RequestException as e:
            return print(f"Erro ao carregar informações: {e}")

    def atualizar_code(self, code_usado):
        try:
            proximo_code = int(code_usado) + 1
            info = f'{{"proximo_code": "{proximo_code}"}}'

            requests.patch(f'{self.base_URL}.json', data=info, headers=self.headers, params=self.params)
            
            return self.my_app.mudar_tela('home_page')
            
        except requests.exceptions.RequestException as e:
            return print(f"Erro ao carregar informações: {e}")
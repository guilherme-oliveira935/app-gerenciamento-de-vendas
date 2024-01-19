from kivy.app import App
import telas
from botoes import *
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from myfirebase import MyFirebase
import os
from functools import partial
from datetime import date
from Bannerequipe import BannerEquipe
from Bannervendas import BannerVenda

manager = Builder.load_file('main.kv')

class VendasApp(App):
    
    def build(self):
        self.firebase = MyFirebase()
        return manager
    
    def on_start(self):
        self.adicionar_scrollview_vendas()
        data = self.data()
        data_label = self.root.ids['adicionar_vendas_page'].ids['data']
        data_label.text = f'Data: {data}'
        self.cliente = None
        self.produto = None
        self.unidade = None
    
    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela
    
    def data(self):
        data = date.today().strftime('%d/%m/%Y')
        return str(data)

    def carregar_vendas_usuario(self):
        grid_vendas_page = self.root.ids['home_page'].ids['lista_vendas']

        if grid_vendas_page.children != None:
            grid_vendas_page.clear_widgets()

        dados = self.firebase.carregar_informacoes(self.local_id)
        lista_vendas = dados['vendas']
        for chave_id in lista_vendas:
            banner_vendas = BannerVenda(cliente=lista_vendas[chave_id]["cliente"],
                                        foto_cliente=lista_vendas[chave_id]["foto_cliente"],
                                        produto=lista_vendas[chave_id]["produto"],
                                        foto_produto=lista_vendas[chave_id]["foto_produto"],
                                        data=lista_vendas[chave_id]['data'],
                                        preco=lista_vendas[chave_id]['preco'],
                                        unidade=lista_vendas[chave_id]['unidade'],
                                        quantidade=lista_vendas[chave_id]["quantidade"])
            
            grid_vendas_page.add_widget(banner_vendas)

    def carregar_todas_vendas(self):
        label_total_vendas = self.root.ids['listar_todas_vendas_page'].ids['label_total_vendas']
        grid_todas_vendas_page = self.root.ids['listar_todas_vendas_page'].ids['lista_vendas']

        if grid_todas_vendas_page.children != None:
            grid_todas_vendas_page.clear_widgets()
        

        dados_equipe = self.firebase.carregar_equipe(self.local_id)
        dados = self.firebase.carregar_informacoes(self.local_id)
        lista_venda_user = dados['vendas']

        if lista_venda_user == "":
            total_vendas = 0
        
        else:
            total_vendas = float(dados['total_vendas'])

            #carregar as vendas do usuario logado:
            for chave_id in lista_venda_user:
                banner_vendas = BannerVenda(cliente=lista_venda_user[chave_id]["cliente"],
                                            foto_cliente=lista_venda_user[chave_id]["foto_cliente"],
                                            produto=lista_venda_user[chave_id]["produto"],
                                            foto_produto=lista_venda_user[chave_id]["foto_produto"],
                                            data=lista_venda_user[chave_id]['data'],
                                            preco=lista_venda_user[chave_id]['preco'],
                                            unidade=lista_venda_user[chave_id]['unidade'],
                                            quantidade=lista_venda_user[chave_id]["quantidade"])
                
                grid_todas_vendas_page.add_widget(banner_vendas)
        if dados_equipe != None:
            #carregar as vendas da equipe:
            for dados_vendedor in dados_equipe:
                lista_vendas_vendedor = dados_vendedor[0]['vendas']
                if dados_vendedor[0]['total_vendas'] != '':
                    total_vendas_vendedor = float(dados_vendedor[0]['total_vendas'])
                    total_vendas = total_vendas_vendedor + total_vendas

                for venda in lista_vendas_vendedor:
                    banner_vendas = BannerVenda(cliente=lista_vendas_vendedor[venda]["cliente"],
                                                foto_cliente=lista_vendas_vendedor[venda]["foto_cliente"],
                                                produto=lista_vendas_vendedor[venda]["produto"],
                                                foto_produto=lista_vendas_vendedor[venda]["foto_produto"],
                                                data=lista_vendas_vendedor[venda]['data'],
                                                preco=lista_vendas_vendedor[venda]['preco'],
                                                unidade=lista_vendas_vendedor[venda]['unidade'],
                                                quantidade=lista_vendas_vendedor[venda]["quantidade"])
                    
                    grid_todas_vendas_page.add_widget(banner_vendas)

        else:
            pass

        label_total_vendas.text = f'TOTAL DE VENDAS DA EQUIPE: R${total_vendas}'

    def exibir_equipe(self):
        lista_equipe = self.firebase.carregar_equipe(self.local_id)
        if lista_equipe != None:
            grid_equipe_page = self.root.ids['listar_vendedores_page'].ids['lista_vendedores']
            if grid_equipe_page.children != None:
                grid_equipe_page.clear_widgets()
            
            for dados_vendedor in lista_equipe:
                banner_vendedor = BannerEquipe(dados_vendedor = dados_vendedor)
                grid_equipe_page.add_widget(banner_vendedor)

    def adicionar_vendedor(self, id_vendedor):
        texto = self.firebase.adicionar_vendedor(self.local_id, id_vendedor)

        if texto != True:
            self.root.ids['listar_vendedores_page'].ids['label_status'].text = f'{texto}'
            self.root.ids['listar_vendedores_page'].ids['label_status'].color = (1, 0, 0, 1)
        else:
            self.root.ids['listar_vendedores_page'].ids['label_status'].text = 'USUÁRIO ADICIONADO'
            self.root.ids['listar_vendedores_page'].ids['label_status'].color = (0, 207/255, 219/255, 1)

    def resetar_texto_equipe(self):
        self.root.ids['listar_vendedores_page'].ids['label_status'].text = ''

    def exibir_codigo(self):
        dados = self.firebase.carregar_informacoes(self.local_id)
        codigo = dados['codigo_compartilhavel']
        self.root.ids['ajustes_page'].ids['label_codigo'].text = f'CÓDIGO DE USUÁRIO: {codigo}'

    def exibir_foto_atual(self):
        dados = self.firebase.carregar_informacoes(self.local_id)
        foto_atual = dados['avatar']
        self.root.ids['mudar_foto_page'].ids['foto_atual'].source = f'icones/fotos_perfil/{foto_atual}'
        self.root.ids['ajustes_page'].ids['foto_atual'].source = f'icones/fotos_perfil/{foto_atual}'

    def exibir_total_vendas(self):
        dados = self.firebase.carregar_informacoes(self.local_id)
        total_vendas = dados['total_vendas']
        self.root.ids['home_page'].ids['label_total_vendas'].text = f'TOTAL DE VENDAS R${total_vendas}'

    def carregar_fotos_perfil(self):
        grid_fotos = self.root.ids['mudar_foto_page'].ids['lista_fotos_perfil']
        arquivo_fotos = os.listdir("icones/fotos_perfil")
        if grid_fotos.children != None:
            grid_fotos.clear_widgets()

        for imagem in arquivo_fotos:
            foto = ImageButton(source=f'icones/fotos_perfil/{imagem}',
                               on_release=partial(self.mudar_foto_perfil, imagem))
            grid_fotos.add_widget(foto)

    def mudar_foto_perfil(self, foto, *args):
        self.firebase.atualizar_foto_perfil(self.local_id, foto)
        return self.mudar_tela('home_page')

    def adicionar_scrollview_vendas(self):
        arquivos_client = os.listdir('icones/fotos_clientes')
        arquivos_products = os.listdir('icones/fotos_produtos')
        client_list = self.root.ids['adicionar_vendas_page'].ids['lista_clientes']
        product_list = self.root.ids['adicionar_vendas_page'].ids['lista_produtos']

        for foto_cliente in arquivos_client:
            imagem = ImageButton(source=f'icones/fotos_clientes/{foto_cliente}', 
                                 on_release=partial(self.pintar_texto_vendas, foto_cliente, '1'))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(),
                                font_name=f'fontes/static/Montserrat-ExtraBold.ttf',
                                on_release=partial(self.pintar_texto_vendas, foto_cliente, '1'))
            label.color = (0.024, 0.733, 0.290)

            client_list.add_widget(imagem)
            client_list.add_widget(label)
        
        for foto_produto in arquivos_products:
            imagem = ImageButton(source=f'icones/fotos_produtos/{foto_produto}',
                                on_release=partial(self.pintar_texto_vendas, foto_produto, '2'))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                font_name=f'fontes/static/Montserrat-ExtraBold.ttf',
                                on_release=partial(self.pintar_texto_vendas, foto_produto, '2'))
            label.color = (0.024, 0.733, 0.290)
            
            product_list.add_widget(imagem)
            product_list.add_widget(label)

    def pintar_texto_vendas(self, click, acao, *args):
        if acao == '1':

            label = self.root.ids['adicionar_vendas_page'].ids['label_selecione_cliente']
            label.color = (0.024, 0.733, 0.290)

            self.cliente = click.replace(".png", "").capitalize()
            lista_clientes = self.root.ids['adicionar_vendas_page'].ids['lista_clientes']
            
            for item in list(lista_clientes.children):
                try:
                    texto = item.text.lower() + ".png"
                    if click == texto:
                        item.color = (0, 207/255, 219/255, 1)
                    elif type(item) == LabelButton:
                        item.color = (0.024, 0.733, 0.290)
                except:
                    pass

        elif acao == '2':

            label = self.root.ids['adicionar_vendas_page'].ids['label_selecione_produto']
            label.color = (0.024, 0.733, 0.290)

            self.produto = click.replace(".png", "").capitalize()
            lista_produtos = self.root.ids['adicionar_vendas_page'].ids['lista_produtos']
            for item in list(lista_produtos.children):
                try:
                    texto = item.text.lower() + ".png"
                    if click == texto:
                        item.color = (0, 207/255, 219/255, 1)
                    elif type(item) == LabelButton:
                        item.color = (0.024, 0.733, 0.290)
                except:
                    pass

        else:
            self.unidade = click.replace('unidades_', '')
            page = self.root.ids['adicionar_vendas_page']

            page.ids['unidades_kg'].color = (0.024, 0.733, 0.290)
            page.ids['unidades_unidades'].color = (0.024, 0.733, 0.290)
            page.ids['unidades_litros'].color = (0.024, 0.733, 0.290)

            page.ids[click].color = (0, 207/255, 219/255, 1)

    def resetar(self):
            page = self.root.ids['adicionar_vendas_page']
            lista_clientes = page.ids['lista_clientes']
            lista_produtos = page.ids['lista_produtos']
            for item in list(lista_clientes.children):
                if type(item) == LabelButton:
                    item.color = (0.024, 0.733, 0.290)
            for item in list(lista_produtos.children):
                if type(item) == LabelButton:
                    item.color = (0.024, 0.733, 0.290)

            page.ids['unidades_kg'].color = (0.024, 0.733, 0.290)
            page.ids['unidades_unidades'].color = (0.024, 0.733, 0.290)
            page.ids['unidades_litros'].color = (0.024, 0.733, 0.290)

            page.ids['label_selecione_cliente'].color = (0.024, 0.733, 0.290)
            page.ids['label_selecione_produto'].color = (0.024, 0.733, 0.290)
            page.ids['label_preco_total'].color = (0.024, 0.733, 0.290)
            page.ids['label_quantidade_total'].color = (0.024, 0.733, 0.290)

            self.cliente = None
            self.produto = None
            self.unidade = None

            self.mudar_tela('home_page')
    
    def adicionar_venda(self, preco_total = None, quantidade_total = None):
        page = self.root.ids['adicionar_vendas_page']
        data = page.ids['data'].text.replace("Data: ", "")
        foto_produto = None
        foto_cliente = None

        if self.cliente == None:
            page.ids['label_selecione_cliente'].color = (1, 0, 0, 1)
        else:
            foto_cliente = self.cliente + ".png"
        if self.produto == None:
            page.ids['label_selecione_produto'].color = (1, 0, 0, 1)
        else:
            foto_produto = self.produto + ".png"
        if self.unidade == None:
            page.ids['unidades_kg'].color = (1, 0, 0, 1)
            page.ids['unidades_unidades'].color = (1, 0, 0, 1)
            page.ids['unidades_litros'].color = (1, 0, 0, 1)
        
        try:
            preco = float(preco_total)
        except:
            page.ids['label_preco_total'].color = (1, 0, 0, 1)
        try:
            quantidade = float(quantidade_total)
        except:
            page.ids['label_quantidade_total'].color = (1, 0, 0, 1)

        if foto_produto and foto_cliente and (self.unidade != None) and (type(preco) == float) and (type(quantidade) == float):
            info = f'{{"cliente": "{self.cliente}", "produto": "{self.produto}", "foto_cliente": "{foto_cliente}", "foto_produto": "{foto_produto}","data": "{data}", "unidade": "{self.unidade}", "preco": "{preco}", "quantidade": "{quantidade}"}}'

            valor = preco * quantidade
            self.firebase.salvar_informacoes(self.local_id, 'vendas', info)
            self.firebase.atualizar_total_vendas(self.local_id, valor)
            self.resetar()

    def log_out(self):
        self.local_id = None
        self.id_token = None
        self.refresh_token = None
        self.root.ids['login_page'].ids['email_input'].text = ''
        self.root.ids['login_page'].ids['senha_input'].text = ''
        self.mudar_tela('login_page')

if __name__ == '__main__':

    VendasApp().run()

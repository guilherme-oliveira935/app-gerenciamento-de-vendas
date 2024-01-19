from botoes import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

class BannerVenda(GridLayout):

    def __init__(self, **kwargs):
        super().__init__()
        self.rows = 1

        with self.canvas:
            Color(rgb=(0.450, 0.584, 0.282))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        if kwargs["unidade"] == 'unidades_unidades':
             unidade = kwargs["unidade"].replace('_unidades', '')
        else:
             unidade = kwargs["unidade"]

        cliente = kwargs["cliente"]
        foto_cliente = kwargs["foto_cliente"]
        produto = kwargs["produto"]
        foto_produto = kwargs["foto_produto"]
        data = kwargs["data"]
        quantidade = float(kwargs["quantidade"])
        preco = float(kwargs["preco"])

        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint= {"right": 1, "top": 0.95},
                                size_hint=(1, 0.75),
                                source=f"icones/fotos_clientes/{foto_cliente}")
        esquerda_label = Label(text=cliente, size_hint=(1, 0.2), 
                               pos_hint={"right": 1,"top": 0.2},
                               font_name='fontes/static/Montserrat-ExtraBold.ttf')
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        meio = FloatLayout()
        meio_imagem = Image(pos_hint={"right": 1, "top": 0.95},
                            size_hint=(1, 0.75),
                            source=f"icones/fotos_produtos/{foto_produto}")
        meio_label = Label(text=produto, size_hint=(1, 0.2),
                           pos_hint={"right": 1, "top": 0.2},
                           font_name='fontes/static/Montserrat-ExtraBold.ttf')
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        direita = FloatLayout()
        direita_label_data = Label(text=f"Data: {data}",
                                   size_hint=(1, 0.33),
                                   pos_hint={"right":1, "top": 0.9},
                                   font_name='fontes/static/Montserrat-ExtraBold.ttf')
        direita_label_preco = Label(text=f"Preço: R${preco:,.2f}",
                                    size_hint=(1, 0.33),
                                    pos_hint={"right": 1, "top": 0.65},
                                    font_name='fontes/static/Montserrat-ExtraBold.ttf')
        direita_label_quantidade = Label(text=f"{quantidade} {unidade}",
                                        size_hint=(1, 0.33),
                                        pos_hint={"right": 1, "top": 0.4},
                                        font_name='fontes/static/Montserrat-ExtraBold.ttf')
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size

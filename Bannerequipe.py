from botoes import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

class BannerEquipe(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        with self.canvas:
            Color(rgb=(0.450, 0.584, 0.282))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        dados_vendedor = kwargs['dados_vendedor'][0]
        
        foto = ImageButton(source=f'icones/fotos_perfil/{dados_vendedor["avatar"]}',
                            pos_hint={'right': 0.3, 'top': 0.9},
                            size_hint=(0.3, 0.8))

        total_vendas = LabelButton(text=f'TOTAL VENDAS: {dados_vendedor["total_vendas"]}',
                                pos_hint={'right': 0.9, 'top': 0.6},
                                size_hint=(0.5, 0.5),
                                bold=True,
                                font_name='fontes/static/Montserrat-ExtraBold.ttf')
        
        nome = LabelButton(text=f'NOME: {dados_vendedor["nome_usuario"]}',
                        pos_hint={'right': 0.9, 'top': 0.9},
                        size_hint=(0.5, 0.5),
                        bold=True,
                        font_name='fontes/static/Montserrat-ExtraBold.ttf')

        self.add_widget(foto)
        self.add_widget(total_vendas)
        self.add_widget(nome)
    
    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size

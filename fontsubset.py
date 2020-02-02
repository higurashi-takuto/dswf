import base64
from io import BytesIO
from fontTools.ttLib import sfnt
from fontTools.subset import Options, Subsetter, load_font


class FontSubsetter:
    '''
    フォントのサブセットに関するクラス
    args:
        font_path:
            型: str
            概要: ベースとなるフォントのパス
        options:
            型: fontTools.subset.Options
            概要: サブセットに使用するオプション
            初期値: None
        featurs:
            型: list
            概要: 引き継ぐ OpenType 機能
            初期値: ['*']（全て）
    '''
    def __init__(self, font_path, options=None, featurs=['*']):
        if not options:
            options = self.make_options(featurs)
        self.options = options
        self.font = load_font(font_path, self.options)

    '''
    オプションを生成する
    args:
        featurs:
            型: list
            概要: 引き継ぐ OpenType 機能
    return:
        options:
            型: fontTools.subset.Options
            概要: 作られたオプション
    '''
    def make_options(self, featurs):
        options = Options()
        options.recalc_bounds = True
        options.recalc_timestamp = True
        options.recalc_average_width = True
        options.recalc_max_context = True
        options.drop_tables = []
        options.passthrough_tables = True
        options.layout_features = featurs
        return options

    '''
    指定されたテキストでサブセットする（インスタンスの状態変化）
    args:
        text:
            型: str
            概要: サブセットに含む文字
    '''
    def subset(self, text):
        subsetter = Subsetter(self.options)
        subsetter.populate(text=text)
        subsetter.subset(self.font)

    '''
    フォントを埋め込んだ CSS を作成する
    args:
        class_name:
            型: str
            概要: フォントを適用するクラス名
    return:
        css:
            型: str
            概要: 作られた CSS
    '''
    def save_as_css(self, class_name):
        with BytesIO() as buff:
            sfnt.USE_ZOPFLI = False
            self.font.flavor = 'woff2'
            self.font.save(buff, reorderTables=self.options.canonical_order)
            encoded = str(base64.b64encode(buff.getvalue()), 'utf-8')
        css = (f'@font-face{{font-family:"{ class_name }";'
               f'src:url("data:application/font-woff;charset=utf-8;base64,'
               f'{ encoded }")format("woff2");}}.{ class_name }'
               f'{{font-family: "{ class_name }";}}')
        return css

    '''
    フォントを閉じる
    '''
    def close(self):
        self.font.close()

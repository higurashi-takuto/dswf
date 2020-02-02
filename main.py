from flask import Flask, render_template, make_response, request, redirect
from fontsubset import FontSubsetter


'''
Flask のインスタンス生成
static_folder: str
               静的なリソースのパス
               今回は同ルートの js

CORS 対応する場合
    必要ライブラリのインストール
    $ pip install flask-cors

    追加コーディング
    CORS(app)
'''
app = Flask(__name__, static_folder='js')

'''
見本用のトップページ
ページのルーティング: /
                  トップページなのでルートを指定
'''
@app.route('/')
def index():
    return render_template('index.html')


'''
サブセットの処理する API 部分（今回は内部からしか使われず、単体機能なのであまり API 感はないが…）
ページのルーティング: /
                  トップページなのでルートを指定
'''
@app.route('/subset', methods=['GET', 'POST'])
def subset():
    # POST を受け取った場合
    if request.method == 'POST':
        # リクエストからフォントサブセットに必要なパラメータを取得
        name = request.form['name']
        family = request.form['family']
        style = request.form['style']
        content = request.form['content']
        # フォントをサブセット化し、CSS を作成
        font_path = f'{ family }/{ family }-{ style }.otf'
        fs = FontSubsetter(font_path)
        fs.subset(content)
        css = fs.save_as_css(name)

        # レスポンスを作成し、返す
        response = make_response()
        response.mimetype = 'text/css'
        response.data = css
        return response
    # GET だった場合はトップページへリダイレクト
    else:
        return redirect('/')


# プログラム実行時にサーバを立てる
if __name__ == "__main__":
    # ホストをグローバル向けにし、並列処理を有効化
    app.run(host='0.0.0.0', threaded=True)

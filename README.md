# Dynamic Subsetting of Web Fonts

ダイナミックサブセッティング Web フォント

[動作デモページ](https://dswf.hgrs.me)

## サーバサイド
### 主なコード
- Web サーバ: [`main.py`](main.py)
- フォントのサブセット: [`fontsubset.py`](fontsubset.py)

### 使い方
1. `/subset` に対して `name, family, style, content` を含む POST を行います。
    - `name`: HTML に付与されたクラス名
    - `family`: 適用するフォント名
    - `style`: 太さ・スタイル名
    - `content`: 含める文字
2. フォントが埋め込まれた CSS をレスポンスとして返還します。

## クライアントサイド
### 主なコード
- メインの処理を行う JavaScript: [`js/subsetter.js`](js/subsetter.js)

### 使い方
1. `js/subsetter.js` 内、1行目の URL を動作させるサーバのドメインに変更します。
1. Web フォントを適用したい HTML ファイル内の `<head>` 内で JavaScript のコードを読み込みます。<br>`<script src="https://example.com/js/subsetter.js"></script>`
1. Web フォントを適用したい文字列に対して任意の名前の `class` を付与します。
1. `class` の付与された部分の DOM ツリーが読み込まれた後に、JavaScript で `getFont('class名', 'フォント名', '太さ・スタイル名')` を実行します。
1. フォントが反映されます。

### コーディング例
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <!-- JavaScript を読み込み（ドメインは適当なものに変更） -->
  <script src="https://example.com/js/subsetter.js"></script>
  <!-- ユーザが書く必要のある JavaScript -->
  <script>
    window.onload = function() {
      // フォントの指定
      getFont('serif', 'SHSserif', 'Regular');
    }
  </script>
</head>
<body>
  <!-- getFont() で指定しするクラスを付与 -->
  <h1 class="serif">ネットワークプログラミング特論 DEMO</h1>
</body>
</html>
```

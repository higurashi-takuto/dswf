const URL = 'https://dswf.hgrs.me/subset';

/*
head タグに入力された CSS を追加する
content:
  型: str
  概要: 追加する CSS
*/
function addStyle(content) {
  // style タグを作成
  const style = document.createElement('style');
  // CSS を作成・追加
  const css = document.createTextNode(content);
  style.appendChild(css);
  document.head.appendChild(style);
}

/*
サブセットを行う API（今回は同一サーバ内）にリクエストを行う
className:
  型: str
  概要: 指定されたフォントを指定するクラス名称
fontFamily:
  型: str
  概要: 適用するフォントのファミリー名
fontStyle:
  型: str
  概要: 適用するフォントのスタイル名
content:
  型: str
  概要: サブセットに含める文字列（重複可）
*/
const subsetter = function(className, fontFamily, fontStyle, content){
  return new Promise(function(resolve){
    // XMLHttpRequest を用いて POST する
    const xhr = new XMLHttpRequest();
    xhr.open('POST', URL, true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    const query = 'name=' + className + '&' +
                  'family=' + fontFamily + '&' +
                  'style=' + fontStyle + '&' +
                  'content=' + content;
    xhr.send(query);
    // 返答に対する反応
    xhr.onreadystatechange = function() {
      if(xhr.readyState === 4 && xhr.status === 200) {
        resolve(xhr.responseText);
      }
    }
  });
}

/*
フォントを適用する（ユーザはこの関数のみ呼び出せば良い）
className:
  型: str
  概要: 指定されたフォントを指定するクラス名称
fontFamily:
  型: str
  概要: 適用するフォントのファミリー名
fontStyle:
  型: str
  概要: 適用するフォントのスタイル名
*/
function getFont(className, fontFamily, fontStyle) {
  // 指定されたタグで使用されている文字列の取得
  let text = '';
  const elements = document.getElementsByClassName(className);
  for( const element of elements ) {
      text += element.innerHTML;
  }
  // 上記2つの関数を用いてフォントを取得とスタイルの適用
  const content = encodeURIComponent(text);
  subsetter(className, fontFamily, fontStyle, content)
  .then(function(response) {
    addStyle(response);
  });
}

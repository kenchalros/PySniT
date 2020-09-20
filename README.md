# PySniT
vscodeのPythonスニペットを管理するCLIです。

### requires
- mac（現状はmacのみ対応です。）
- python3.6~（3.6未満でも動作するかもしれませんが、確認していません。）

### 注意点
このライブラリは、vscodeのスニペット設定ファイル（`python.json`）を書き換えます。**必要であれば事前にバックアップをとっておいてください。**
macの場合、下記ディレクトリ配下にスニペット設定ファイルが配置されています。
```
~/Library/Application Support/Code/User/snippets/
```

### 概要
- **任意の関数、クラス**を**スニペットとして登録**することができます。
- スニペットに登録したい関数、クラスに**デコレータを記述するだけ**でスニペットとして抽出します。デコレータを付与するだけなので、**関数、クラスへのテストを実行できます**！
- **スニペット管理用ファイルを用意してコマンドを実行**するだけで、エディターのスニペット設定を更新できるので、直接スニペット設定ファイルを編集しなくてすみます。

### 使い方
ここでは、スニペット管理プロジェクトをpipenvを用いて構築する例を示します。
#### step1 pysnitライブラリのインストール
プロジェクト用ディレクトリ作成後、本ライブラリをインストールします。  
```shell
# スニペット管理用ディレクトリを作成
$ mkdir python-snippet
$ cd python-snippet

# python3.6でプロジェクト作成
$ pipenv --python 3.6
# pysnitのインストール
$ pipenv install git+https://github.com/kenchalros/PySniT.git#egg=pysnit
# 仮想環境に入る
$ pipenv shell
```

#### step2 snippetデコレータを記述
スニペットに登録したい関数またはクラスを用意します。  
ここでは`sample.py`という名前でファイルを作成し、関数を定義します。  
また、pysnitからsnippetモジュールをインポートし、スニペットに登録したい関数をデコレートします。  
`snippet`デコレータには、`name`、`prefix`、`description`を指定することができます。ここでは`prefix`のみを指定しています。
```python
# sample.py
from pysnit import snippet

@snippet(prefix='hw')
def hello_world():
    print('hello world')
```

#### step3 スニペット管理用ファイルの準備
snippet管理用ファイルを作成します。  
`snippet.toml`というファイル（デフォルトでこの名前の設定ファイルを読み込みこんで設定します）を作成し、登録したい関数、クラスが含まれたファイルへのパスを記述します。その際、セクションの名前は`[module]`である必要があるので注意してください。  
なお、モジュールとして管理できないインライン形式のスニペットを直接記述することができます。セクションの名前は`[module]`以外であれば何でもOKです。
```toml
[module]
sample = './sample.py'
# 他にもモジュールがある場合はこのセクション内に続けて記述する

[printf]
prefix = 'pf'
body = ["print('$1'.format($2))"]
```
現状のプロジェクトディレクトリは下記のようになっています。
```text
python-snippet/
   - sample.py
   - snippet.toml
```

#### step4 スニペットの登録
`snippet.toml`ファイルの準備ができたら、`pysnit snpt`コマンドを実行します。  
デフォルトでは、カレントディレクトリにある`snippet.toml`ファイルを読み込むようになっているので、今回の例ではプロジェクトのルートでコマンドを実行してください。
```shell
$ pysnit snpt
...
```
特に問題がなければスニペットが登録されているはずです!  

# Azure Functions in Python
  

## Getting Started

### Project Structure

プロジェクトのメインフォルダには、以下のファイルを格納することができます：

* *function_app.py*：ファンクションとそのトリガー、バインディングはここで定義されます。
* *local.settings.json*：ローカルで実行する際に、アプリの設定や接続文字列を保存するために使用します。このファイルはAzureに公開されません。
* *requirements.txt*： Azureへの公開時にシステムがインストールするPythonパッケージのリストが格納されています。
* *host.json*： 関数アプリインスタンス内のすべての関数に影響する設定オプションが含まれています。このファイルは、Azureにパブリッシュされます。ローカルで実行する場合、すべてのオプションがサポートされるわけではありません。
  
## 参考資料
* [Azure Functions Developer Python Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level)  
* [quickstart](https://aka.ms/fxpythonquickstart)  
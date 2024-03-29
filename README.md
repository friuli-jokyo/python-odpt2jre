# python-odpt2jre
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

ODPT形式の鉄道運行情報をJR東日本風に変換

## Installation

このリポジトリを直接インストールします。自動的に[odpt-train-info](https://github.com/friuli-jokyo/python-odpt-train-info)もインストールされます。
```bash
pip install git+https://github.com/friuli-jokyo/python-odpt2jre
```

## Example

ソースコードは[/example.py](/example.py)に記載。

```python
>>> import odpt2jre

# ODPT形式運行情報のキャッシュ保存先を指定(デフォルトは"./__odptcache__/")
>>> odpt2jre.set_odpt_cache_dir("./__odptcache__/")

# JR東日本形式運行情報のキャッシュ保存先を指定(デフォルトは"./__jrecache__/")
>>> odpt2jre.set_jre_cache_dir("./__jrecache__/")

# 公共交通オープンデータセンターのconsumerKeyをセット(.env等を用いて環境変数"ODPT_CENTER_TOKEN"を設定すればここでセットする必要はありません)
>>> odpt2jre.Distributor.ODPT_CENTER.set_consumer_key("xxxxxxxxxxxx")

# JR東日本形式運行情報のキャッシュを更新(内部でODPT形式運行情報のキャッシュ更新も行われています)
>>> odpt2jre.refresh_cache()

# キャッシュからJR東日本形式の運行情報を取得
>>> info = odpt2jre.fetch_info()
>>> print(info[0])
{
   "lineName": {
      "id": "TWR.Rinkai",
      "ja": "りんかい線",
      "en": "Rinkai Line"
   },
   "cause": None,
   "direction": {
      "id": "inbound_and_outbound",
      "ja": "上下線",
      "en": "Inbound and outbound lines",
      "ko": "상하행선",
      "zh-Hans": "上下行线",
      "zh-Hant": "上下行線"
   },
   "section": {
      "ja": "全線",
      "en": "All lines",
      "ko": "전선",
      "zh-Hans": "全线",
      "zh-Hant": "全線"
   },
   "infoStatus": {
      "id": "NORMAL",
      "ja": "平常運転",
      "en": "Normal operation",
      "ko": "평상시 운행",
      "zh-Hans": "正常运行",
      "zh-Hant": "正常運行"
   },
   "infoStatusIcon": "CIRCLE",
   "infoText": {
      "ja": "りんかい線は、平常運転しています。",
      "en": "The Rinkai Line has normal operation."
   },
   "rawText": {
      "ja": ""
   },
   "causeTime": None,
   "resumeTime": None,
   "date": "0000-00-00T00:00:00+09:00",
   "valid": "0000-00-00T00:00:00+09:00"
}
```

## License

[MIT](LICENSE)

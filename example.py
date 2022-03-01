import odpttraininfo as odpt
import odpt2jre

# ODPT形式運行情報のキャッシュ保存先を指定(デフォルトは"./__odptcache__/")
odpt.cache.set_cache_dir("./path/to/cache/directory/")

# JR東日本形式運行情報のキャッシュ保存先を指定(デフォルトは"./__jrecache__/")
odpt2jre.cache.set_cache_dir("./path/to/cache/directory/")

# 公共交通オープンデータセンターのconsumerKeyをセット
odpt.Distributor.ODPT_CENTER.set_consumer_key("xxxxxxxxxxxx")

# JR東日本形式運行情報のキャッシュを更新(内部でODPT形式運行情報のキャッシュ更新も行われています)
odpt2jre.refresh_cache()

# キャッシュからJR東日本形式の運行情報を取得
info = odpt2jre.fetch_info()
print(info[0])
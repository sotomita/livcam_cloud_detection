#! /usr/bin/env python3


cameradata_dir_list = [
    "./input/livecamera1/test_data/09",
    "./input/livecamera1/test_data/10",
]  # 元データのディレクトリ
output_dir = "./output"  # 出力ディレクトリ
mask_dir = f"{output_dir}/mask"  # マスク画像の出力ディレクトリ
background_dir = f"{output_dir}/background"  # 背景画像の出力ディレクトリ
result_dir = f"{output_dir}/result"  # 結果画像の出力ディレクトリ
x_start, x_end = 10, 2262  # 切り出し範囲（x座標）
y_start, y_end = 10, 1000  # 切り出し範囲（y座標）
history = 200  # 背景差分の履歴フレーム数
varThreshold = 50  # 背景差分のしきい値
contour_area_max = 500  # 輪郭の最小面積（これ以下の輪郭は無視される）

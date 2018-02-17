import numpy as np
import pickle
import re

# フォントの情報を読み込む
font_sjislall_path = "data/font_data.txt" # 変換元となるデータ

font_sjisall = []
with open(font_sjislall_path, 'r') as f:
    for line in f:
        font_sjisall.append(line.strip('\n'))

# 数値文字参照をデコードする
def sjis2uni(s):
    cs = []
    for e in re.findall("&#([0-9a-fA-F]+);", s):
        # cs.append(chr(int(e, 16)))
        cs.append(chr(int(e, 10)))
    return "".join(cs)


def str2uni(str):
    while True:
        matchOB = re.search("&#([0-9a-fA-F]+);", str)
        if matchOB == None: break
        str = str[:matchOB.start()] + sjis2uni(matchOB.group()) + str[matchOB.end():]
    return str


uni_list = []
for line in font_sjisall:
    uni_list.append(str2uni(line))


# フォント情報を画像リストに変換
def zeroone2npy(list):
    """

    :param list: 18行のテキストのリスト
    :return: 文字画像(bool)のnp array. shape=[16, 文字幅]
    """
    char = []
    for i in range(len(list)):
        line = []
        for j in range(len(list[i])):
            line.append(bool(int(list[i][j])))
        char.append(line)
    char = np.array(char)
    return char


num_char = int(len(uni_list)//18)
char_dict = {} # {文字: 文字画像}の辞書
for i in range(num_char):
    char = uni_list[i * 18]
    char_arr = zeroone2npy(uni_list[i*18+2:i*18+18])
    char_dict[char] = char_arr

# 保存
def picklesave(data, path):
    with open(path, mode='wb') as f:
        pickle.dump(data, f)


picklesave(char_dict, "data/char_dict.pkl")
print("saved:", "data/char_dict.pkl")
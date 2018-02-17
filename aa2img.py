import numpy as np
import pickle
from PIL import Image
import os, glob
import re


def sjis2uni(s):
    cs = []
    for e in re.findall("&#([0-9a-fA-F]+);", s):
        # cs.append(chr(int(e, 16)))
        cs.append(chr(int(e, 10)))
    return "".join(cs)


def str2uni(str):
    while True:
        matchOB = re.search("&#([0-9a-fA-F]+);", str)
        if matchOB==None: break
        str = str[:matchOB.start()] + sjis2uni(matchOB.group()) + str[matchOB.end():]
    return str


def pickleload(path):
    """
    pickleファイルを読み込む
    :param path:
    :return:
    """
    with open(path, mode='rb') as f:
        data = pickle.load(f)
    return data


def calc_width(str, char_dict):
    """
    文字列の幅を計算する
    :param str: 文字列
    :param char_dict: 文字の辞書
    :return: 文字幅
    """
    width = 0
    for i in range(len(str)):
        try:
            width += char_dict[str[i]].shape[1]
        except:
            print("辞書に含まれない文字です", str[i])
    return width


def aa2img(input_path, output_path, char_dict):
    """
    AAを画像に変換する
    :param input_path: 変換するAA(.txt)のパス
    :param output_path: 出力する画像(.png)のパス
    :param char_dict: 文字の辞書
    :return:
    """
    aa_text = []
    with open(input_path, 'r') as f:
        for line in f:
            aa_text.append(line.strip('\n'))

    for k, v in enumerate(aa_text):
        if k==0:
            max_width = calc_width(v, char_dict)
        else:
            max_width = max(max_width, calc_width(v, char_dict))

    aa_image = np.ones([18*len(aa_text), max_width], np.uint8) * 255
    for h, line in enumerate(aa_text):
        w = 0
        for char in line:
            char_width = char_dict[char].shape[1]
            char_img = 255 - char_dict[char].astype(np.uint8) * 255
            aa_image[h*18:h*18+16, w:w+char_width] = char_img
            w += char_width

    aa_image = Image.fromarray(aa_image)
    aa_image.save(output_path)
    print("saved:", output_path)


def aa_list2img(aa_list, output_path, char_dict):
    """
    AAを画像に変換する
    :param input_path: リストで表したAA
    :param output_path: 出力する画像(.png)のパス
    :param char_dict: 文字の辞書
    :return:
    """
    for k, v in enumerate(aa_list):
        if k==0:
            max_width = calc_width(v, char_dict)
        else:
            max_width = max(max_width, calc_width(v, char_dict))

    aa_image = np.ones([18*len(aa_list), max_width], np.uint8) * 255
    for h, line in enumerate(aa_list):
        w = 0
        for char in line:
            char_width = char_dict[char].shape[1]
            char_img = 255 - char_dict[char].astype(np.uint8) * 255
            aa_image[h*18:h*18+16, w:w+char_width] = char_img
            w += char_width

    aa_image = Image.fromarray(aa_image)
    aa_image.save(output_path)
    print("saved:", output_path)


def aas2imgs(load_dir, save_dir, char_dict, tail):
    aa_path_list = glob.glob(load_dir + "*237.txt")
    for aa_path in aa_path_list:
        aa2img(aa_path, save_dir, char_dict, tail)


def ast2pngs(input_path, output_dir, char_dict):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    print('convert AST to PNGs. save dir: ', output_dir)
    # ASTファイル読み込み
    txt_list = []
    with open(input_path, 'r') as f:
        for line in f:
            txt_list.append(line.strip('\n'))

    # 数値文字参照をデコード
    uni_list = []
    for line in txt_list:
        uni_list.append(str2uni(line))

    # AAのリスト作成
    aa_list = []
    for i, line in enumerate(uni_list):
        if i==0:
            aa=[]
        elif line[:5] == '[AA][' and line[-1:]==']':
            aa_list.append(aa)
            aa = []
        else:
            aa.append(line)

    # 各AAをPNGに変換
    for i, aa in enumerate(aa_list):
        aa_list2img(aa, os.path.join(output_dir, str(i)+".png"), char_dict)


def mlt2pngs(input_path, output_dir, char_dict):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    print('convert MLT to PNGs. save dir: ', output_dir)
    # MLTファイル読み込み
    txt_list = []
    with open(input_path, 'r') as f:
        for line in f:
            txt_list.append(line.strip('\n'))

    # 数値文字参照をデコード
    uni_list = []
    for line in txt_list:
        uni_list.append(str2uni(line))

    # AAのリスト作成
    aa_list = []
    for i, line in enumerate(uni_list):
        if i==0:
            aa=[]
        elif i==len(txt_list)-1:
            aa_list.append(aa)
        elif line == '[SPLIT]':
            aa_list.append(aa)
            aa = []
        else:
            aa.append(line)
    # 各AAをPNGに変換
    for i, aa in enumerate(aa_list):
        aa_list2img(aa, os.path.join(output_dir, str(i)+".png"), char_dict)

def example_aa2img():
    char_dict = pickleload("data/char_dict.pkl")
    aa2img("data/sample.txt", "data/sample.png", char_dict)

def example_aas2imgs():
    load_dir = "data/text_selected/"
    save_dir = "data/tmp/"
    char_dict_path = "data/char_dict.pkl"
    char_dict = pickleload(char_dict_path)
    tail = "line"
    tail = "orig"
    aas2imgs(load_dir, save_dir, char_dict, tail)


def example_ast2png():
    char_dict = pickleload("data/char_dict.pkl")
    print(char_dict['\u2003'])
    mlt2pngs("data/sample.mlt", "data/output3", char_dict)

def main():
    char_dict = pickleload("data/char_dict.pkl")
    mlt_path = "data/sample.mlt" # 変換するMLTファイルを指定
    output_dir = "data/output" # 出力するフォルダを指定
    mlt2pngs(mlt_path, output_dir, char_dict)


if __name__=='__main__': main()
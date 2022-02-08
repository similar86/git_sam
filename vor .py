import cv2
import numpy as np
import itertools

from numpy.core.fromnumeric import shape


"""
jpgからpngにしたため値が0,255になっていない可能性がある画像を0,255にするメソッド
*二値化のようなもの
img : モノクロ画像
"""
def thou_img(img):
    img = np.where(img >= 200, 255 ,0)
    return img


"""
選んだ画像（白黒）の白い部分がどのぐらいあるか確認する
img : モノクロ画像
"""
def count_white(img):
    menseki = 0
    width,height = img.shape
    for i in range(width):
        for k in range(height):
            white_image = img[i][k]
            if white_image == 255:
                menseki += 1
    return menseki

"""
黒い画像を作成するメソッド
img : モノクロ画像
"""
def create_black(img):
    h , w  =img.shape
    black = np.zeros((h,w),np.uint8)
    return black
"""
白い画像を作成するメソッド
img : モノクロ画像
"""
def create_white(img):
    h , w = img.shape
    white = np.ones((h,w),np.uint8)
    return white


"""
listに格納された中身の組み合わせの全パターンをtuple型で返すメソッド
返り値はtupple型ではなくint型で返す
"""
def combi(list):
    for balls in itertools.combinations(list, 2):
        img = balls[0]
        img2 = balls[1]
    return img ,img2

"""
重なった部分を消すメソッド
map : 重なっているか判別する画像
img1 : 重なっていたら消したい画像1
img2 : 重なっていたら消したい画像2
"""
def delete_map(map,img1 ,img2):
    result1 = np.where(map == 255, 0, img1)
    result2 = np.where(map == 255, 0, img2)
    return result1 , result2

"""
重なった部分を消すメソッド
map : 重なっているか判別する画像
img1 : 重なっていたら消したい画像
"""
def delete_one_map(map,img1 ):
    result1 = np.where(map == 255, 0, img1)
    return result1

"""
境界線を出すメソッド
kernel : カーネルサイズ
img : モノクロ画像
"""
def write_border(kernel,img):
    img = np.uint8(img)
    img = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
    return img


"""
mask画像から重心を求める
gray : モノクロ画像
"""
def cal_monent(gray):
    _, contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxCont=contours[0]
    for c in contours:
        if len(maxCont)<len(c):
            maxCont=c
    mu = cv2.moments(maxCont)
    y, x= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    return x,y

"""
白い部分があるかを判断する関数
img : モノクロ画像
"""
def check_white(img):
    count = 0
    for i in range(img.shape[0]):
        for k in range(img.shape[1]):
            check = int(img[i][k])
            if check == 255:
                count = 1
                break
        if count == 1:
            break
    if count == 1:
        return True
    else:
        return False
"""
白い部分を出すメソッド
"""
def over_lap(img1,black):
    black = np.where(img1 >= 200,img1,black)
    return black


"""
where関数を使って形状マスクと重心がどれほど重なっているのか確認するメソッド
share 形状マスク画像
img 重心が白くなっている画像
"""
def check_where(share,img):
    img = np.where(img >= 200 ,share,img)
    return img

"""
画像を膨張するためのメソッド
ker カーネル
img 膨張させたい画像
"""
def dil_img(ker,img):
    dil = cv2.dilate(img,ker,iterations=1)
    return dil


if __name__ == "__main__":
    f1 = 0
    fl2 = 0
    ker8 = np.ones((3,3),np.uint8)
    ker4 = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
    share = cv2.imread(input("input size:"),0)
    obj = int(input("input object number:"))
    mask_num = 1
    black = create_black(share)
    over_map = create_black(share)
    white = create_white(share)
    h , w  =share.shape
    total = h * w 
    max_menseki = 0
    co = 0
    gra_x_list = []
    gra_y_list = []
    

    #マスク画像をリストに格納する
    for i in range(obj):
        if i == 0:
            img_list = [cv2.imread(input("input mask image:"),0)]
            if mask_num == 1:
                img_list[0].astype(np.uint8)
                check_point = thou_img(img_list[0])
                point_list = [check_point]
        else:
            img_list.append(cv2.imread(input("input image:"),0))
            img_list[i] = img_list[i].astype(np.uint8)
            if mask_num == 1:
                check_point = thou_img(img_list[i])
                point_list.append(check_point)
                

    """
    ここから膨張を繰り返す処理の始まり
    point_list : 膨張させる画像
    lap_list : 重複した部分を格納するlist 
    f1 : 膨張させていって切り取り領域まで膨張させたら+1する
    """
    idx1 = 0
    idx2 = 0
    idx_1 = 0
    idx_2 = 0
    _leng = len(point_list)* -1
    len1 = len(point_list) - 1
    r = 1
    r2 = 1
    menseki = 0
    lap_ = 0
    while True:
        #sipmeの場合はそのまま膨張させるために代入
        if mask_num == 1:
            f1 = obj
        #全て膨張したものが形状に入ったらこっちに行く
        if f1 == obj :
            _leng = len(point_list)* -1
            len1 = len(point_list) - 1
            r = 1
            r2 = 1
            #全ての画像を一緒に膨張させる
            for vc in range(obj):
                if co % 2 == 0:
                    point_list[vc] = np.uint8(point_list[vc])
                    point_list[vc] = cv2.dilate(point_list[vc],ker4,iterations=1)
                else:
                    point_list[vc] = np.uint8(point_list[vc])
                    point_list[vc] = cv2.dilate(point_list[vc],ker8,iterations=1)
            #一つ一つ重なっているところがないか確認
            for h in range(len(list(itertools.combinations(point_list, 2)))):
                if len(point_list) >= 2:
                    idx1 = _leng 
                    idx2 = _leng + r
                    if len1 == r:
                        len1 -= 1
                        r = 0
                        _leng += 1
                    for h2 in range(len(list(itertools.combinations(point_list, 2)))):
                        if len1 == r2 - 1:
                            len1 -= 1
                            r2 = 1
                            _leng += 1
                        idx_1 = _leng 
                        idx_2 = _leng + r2    
                        over_map = cv2.bitwise_and(point_list[idx_1],point_list[idx_2])
                        if check_white(over_map):
                            point_list[idx_1] , point_list[idx_2] = delete_map(over_map , point_list[idx_1] , point_list[idx_2])
                        r2 += 1                        
                        if h2 == len(list(itertools.combinations(point_list, 2))) - 1:
                            _leng = len(point_list)* -1
                            len1 = len(point_list) - 1
                            r2 = 1
                else:
                    img1 = point_list[idx1]
                    img2 = point_list[idx2]
                    over_map = np.where(img1 >=200,img2,0)
                    point_list[idx1] , point_list[idx2] = delete_map(map,img1 ,img2) 
            co += 1
            for i in range(len((point_list))):
                point_list[i] = cv2.morphologyEx(point_list[i],cv2.MORPH_OPEN,ker8)
                menseki = menseki + count_white(point_list[i]) + count_white(over_map)

            print("menseki ="+str(menseki))
            if max_menseki < menseki:
                max_menseki = menseki
            elif max_menseki == menseki :
                fl2 += 1
                print()
                print("fl2 = ",fl2)
                for i in range(len(point_list)):
                    border = write_border(ker4,point_list[i])
                    black = over_lap(border , black)
                    lap = np.where(share >= 200 , point_list[i] , share)
            if fl2 >= 5: 
                for i in range(len(point_list)):
                    border = write_border(ker4,point_list[i])
                    black = over_lap(border , black)
                    cv2.imwrite("vor.png",black)
                break
            else:
                menseki = 0
            r += 1
           
        
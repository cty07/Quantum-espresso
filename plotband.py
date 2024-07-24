# 引入必要的函式庫
import numpy as np

# 開啟 'bd.dat' 檔案
feig = open('bd.dat')

# 讀取文件的第一行
l = feig.readline()

# 從第一行中提取能帶數目和k點數目
nbnd = int(l.split(',')[0].split('=')[1])
nks = int(l.split(',')[1].split('=')[1].split('/')[0])

# 設定一些參數
ymin = -5
ymax = 5
#nband = 4  # 這是僅適用於絕緣體的價帶編號
dline = 30  # 垂直線的間隔
fmenergy=-0.9133

# 創建一個二維數組，用於存儲能帶數據
eig = np.zeros((nks, nbnd), dtype=float)

# 逐行讀取文件並填充eig數組
for i in range(nks):
    l = feig.readline()
    count = 0
    if nbnd % 10 == 0:
        n = nbnd // 10
    else:
        n = nbnd // 10 + 1
    for j in range(n):
        l = feig.readline()
        for k in range(len(l.split())):
            eig[i][count] = l.split()[k]
            count = count + 1

# 關閉文件
feig.close()

# 引入Matplotlib庫並設置繪圖環境
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# 創建一個子圖
p1 = plt.subplot(1, 1, 1)

# 設置圖形大小和線寬度
F = plt.gcf()
F.set_size_inches([8, 5])
lw = 1.2  # 線寬

# 設置x軸和y軸範圍
plt.xlim([0, nks - 1])  # 201個點
plt.ylim([ymin, ymax])

# 設置y軸標籤
plt.ylabel(r' E (eV) ', fontsize=16)

# 繪製能帶圖
x=[]
for i in range(nbnd):
    line1 = plt.plot(eig[:, i]-fmenergy , color='r', linewidth=lw)
    x.append(eig[:, i]-fmenergy)

# 将列表中的所有数组堆叠成一个二维数组
x_array = np.vstack(x)

# 使用条件筛选找到大于 0 的元素
positive_values = x_array[x_array > 0]
negative_values = x_array[x_array < 0]

# 找到大于 0 的元素中的最小值
cbm = np.min(positive_values)
vbm = np.max(negative_values)
plt.axhline(y=0,color='black',linewidth=1)
if fmenergy !=0:
    plt.title("Band gap=" + str(cbm-vbm)[0:5] + " eV")

# 在指定的點添加垂直線
vline = dline
while vline < nks - 1:
    plt.axvline(x=vline, ymin=ymin, ymax=ymax, linewidth=lw, color='black')
    vline = vline + dline

    # 設置x軸刻度標籤
# 設置x軸刻度標籤
plt.xticks((0, 30, 60, 90, 120, 150, 180, 210), ( r'${\Gamma}$','M', 'K', r'${\Gamma}$', 'A', 'L', 'H', 'A'))

# 將圖形保存為 'pwband.png' 文件，並設置dpi
plt.savefig('pwband-soc.png', dpi=500)



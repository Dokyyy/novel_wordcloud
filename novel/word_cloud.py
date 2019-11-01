import tkinter

from wordcloud import WordCloud,ImageColorGenerator
import jieba
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


global fileName  #选定文件名称
global filePath  #文件路径
global stopword_flag # 是否去除停用词标记，0表示保留停用词，1表示去除停用词，初始化为0
stopword_flag = 1
fileName = ''   #初始化

#选择文件
def FILE_SELECT():

    root = Tk()
    root.withdraw()       # 将Tkinter.Tk()实例隐藏
    default_dir = os.path.dirname(os.path.realpath(__file__)) + '\data\\'
    global filePath
    filePath = askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    print('file:', filePath)
    temp = filePath.split('/')
    file = temp[-1:][0]
    temp = file.split('.')
    global fileName
    fileName = temp[0]
    label_data.config(text = '选择文件: '+ fileName)

#保留停用词
def SAVE_STOPWORDS():
    global stopword_flag
    stopword_flag = 0

#去除停用词
def DELETE_STOPWORDS():
    global stopword_flag
    stopword_flag = 1

def make_wordcloud():

    cur_path = os.path.dirname(__file__)  # 当前路径
    # 停用词
    global stopword_flag
    stopwords = []
    if stopword_flag == 1: #去除停用词
        for word in open(os.path.join(cur_path, 'stopwords.txt'), 'r', encoding='utf-8'):
            stopwords.append(word.strip())

    # print('path: ',path.join(cur_path, './replies', file), encoding='utf-8'))

    # 读取的文本,，未去除停用词
    global filePath
    text = open(filePath, encoding='utf-8').read()
    article = jieba.cut(text)

    jbText = ''
    for word in article:
        if word not in stopwords:
            jbText += word + ' '

    imgMask = np.array(Image.open(os.path.join(cur_path, './images', 'msk.png')))  # 读入背景图片
    wc = WordCloud(
        background_color = 'white',
        max_words = 500,
        font_path = 'msyh.ttc',  # 默认不支持中文
        mask = imgMask,  # 设置背景图片
        random_state = 30  # 生成多少种配色方案
    ).generate(jbText)
    ImageColorGenerator(imgMask)  # 根据图片生成词云颜色
    wc.to_file(os.path.join(cur_path, './images', fileName + '.png'))
    print('成功保存词云图片！')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    print(1)



def exit_sc():
    sc.destroy()

# 关于
def about():
    info = '''
这是一个词云分析平台，用户可自行选择
文本文档进行词云分析，在选定文本文档
之后，可以生成相应的词云图片展示且对
图片进行保存.'''
    messagebox.showinfo('关于', info)


# 使用方法
def use():
    info = '''
在菜单栏中选择分析文本
点击RUN开始运行程序
点击EXTI或菜单栏<退出>终止程序'''
    messagebox.showinfo('使用方法', info)

def HISTORY_DATA():
    start_directory = r'images'
    os.startfile(start_directory)

def version():
    info1 = '''
版本1.0：
1. 可自行选择文件
2. 对生成的文件进行词云图片展示
3. 可对词云图片进行保存查看'''

    info2 = '''
优化：
1. 可设置增添停用词'''

    messagebox.showinfo('version2.0', info2)


if __name__ == '__main__':
    fileName = '一帘幽梦'
    #make_wordcloud(fileName)

    # 初始化一个窗体对象
    sc = Tk()
    sc.title('词云分析平台')
    image = Image.open(r'background.jpg')
    background_image = ImageTk.PhotoImage(image)
    w = background_image.width()
    h = background_image.height()
    sw = sc.winfo_screenwidth()
    sh = sc.winfo_screenheight()
    sc.geometry('%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2))
    background_label = Label(sc, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # tkinter.messagebox.showinfo('欢迎','欢迎使用数据聚类平台')

    # 窗体内容
    label_title = Label(sc, text='词云分析平台', bg='cyan',
                        font=('黑体', 14, 'bold'), width=5, height=2)
    label_title.pack(fill=X)

    menubar = Menu(sc)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='历史生成词云', command=HISTORY_DATA)
    filemenu.add_command(label='版本信息', command=version)
    filemenu.add_separator()
    filemenu.add_command(label='退出', command=exit_sc)
    menubar.add_cascade(label='菜单', menu=filemenu)

    filechoose = Menu(menubar, tearoff=0)
    filechoose.add_command(label='选取文件', command=FILE_SELECT)
    menubar.add_cascade(label='文件', menu=filechoose)

    setting = Menu(menubar, tearoff=0)
    userChoice = IntVar()
    userChoice.set(1)  # OFFICEOpen默认选中
    #setting.add_command(label='去除停用词', command=FILE_SELECT)
    menubar.add_cascade(label = '设置', menu = setting)
    setting.add_radiobutton(label='去除停用词', command = DELETE_STOPWORDS, variable = userChoice, value = 1)
    setting.add_radiobutton(label = '保留停用词', command = SAVE_STOPWORDS, variable = userChoice, value = 2)


    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label='关于', command=about)
    helpmenu.add_separator()
    helpmenu.add_command(label='使用方法', command=use)
    menubar.add_cascade(label='帮助', menu=helpmenu)
    sc.config(menu=menubar)

    # 文本和按钮
    label_data = Label(sc, text='请选取文件',
                       bg='snow', font=('Consolas', 12, 'bold'),
                       width=40, height=2)
    label_data.place(relx=0.2, rely=0.075, anchor=CENTER, x=7, y=38)

    buttons = Button(sc, text='RUN', command = make_wordcloud, width=10, height=1, fg='green',
                     font=('Consolas', 10, 'bold'))
    buttons.place(anchor=CENTER, x=440, y=180)

    buttone = Button(sc, text='EXIT', command=exit_sc, width=10, height=1, fg='red',
                     font=('Consolas', 10, 'bold'))
    buttone.place(anchor=CENTER, x=440, y=230)

    # 窗体显示
    sc.mainloop()

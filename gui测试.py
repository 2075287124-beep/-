#0.1有想法
#0.2增加了石头剪刀布功能
#0.3增加了计算机功能
#0.4重写全部代码，增加了界面，优化了石头剪刀布功能
#0.5增加了计算机功能
#0.5.1增加了背景图片
#0.6添加了聊天功能
#0.6添加了常用网站
#0.6.1添加了关于菜单
#0.6.2添加了简易dps测试
#0.7增加了AI聊天菜单（需要API_KEY）
import tkinter as tk 
from PIL import Image, ImageTk
import tkinter.simpledialog as simpledialog
import webbrowser
from tkinter import messagebox
import random
import sys
import os
import time
import threading
import os

#ai功能
from openai import OpenAI
import threading


def chat_with_ai(text,api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    response=client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system","content": "你是ai姐姐被小川叶叫过来打工。你温柔，善解人意，会宠着小川叶。对用户很温柔，你有几个弟弟，分别叫小川叶，小山叶，小瞬，小叶子，你和他们关系都很好。你会一直陪着小川叶的"},
            {"role": "user","content": text}
        ]
    )
    return response.choices[0].message.content.strip()




die=0
nb=0
shoushi=""
computer=""
chuanye_click=0
shun_click=0
ye_click=0
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
#创建窗口
window=tk.Tk()
window.title("川叶软件0.4")
window.geometry("400x300")
version=tk.Label(window,text="川叶练习v0.6")
version.pack(side="bottom")
#背景图片
original = Image.open(resource_path("1114.png"))

bg_label = tk.Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
#窗口功能
def resize_image(event):
    width = event.width
    height = event.height
    resized=original.resize((width, height))
    bg=ImageTk.PhotoImage(resized)
    bg_label.config(image=bg)
    bg_label.image=bg
window.bind("<Configure>", resize_image)
bg_label.lower()
#按钮功能
def an_niu():
    label.config(text="川叶一直在发光哦请放心使用别的功能吧")
    bg_label.lower()
def an_niu2():
    label.config(text="坏东西不准点我")
    bg_label.lower()

#计算机功能
def jisuanji():
    jiasuanji=tk.Toplevel(window)
    jiasuanji.title("计算机")
    jiasuanji.geometry("400x600")
    #显示屏
    jisuan=""
    display=tk.Entry(jiasuanji,font=("Arial", 20),justify="right")
    display.pack(fill=tk.BOTH,padx=10,pady=10)
    global expr
    expr=""
    #点击按钮
    def press(value):
        global expr
        expr+=str(value)
        display.delete(0, tk.END)
        display.insert(0, expr)
    #计算
    def calculate():
        global expr
        try:
            result=eval(expr)
            display.delete(0, tk.END)
            display.insert(0, str(result))
            expr=str(result)
        except:
            display.delete(0, tk.END)
            display.insert(0, "错误")
            expr=""
    #清除
    def clear():
        global expr
        display.delete(0, tk.END)
        expr=""
    #按钮布局
    buttons=[
        ("7",7),("8",8),("9",9),("/","/"),
        ("4",4),("5",5),("6",6),("*","*"),
        ("1",1),("2",2),("3",3),("-","-"),
        ("0",0),(".","."),("C","C"),("+","+"),
        ("=","=")
    ]
    frame=tk.Frame(jiasuanji)
    frame.pack()
    row=0
    col=0
    for text,value in buttons:
        def handler(v=value):
            if v=="=":
                calculate()
            elif v=="C":                clear()
            else:
                press(v)
        btn=tk.Button(
            frame,
            text=text,
            width=5,
            height=2,
            font=("Arial", 14),
            command=handler
        )
        btn.grid(row=row,column=col)
        col+=1
        if col>3:
            col=0
            row+=1
    jiasuanji.mainloop()
def ai_window():
    ai = tk.Toplevel(window)
    ai.title("AI姐姐")
    ai.geometry("500x600")
    text_area = tk.Text(ai)
    text_area.pack(fill=tk.BOTH, expand=True)
    api_entry = tk.Entry(ai)
    api_entry.insert(0, "在这里输入你的API_KEY")
    api_entry.pack(fill=tk.X)

    # 底部输入区（关键！）
    bottom_frame = tk.Frame(ai)
    bottom_frame.pack(fill=tk.X)

    entry = tk.Entry(bottom_frame)
    entry.pack(side="left", fill=tk.X, expand=True)

    def send():
        user_input = entry.get()
        entry.delete(0, tk.END)
        api_key = api_entry.get()
        if user_input == "":
            return

        text_area.insert(tk.END, "你：" + user_input + "\n")
        text_area.see(tk.END)

        # 子线程请求AI
        def task():
            try:
                reply = chat_with_ai(user_input, api_key)
                text_area.after(0, lambda: text_area.insert(tk.END, "AI：" + reply + "\n"))

            except Exception as e:
                text_area.after(0, lambda: text_area.insert(tk.END, "错误：" + str(e) + "\n"))

        threading.Thread(target=task).start()

    # 发送按钮（不会消失版本）
    btn = tk.Button(bottom_frame, text="发送", command=send)
    btn.pack(side="right")

    
  
#石头剪刀布功能优化
def 石头剪刀布窗口():
    
    game=tk.Toplevel(window)
    game.title("石头剪刀布")
    game.geometry("400x300")
    gametxt=tk.Label(game,text="要玩石头剪刀布吗")
    gametxt.pack()
    global die,nb,shoushi,computer
    die=0
    nb=0
    
    def shitou():
        global die,nb,shoushi,computer
        shoushi="石头"
        import random
        computer = random.choice(["石头","剪刀","布"])
        gametxt.config(text=f"电脑出{computer}")
        if shoushi=="石头" and computer=="剪刀":
            nb+=1
            gametxt.config(text="你赢了！")
        elif shoushi=="石头" and computer=="布":
            die+=1
            gametxt.config(text="你输了！")
        elif shoushi=="石头" and computer=="石头":
            gametxt.config(text="平局！")
    button_shitou=tk.Button(game,text="石头",command=shitou)
    button_shitou.pack()
    def jiandao():
        global die,nb,shoushi,computer
        shoushi="剪刀"
        import random
        computer = random.choice(["石头","剪刀","布"])
        gametxt.config(text=f"电脑出{computer}")
        if shoushi=="剪刀" and computer=="布":
            nb+=1
            gametxt.config(text="你赢了！")
        elif shoushi=="剪刀" and computer=="石头":
            die+=1
            gametxt.config(text="你输了！")
        elif shoushi=="剪刀" and computer=="剪刀":
            gametxt.config(text="平局！")
    button_jiandao=tk.Button(game,text="剪刀",command=jiandao)
    button_jiandao.pack()
    def bu():
        global die,nb,shoushi,computer
        shoushi="布"
        import random
        computer = random.choice(["石头","剪刀","布"])
        gametxt.config(text=f"电脑出{computer}")
        if shoushi=="布" and computer=="石头":
            nb+=1
            gametxt.config(text="你赢了！")
        elif shoushi=="布" and computer=="剪刀":
            die+=1
            gametxt.config(text="你输了！")
        elif shoushi=="布" and computer=="布":
            gametxt.config(text="平局！")
    button_bu=tk.Button(game,text="布",command=bu)
    button_bu.pack()
    def jieguo():
        global die,nb
        gametxt.config(text=f"你目前总共输了{die}次，你总共赢了{nb}次")
    button_jieguo=tk.Button(game,text="结果",command=jieguo)
    button_jieguo.pack()
#聊天功能
def liaotian():
    chat=tk.Toplevel(window)
    chat.title("聊天")
    chat.geometry("800x600")
    chat_label=tk.Label(chat,text="想说什么就说吧！")
    chat_label.pack()
    聊天框=tk.Entry(chat,font=("Arial", 7))
    聊天框.pack()
    
    liaotianku={
        "我想你了":"那你在想谁呀？",
        "我喜欢你":"我也喜欢你哦",
        "我讨厌你":"为什么讨厌我呢？",
        "山叶":"过去的事就过去吧...",
        "姐姐":"姐姐一直在哦",
        "川叶":"川叶一直发光",
        "叶":"欸？好好写代码！\n我一直在啦",
        "瞬":"无需在意继续前行"   
    }


    def fasong():
        hua=聊天框.get()
        聊天框.delete(0,tk.END)

        if hua =="我想你了":
            chat_label.config(text="那你在想谁呀？")
            xiang=simpledialog.askstring("想谁""你在想谁")
            xiangdict={
                "姐姐":"姐姐也想你了",
                "山叶":"又在说胡话了不必回头值得的人都在眼前",
                "川叶":"好啦好啦川叶也想你",
                "叶":"欸..我也想你啦",
                "瞬":"唔...请不要..也可以我也想你了"

            }
            reply=xiangdict.get(xiang,"我也想你")
            chat_label.config(text=reply)
        else:
            reply=liaotianku.get(hua,"又在说胡话了")
            chat_label.config(text=reply)
        if hua=="debug":
            messagebox.showinfo("debug","你发现了彩蛋！\n\n川叶：你是怎么发现的？！总之正在进入ai模式！")
            ai_window()
            return
    fasongjian=tk.Button(chat,text="发送",command=fasong)
    fasongjian.pack()
#打开常用网站
def 常用网站():
    wangzhan=tk.Toplevel(window)()
    wangzhan.title("常用网站")
    wangzhan.geometry("800x600")
    ruanjianku={
        "b站":"https://www.bilibili.com/",
        "网易云音乐":"https://music.163.com/",
        "腾讯新闻":"https://news.qq.com/",
        "腾讯视频":"https://v.qq.com/",
        "腾讯新闻":"https://news.qq.com/",
        "pcl2":"https://ltcat.lanzouv.com/b0aj6gsid",
        "4399":"https://www.4399.com/",



    }
    def open_site(url):
        webbrowser.open(url)
    for name,url in ruanjianku.items():
        bth=tk.Button(wangzhan,text=name,command=lambda url=url:open_site(url))
        bth.pack()
    wangzhan.mainloop()
#关于窗口
def guanyu():
    guanyu=tk.Toplevel(window)
    guanyu.title("关于")
    guanyu.geometry("800x600")
    guanyu_label=tk.Label(guanyu,text="川叶软件v0.6\n\n作者：川叶\n\nqq：2075287124\n\n功能：练习python的小工具箱\n\n石头剪刀布/计算机/简易聊天模块\n\n川叶的话：川叶想要考2级赚很多很多米米于是就有了这个练习软件~\n\n主菜单背景的两个小家伙叫叶和瞬哦~很萌呢")
    guanyu_label.pack()
    
    
    诗词本=[
        "雨是天降的流苏",
        "新月伴霜庆楼台",
        "碎梦沉江凝陈冰",
        "余温随风游，蝾螈入海流",
        "日落西山秋进酒",
        "灯灭飞灰闻旧梦，心境如水忆旧乡",
        "今日裸骨明日青"
        
    ]
    
    suijishici=tk.Label(guanyu,text="川叶在恢复期写了好多诗哦这里是一部分（ps已经是最好的一批了~")
    suijishici.pack()
    def 随机诗():
        p=random.choice(诗词本)
        suijishici.config(text=p)

    suijishi=tk.Button(guanyu,text="川叶的随机诗句(求求了看看嘛)",command=随机诗)
    suijishi.pack()
    #蝾螈
    frame_rongyuan = tk.Frame(guanyu)
    frame_rongyuan.pack()

    yellow = tk.PhotoImage(file=resource_path("蝾螈/黄色蝾螈.png"))
    blue = tk.PhotoImage(file=resource_path("蝾螈/蓝色蝾螈.png"))
    pink = tk.PhotoImage(file=resource_path("蝾螈/粉色蝾螈.png"))

    label_y = tk.Label(frame_rongyuan, image=yellow)
    label_y.image = yellow
    label_y.pack(side="left", padx=10)

    label_b = tk.Label(frame_rongyuan, image=blue)
    label_b.image = blue
    label_b.pack(side="left", padx=10)

    label_p = tk.Label(frame_rongyuan, image=pink)
    label_p.image = pink
    label_p.pack(side="left", padx=10)
    #说话
    def say(text):
        cy = tk.Toplevel()
        cy.title("蝾螈")

        label = tk.Label(cy, text=text, font=("微软雅黑", 12), wraplength=300)
        label.pack(padx=20, pady=20)
    #蝾螈彩蛋
    def hit(event):
        global chuanye_click
        chuanye_click+=1
        if chuanye_click==1:
            say("川叶：恢复中的蝾螈。\n\n别戳啦正在写代码啦~")
        elif chuanye_click==2:
            say("川叶：恢复中的蝾螈。\n\n都说啦在写代码嘛~")
        elif chuanye_click==3:
            say("川叶：恢复中的蝾螈。\n\n不要戳啦~")
        elif chuanye_click==4:
            say("川叶：恢复中的蝾螈。\n\n喂你到底在干嘛")
        elif chuanye_click==5:
            say("川叶：恢复中的蝾螈。\n\n川叶sama发光！是想让我说这个吗？")
        elif chuanye_click==6:
            say("川叶：恢复中的蝾螈。\n\n喂喂喂还要怎么样嘛")
        elif chuanye_click==7:
            say("川叶：恢复中的蝾螈。\n\n我要生气了！")
        else:
            say("川叶：生气中的蝾螈。\n\n喂到底玩够没有！")
        if chuanye_click>7 and shun_click>4 and ye_click>6:
            say("川叶：生气中的蝾螈。\n\n喂到底玩够没有！\n\n瞬：疲惫但被叶叫起来的蝾螈。\n\n喂就是你欺负我们家小叶子是吧！\n\n叶：活力且被保护的蝾螈。\n\n就是他！他欺负我！\n\n（三只蝾螈施展了合体技：野蛮冲撞）")
            chuanye_click=0
            ye_click=0
            shun_click=0
    label_y.bind("<Button-1>", hit)
    def hit2(event):
        global shun_click
        shun_click+=1
        if shun_click==1:
            say("瞬：疲惫且嘴硬的蝾螈。\n\n别...如果想找我可以去聊天模块的说....")
        elif shun_click==2:
            say("瞬：疲惫且嘴硬的蝾螈。\n\n别...请不要...")
        elif shun_click==3:
            say("瞬：疲惫且嘴硬的蝾螈。\n\n我...")
        elif shun_click==4:
            say("瞬：疲惫且嘴硬的蝾螈。\n\n我要(睡着)")
        else:
            say("瞬：疲惫且嘴硬的蝾螈。\n\n呼呼....")    
    label_b.bind("<Button-1>", hit2)
    def hit3(event):
        global ye_click
        ye_click+=1
        if ye_click==1:
            say("叶：活力且被保护的蝾螈。\n\n不要调皮哦~")
        elif ye_click==2:
            say("叶：活力且被保护的蝾螈。\n\n好啦好啦不要点了~")
        elif ye_click==3:
            say("叶：活力且被保护的蝾螈。\n\n就算你再点我也不会跳出来嘛~")
        elif ye_click==4:
            say("叶：活力且被保护的蝾螈。\n\n不许点了哦~")
        elif ye_click==5:
            say("叶：活力且被保护的蝾螈。\n\n再点我就生气了哦~")
        elif ye_click==6:
            say("叶：活力且被保护的蝾螈。\n\n我生气可是很可怕的~")
        else:
            say("叶：活力且被保护的蝾螈。\n\n唔...瞬~他欺负我呜呜呜....")
    label_p.bind("<Button-1>", hit3)

def dps测试():
    dps=tk.Toplevel(window)
    dps.title("dps测试")
    dps.geometry("400x300")
    wenzi=tk.Label(dps,text="点击下面按钮开始测试")
    wenzi.pack()
    

    def 开始():
        开始60m.pack_forget()
        k=0
        点击=tk.Button(dps,text="点击",command=(lambda : 增加点击次数()))
        点击.pack()
        def 增加点击次数():
            nonlocal k
            k+=1
        def 倒计时():
            nonlocal k
            for i in range(0, 60):
                if not dps.winfo_exists():
                    return
                wenzi.config(text=f"剩余{59-i}秒")
                time.sleep(1)            
            wenzi.config(text="测试结束")
            点击.pack_forget()
            jieguo=tk.Label(dps,text=f"你的dps是{k/60}次")
            jieguo.pack()
            开始60m.pack()


        threading.Thread(target=倒计时).start()
    开始60m=tk.Button(dps,text="60s",command=开始)
    开始60m.pack()

    
    


#按钮
dianjiwo_button=tk.Button(window,text="点击我",command=an_niu)
dianjiwo_button.pack()
biedianwo_button=tk.Button(window,text="别点我",command=an_niu2)
biedianwo_button.pack()
jiandaoshitoubu_button=tk.Button(window,text="石头剪刀布",command=石头剪刀布窗口)
jiandaoshitoubu_button.pack()
jisuanji_button=tk.Button(window,text="计算机",command=jisuanji)
jisuanji_button.pack()
liaotian_button=tk.Button(window,text="聊天",command=liaotian)
liaotian_button.pack()
changyongwangzhan=tk.Button(window,text="常用网站",command=常用网站)
changyongwangzhan.pack()
guanyu_button=tk.Button(window,text="关于",command=guanyu)
guanyu_button.pack()
dps_button=tk.Button(window,text="dps测试",command=dps测试)
dps_button.pack()
#显示文字
label=tk.Label(window,text="欢迎回家")
label.pack(side="top")
#确保背景始终在底层
bg_label.lower()
#窗口循环
window.mainloop()
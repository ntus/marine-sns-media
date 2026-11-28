# ブラックフライデー SNS 動画 v0.4.0（黒地版：当社の型の白黒反転。全商品の「宝の山」から空撮のように寄る）Claude 11/28
import csv,glob,os,subprocess,math,qrcode,sys
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageOps,ImageFilter
B="/tmp/claude-0/-home-user/744e84c8-e228-5c87-bd31-ecf90cd614c3/scratchpad/"
A=B+"allbf/"
FB=B+"fonts/NotoSansCJKjp-Bold.otf"; FR=B+"fonts/NotoSansCJKjp-Regular.otf"
LOGO="/mnt/project-files/brand/logo/nt_marine_logo_ja_landscape_white.png"
URL="https://s.ntus.info/view/category/bf2026?utm_source=sns&utm_medium=video&utm_campaign=blackfriday2026"
FPS=30; BG=(14,14,14); INK=(245,244,241); GREY=(170,170,170); RED=(235,70,70); TILE=(245,244,241)
def F(s,b=True): return ImageFont.truetype(FB if b else FR,s)
def ss(t): t=max(0.,min(1.,t)); return t*t*(3-2*t)
def eo(t): t=max(0.,min(1.,t)); return 1-(1-t)**3
def tc(d,W,y,s,f,fill=INK,a=255,sp=0):
    w=d.textlength(s,font=f)+sp*(len(s)-1); x=(W-w)/2
    if sp:
        for ch in s: d.text((x,y),ch,font=f,fill=fill+(a,)); x+=d.textlength(ch,font=f)+sp
    else: d.text((x,y),s,font=f,fill=fill+(a,))
# ---- 宝の山（全画像のモザイク）
def mosaic(cols=12):
    prods=sorted(glob.glob(A+"products/*"))
    reels=sorted(glob.glob(A+"loongze_178_colors/*"))
    T=300; G=14
    items=reels+prods            # 上3段がリール36、その下に対象品102
    rows=math.ceil(len(items)/cols)
    items+= reels[:rows*cols-len(items)]
    Wm=cols*T+(cols+1)*G; Hm=rows*T+(rows+1)*G
    m=Image.new("RGB",(Wm,Hm),BG)
    for i,p in enumerate(items):
        r,c=divmod(i,cols); x=G+c*(T+G); y=G+r*(T+G)
        tile=Image.new("RGB",(T,T),TILE)
        im=Image.open(p).convert("RGB"); im=ImageOps.contain(im,(T-16,T-16),Image.LANCZOS)
        reg=tile.crop((8+(T-16-im.width)//2,8+(T-16-im.height)//2,8+(T-16-im.width)//2+im.width,8+(T-16-im.height)//2+im.height))
        tile.paste(ImageChops.multiply(reg,im),(8+(T-16-im.width)//2,8+(T-16-im.height)//2))
        m.paste(tile,(x,y))
    return m,cols,rows,T,G,len(prods),len(reels)
MZ=None
def qr_img(px):
    q=qrcode.QRCode(border=2,box_size=10,error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(URL); q.make()
    return q.make_image(fill_color=(0,0,0),back_color=(255,255,255)).convert("RGB").resize((px,px),Image.NEAREST)
class Base:
    def __init__(s,W,H):
        s.W,s.H=W,H; v=H>W; s.m=int(W*0.026); s.pad=int(W*0.06)
        s.qs=200 if v else 150; s.foot=s.qs+40; s.fy=H-s.m-s.pad*0.6-s.foot
        base=Image.new("RGBA",(W,H),BG+(255,)); s.base=base
        s.top=int(s.m+s.pad*0.55+(30 if v else 24)+22)
        s.area=(s.m+3, s.top+int(s.pad*0.35), W-s.m-3, int(s.fy)-int(s.pad*0.3))
        ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
        # 外の黒い帯（上と下）と細い白枠
        x0,y0,x1,y1=s.area
        d.rectangle((0,0,W,y0),fill=BG+(255,)); d.rectangle((0,y1,W,H),fill=BG+(255,))
        d.rectangle((0,0,x0,H),fill=BG+(255,)); d.rectangle((x1,0,W,H),fill=BG+(255,))
        d.rectangle((s.m,s.m,W-s.m,H-s.m),outline=INK,width=3)
        y=int(s.fy); d.line((s.pad,y,W-s.pad,y),fill=INK,width=3)
        cy=(y+(H-s.m))//2
        q=qr_img(s.qs); qx=W-s.pad-s.qs; ov.paste(q,(qx,cy-s.qs//2))
        lg=Image.open(LOGO).convert("RGBA"); h=int(s.qs*0.42); lg=lg.resize((int(lg.width*h/lg.height),h),Image.LANCZOS)
        ov.alpha_composite(lg,(s.pad,cy-lg.height//2))
        f1=F(30 if v else 24); f2=F(24 if v else 20,False); tx=qx-24; ty=cy-(f1.size+12+f2.size)//2-6
        for t,f,c,yy in (("QRでセール会場へ",f1,INK,ty),("s.ntus.info",f2,GREY,ty+f1.size+12)):
            d.text((tx-d.textlength(t,font=f),yy),t,font=f,fill=c)
        bf=F(30 if v else 24); bt="BLACK FRIDAY"; sp=6; bw=d.textlength(bt,font=bf)+sp*(len(bt)-1)+44
        bx,by=s.pad,s.m+s.pad*0.55; d.rectangle((bx,by,bx+bw,by+bf.size+22),fill=INK)
        x=bx+22
        for ch in bt: d.text((x,by+8),ch,font=bf,fill=BG); x+=d.textlength(ch,font=bf)+sp
        f3=F(24 if v else 20,False); t3="12/1(火) 23:59まで"
        d.text((W-s.pad-d.textlength(t3,font=f3),by+(bf.size+22-f3.size)/2-4),t3,font=f3,fill=GREY)
        s.ov=ov
def cam_frame(b,cx,cy,vw,dim=0.0,blur=0):
    """モザイク上の (cx,cy) を中心に、幅 vw（モザイクの px）を表示域に写す"""
    m=MZ[0]; x0,y0,x1,y1=b.area; aw,ah=x1-x0,y1-y0
    Wm,Hm=m.size; vw=min(vw,Wm,Hm*aw/ah); vh=vw*ah/aw
    cx=min(max(cx,vw/2),Wm-vw/2); cy=min(max(cy,vh/2),Hm-vh/2)
    box=(cx-vw/2,cy-vh/2,cx+vw/2,cy+vh/2)
    view=m.transform((aw,ah),Image.EXTENT,box,Image.BICUBIC,fillcolor=BG)
    if blur: view=view.filter(ImageFilter.GaussianBlur(blur))
    if dim>0: view=Image.blend(view,Image.new("RGB",view.size,(0,0,0)),dim)
    im=Image.new("RGBA",(b.W,b.H),BG+(255,)); im.paste(view,(x0,y0)); return im
def lerp(a,b,t): return a+(b-a)*t
def camera(t,keys):
    for (t0,c0),(t1,c1) in zip(keys,keys[1:]):
        if t0<=t<=t1:
            u=ss((t-t0)/(t1-t0)); cx=lerp(c0[0],c1[0],u); cy=lerp(c0[1],c1[1],u)
            vw=math.exp(lerp(math.log(c0[2]),math.log(c1[2]),u)); return cx,cy,vw
    return keys[-1][1]
def caption(im,b,l1,l2,a,col2=RED):
    if a<=0: return
    d=ImageDraw.Draw(im); v=b.H>b.W; x0,y0,x1,y1=b.area
    f1=F(50 if v else 40); f2=F(64 if v else 50)
    hh=f1.size+f2.size+(70 if v else 54)
    band=Image.new("RGBA",(x1-x0,hh),(0,0,0,int(185*a))); im.alpha_composite(band,(x0,y1-hh))
    yy=y1-hh+(20 if v else 14)+int(14*(1-a))
    tc(d,b.W,yy,l1,f1,INK,int(255*a)); tc(d,b.W,yy+f1.size+(14 if v else 10),l2,f2,col2,int(255*a))
def render(W,H,out):
    b=Base(W,H); v=H>W
    m,cols,rows,T,G,npr,nre=MZ; Wm,Hm=m.size; step=T+G
    x0,y0,x1,y1=b.area; aw,ah=x1-x0,y1-y0
    full_vw=min(Wm, Hm*aw/ah)               # 画面いっぱい（帯を出さない）
    def cell(c,r): return (G+c*step+T/2, G+r*step+T/2)
    z1=step*(3.2 if v else 4.6)              # リールに寄ったときの幅（タイル数）
    z2=step*(4.2 if v else 6.0)
    rc=lambda c,r: cell(c,r)
    rr=math.ceil(nre/cols); ry=(rr-1)/2
    K=[(0.0,(Wm/2,Hm/2,full_vw)),(2.2,(Wm/2,Hm/2,full_vw*0.93)),
       (4.0,(*rc(1.0,ry),z1)),(7.6,(*rc(cols-2.0,ry),z1)),        # リールの段をなめる
       (9.0,(*rc(cols-2.5,rr+2),z2)),(11.2,(*rc(1.5,rows-3),z2)),  # 対象品を斜めに降りる
       (12.4,(Wm/2,Hm/2,full_vw)),(15.0,(Wm/2,Hm/2,full_vw*0.97))]
    N=int(15.0*FPS)
    def fr(i):
        t=i/FPS; cx,cy,vw=camera(t,K)
        if t<2.2:
            dim=0.72*eo(min(1,t/0.4)) if t<1.9 else 0.72*(1-eo((t-1.9)/0.3))
            im=cam_frame(b,cx,cy,vw,dim)
            a=int(255*eo(t/0.5)) if t<1.9 else int(255*(1-eo((t-1.9)/0.3)))
            d=ImageDraw.Draw(im); f1=F(60 if v else 50); f2=F(96 if v else 76); f3=F(40 if v else 32,False)
            yy=y0+ah*0.30
            tc(d,W,yy,"リールも、釣具も、",f1,INK,a); yy+=f1.size+24
            tc(d,W,yy,"まとめてセール中",f2,INK,a); yy+=f2.size+34
            tc(d,W,yy,f"在庫のある対象品 {npr}品＋リールの色違い",f3,INK,a)
        elif t>=12.4:
            u=(t-12.4)/2.6; im=cam_frame(b,cx,cy,vw,0.72*eo(u*2),blur=int(4*eo(u*2)))
            d=ImageDraw.Draw(im); a=int(255*eo(u*2.2)); fb=F(130 if v else 96)
            yy=y0+ah*(0.10 if v else 0.04)
            tc(d,W,yy,"BLACK",fb,INK,a,4); yy+=fb.size*1.05; tc(d,W,yy,"FRIDAY",fb,INK,a,4); yy+=fb.size*1.4
            d.line((W/2-60,yy,W/2+60,yy),fill=INK+(a,),width=3); yy+=34
            for s_,sz,bold,col in (("Loongze Airlite 即納品",40,True,INK),("最大1万円OFF（税込）",66,True,RED),
                                   ("ルアー・ライン・小物",40,True,INK),("最大30%OFF",66,True,RED),
                                   ("12/1(火) 23:59まで・在庫限り",34,False,GREY)):
                f=F(int(sz*(1 if v else 0.8)),bold); tc(d,W,yy,s_,f,col,a); yy+=f.size+(18 if v else 10)
        else:
            im=cam_frame(b,cx,cy,vw)
            if t<8.2: caption(im,b,"Loongze Airlite 即納品・色違いも",
                              "最大1万円OFF（税込）",eo((t-3.4)/0.6)*(1-eo((t-7.8)/0.4)))
            else: caption(im,b,"ルアーも、ラインも、小物も",
                          "最大30%OFF",eo((t-8.6)/0.6)*(1-eo((t-11.6)/0.5)))
        im.alpha_composite(b.ov); return im
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-c:v","libx264","-pix_fmt","yuv420p","-preset","medium","-crf","27","-movflags","+faststart","-an",out],stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(fr(i).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    if len(sys.argv)>2:
        for ts in (1.0,3.0,5.5,9.5,13.8): fr(int(ts*FPS)).convert("RGB").save(out.replace(".mp4",f"_{ts}.jpg"),quality=80)
if __name__=="__main__":
    W,H=(1080,1920) if sys.argv[1]=="9x16" else (1080,1080)
    MZ=mosaic(9 if H>W else 12); print("mosaic",MZ[0].size,MZ[5],MZ[6])
    o=B+f"bfv/r4/bf2026_v4_black_{sys.argv[1]}.mp4"; render(W,H,o); print(o,os.path.getsize(o))

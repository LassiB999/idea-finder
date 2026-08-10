#!/usr/bin/env python3
"""Idea Finder app icon — purple gradient squircle + glowing lightbulb + spark."""
import os, math
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)
S = 1024                      # render size (downscaled later)
V1 = (151,80,255)            # vivid violet
V2 = (86,72,230)             # deep indigo
V3 = (222,74,244)            # magenta (corner glow)
WHITE = (255,255,255)

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def diag_gradient(size, c1, c2):
    w,h=size; img=Image.new("RGB",(w,h))
    px=img.load()
    for y in range(h):
        for x in range(0,w,1):
            t=((x/w)+(y/h))/2
            px[x,y]=lerp(c1,c2,t)
    return img

def rounded_mask(size, r):
    m=Image.new("L",size,0); d=ImageDraw.Draw(m)
    d.rounded_rectangle([0,0,size[0]-1,size[1]-1], radius=r, fill=255)
    return m

def build():
    # gradient base
    base = diag_gradient((S,S), V1, V2)
    # magenta glow in top-right corner
    glow = Image.new("RGB",(S,S),(0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse([S*0.45,-S*0.25,S*1.25,S*0.55], fill=V3)
    glow=glow.filter(ImageFilter.GaussianBlur(S*0.16))
    base=Image.blend(base,glow,0.38)
    # inner top gloss
    gloss=Image.new("L",(S,S),0); ImageDraw.Draw(gloss).ellipse([-S*0.2,-S*0.55,S*1.2,S*0.35],fill=90)
    gloss=gloss.filter(ImageFilter.GaussianBlur(S*0.06))
    white=Image.new("RGB",(S,S),WHITE)
    base=Image.composite(Image.blend(base,white,0.16),base,gloss)

    d=ImageDraw.Draw(base,"RGBA")
    cx=S/2; cy=S*0.44; R=S*0.20

    # soft halo behind bulb (subtle — keep the purple rich)
    halo=Image.new("L",(S,S),0); ImageDraw.Draw(halo).ellipse([cx-R*1.6,cy-R*1.6,cx+R*1.6,cy+R*1.6],fill=48)
    halo=halo.filter(ImageFilter.GaussianBlur(S*0.075))
    base=Image.composite(Image.new("RGB",(S,S),WHITE),base,halo).convert("RGB")
    d=ImageDraw.Draw(base,"RGBA")

    # bulb glass (white circle)
    d.ellipse([cx-R,cy-R,cx+R,cy+R], fill=WHITE)
    # neck + base of bulb
    nw=R*0.62
    d.rounded_rectangle([cx-nw/2, cy+R*0.72, cx+nw/2, cy+R*1.28], radius=R*0.12, fill=WHITE)
    # screw base bands (purple lines) + inner filament
    for i in range(3):
        yy=cy+R*0.86+i*R*0.16
        d.line([cx-nw*0.42,yy,cx+nw*0.42,yy], fill=V1, width=int(S*0.012))
    # filament (a little upward-growth zig -> "idea/insight")
    d.line([(cx-R*0.34,cy+R*0.18),(cx-R*0.08,cy-R*0.12),(cx+R*0.12,cy+R*0.06),(cx+R*0.34,cy-R*0.30)],
           fill=V2, width=int(S*0.02), joint="curve")
    # arrow head on filament tip (growth)
    tx,ty=cx+R*0.34,cy-R*0.30
    d.line([(tx,ty),(tx-R*0.16,ty)],fill=V2,width=int(S*0.02))
    d.line([(tx,ty),(tx,ty+R*0.16)],fill=V2,width=int(S*0.02))

    # sparkle (discovery) top-right of bulb — 4-point star
    def star4(sx,sy,ro,ri):
        pts=[]
        for k in range(8):
            ang=math.radians(k*45-90); rr=ro if k%2==0 else ri
            pts.append((sx+math.cos(ang)*rr, sy+math.sin(ang)*rr))
        return pts
    d.polygon(star4(cx+R*1.16, cy-R*0.98, R*0.34, R*0.10), fill=WHITE)
    d.polygon(star4(cx+R*1.5, cy-R*0.25, R*0.15, R*0.045), fill=(255,255,255,220))

    # rounded-square mask (app-icon squircle) + transparent corners
    r=int(S*0.235)
    mask=rounded_mask((S,S),r)
    out=Image.new("RGBA",(S,S),(0,0,0,0))
    out.paste(base,(0,0),mask)

    # subtle inner border for definition
    bd=ImageDraw.Draw(out)
    bd.rounded_rectangle([2,2,S-3,S-3],radius=r,outline=(255,255,255,40),width=int(S*0.006))

    for sz in (512,256,192,180,128,64,32):
        out.resize((sz,sz),Image.LANCZOS).save(os.path.join(OUT,f"icon-{sz}.png"))
    # maskable (full-bleed, no transparent corners) for PWA
    full=base.resize((512,512),Image.LANCZOS); full.save(os.path.join(OUT,"icon-maskable-512.png"))
    print("icons written to", OUT)

if __name__=="__main__":
    build()

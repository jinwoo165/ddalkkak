"""Tactile synthesis v2: irregular friction and short damped impacts, no musical beds.
All assets are original synthesis, not field recordings. Fixed seeds are reproducible.
"""
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io.wavfile import write
sr=44100
out=Path(__file__).resolve().parents[1]/'docs/assets/generated'
out.mkdir(parents=True,exist_ok=True)

def make(name,kind,duration,lo,hi,seed):
    rng=np.random.default_rng(seed);t=np.arange(int(sr*duration))/sr;n=len(t)
    def band(lo,hi):
        return sosfilt(butter(2,[lo,hi],btype='bandpass',fs=sr,output='sos'),rng.normal(size=n))
    def pulse(at,width):
        x=(t-at)/width
        return np.where((x>=0)&(x<=1),np.sin(np.pi*np.clip(x,0,1))**1.6,0)
    texture=band(lo,hi);sig=np.zeros(n)
    if kind in ('friction','grain','crisp'):
        # Randomly spaced strokes and microcontacts: no periodic AM / motor buzz.
        pressure=np.interp(t,np.linspace(0,duration,17),rng.uniform(.25,1,17))
        strokes=np.zeros(n)
        count={'friction':3,'grain':6,'crisp':4}[kind]
        for at in np.sort(rng.uniform(.002,duration*.65,count)):
            strokes+=pulse(at,rng.uniform(.035,.10) if kind=='friction' else rng.uniform(.009,.045))
        sig=texture*pressure*(.14+strokes)
        if kind!='friction':
            for at in rng.uniform(.003,duration*.8,40 if kind=='grain' else 18):
                dt=np.maximum(0,t-at)
                sig+=texture*(t>=at)*np.exp(-dt/rng.uniform(.0007,.003))*rng.uniform(.2,.9)
        sig*=np.sin(np.pi*t/duration)**.8
    elif kind in ('squish','soft','air'):
        # Mostly soft, band-limited contact; a few cycles of low resonance only.
        env=pulse(.001,duration*.85)
        sig=texture*env*(.8 if kind=='air' else .32)
        if kind!='air':
            f={'squish':lo,'soft':100}[kind]
            sig+=.22*np.sin(2*np.pi*f*t)*np.exp(-t/.018)*np.minimum(t/.003,1)
            if kind=='squish':sig+=band(350,1300)*pulse(duration*.32,duration*.32)*.18
    elif kind=='snap':
        sig=texture*np.exp(-t/.014)*np.minimum(t/.0015,1)
        sig+=band(130,700)*pulse(.002,.035)*.2
    elif kind=='heart':
        for at,amp in [(0,1),(.085,.6)]:
            dt=np.maximum(t-at,0)
            sig+=amp*(band(65,240)+.12*np.sin(2*np.pi*76*dt))*pulse(at,.055)
    elif kind=='spark':
        # Tiny sugar-like tick, no chord or sustained chime.
        sig=texture*pulse(0,.055)
        sig+=.045*np.sin(2*np.pi*2300*t)*np.exp(-t/.012)*np.minimum(t/.001,1)
    sig-=sig.mean()
    sig*=np.minimum(t/.002,1)*np.minimum((duration-t)/.012,1)
    sig=sig/max(.001,np.max(np.abs(sig)))*.58
    write(out/(name+'.wav'),sr,(sig*32767).astype(np.int16))

settings=[
('dubai','crisp',.23,600,4800),('chocolate','snap',.09,500,2600),
('mochi','squish',.12,140,950),('macaron','crisp',.14,1400,6000),
('donut','grain',.18,1800,6500),('pudding','squish',.105,185,850),
('croissant','crisp',.25,1800,7500),('cake','soft',.13,150,1400),
('waffle','crisp',.17,750,3800),('gummy','squish',.145,120,1100),
('egg','grain',.20,2200,8000),('paw','soft',.085,220,1600),
('heart','heart',.17,65,240),('star','spark',.075,2500,8000),
('cloud','air',.18,160,1600),('cat','soft',.16,95,750)]
for i,(a,b,c,d,e) in enumerate(settings):make('shape_'+a,b,c,d,e,i+113)
for i,(a,b,c,d,e) in enumerate([
('paper','friction',.23,850,6500),('pencil','friction',.19,1400,7800),
('sand','grain',.24,2000,9000),('snow','crisp',.22,280,2800),
('brush','friction',.27,2400,10500)]):make('scratch_'+a,b,c,d,e,i+180)
print('Generated 21 tactile sounds')

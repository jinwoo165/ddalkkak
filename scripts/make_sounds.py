"""Original synthesized tactile sounds; deterministic and royalty-free project assets."""
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io.wavfile import write
sr=44100
out=Path(__file__).resolve().parents[1]/'docs/assets/generated';out.mkdir(parents=True,exist_ok=True)
def make(name,kind,duration,freq,seed):
 rng=np.random.default_rng(seed);t=np.arange(int(sr*duration))/sr;n=len(t)
 noise=rng.normal(0,1,n);low=sosfilt(butter(2,min(freq,15000),fs=sr,output='sos'),noise)
 high=noise-sosfilt(butter(2,900,fs=sr,output='sos'),noise)
 envelope=np.minimum(t/.008,1)*np.exp(-t/(duration/4))
 if kind=='crunch':
  sig=low*.1
  for at in rng.uniform(.005,duration*.65,36):
   dt=np.maximum(0,t-at);sig+=high*np.exp(-dt/.004)*(t>=at)*rng.uniform(.04,.18)
  sig+=.2*np.sin(2*np.pi*160*t)*np.exp(-t/.03)
 elif kind=='rub':
  envelope=np.sin(np.pi*t/duration)**1.3
  sig=low*(.5+.5*np.sin(2*np.pi*(12+seed%15)*t))*.5+high*.025
 elif kind=='chime':
  sig=sum(np.sin(2*np.pi*freq*f*t)*np.exp(-t/(.12+i*.05))/(i+1) for i,f in enumerate([1,1.5,2.01]))*.3
 elif kind=='pop':
  phase=2*np.pi*(freq*t+(freq*2)*.023*(1-np.exp(-t/.023)))
  sig=np.sin(phase)*.5+low*.12
 elif kind=='purr':
  sig=low*(.5+.5*np.sin(2*np.pi*27*t))*.4+np.sin(2*np.pi*90*t)*.08
 elif kind=='heart':
  sig=sum(np.sin(2*np.pi*85*t)*np.exp(-np.maximum(0,t-at)/.045)*(t>=at) for at in [0,.14])*.5
 else: sig=low*.5+np.sin(2*np.pi*freq*t)*np.exp(-t/.02)*.2
 sig*=envelope;sig*=np.minimum((duration-t)/.018,1);sig=sig/max(.01,np.max(np.abs(sig)))*.62
 write(out/(name+'.wav'),sr,(sig*32767).astype(np.int16))
settings=[('dubai','crunch',.38,2400),('chocolate','crunch',.16,1100),('mochi','pop',.2,160),('macaron','crunch',.25,3400),('donut','crunch',.32,6100),('pudding','pop',.36,280),('croissant','crunch',.42,5200),('cake','soft',.21,300),('waffle','crunch',.28,1800),('gummy','pop',.27,110),('egg','rub',.3,6500),('paw','pop',.13,240),('heart','heart',.4,90),('star','chime',.65,1568),('cloud','rub',.5,550),('cat','purr',.45,450)]
for i,(a,b,c,d) in enumerate(settings):make('shape_'+a,b,c,d,i+13)
for i,(a,b,c,d) in enumerate([('paper','rub',.27,3600),('pencil','rub',.22,2000),('sand','crunch',.38,4100),('snow','crunch',.34,900),('brush','rub',.43,5800)]):make('scratch_'+a,b,c,d,i+80)
print('Generated',len(list(out.glob('*.wav'))),'original sounds')

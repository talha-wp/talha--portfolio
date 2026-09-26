"""Build the portfolio's silent 18-second project showcase with FFmpeg.

Usage: python scripts/build-showreel.py /path/to/THICCCBOI-Bold.ttf
The public images stay unchanged. Only the resulting video is published.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
assets = root / 'dist/assets'
font = Path(sys.argv[1]).resolve()

def run(args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def title(text, size, color, x, y):
    return f"drawtext=fontfile='{font}':text='{text}':fontsize={size}:fontcolor={color}:x={x}:y={y}"

with tempfile.TemporaryDirectory(prefix='talha-reel-') as temp:
    temp = Path(temp)
    for index, duration, filename, lines in [
        (0, 3, None, [('TALHA ALI / SELECTED WORK', 23, '0xbcef12', '70', '90'), ('Designed with purpose.', 76, 'white', '70', '260'), ('Built with care.', 76, '0xbcef12', '70', '350'), ('Web design  /  WordPress  /  E-commerce', 25, '0xa5a5a3', '70', '560')]),
        (1, 6, 'didi.jpg', [('01 / WEB DESIGN + DEVELOPMENT', 20, '0xbcef12', '54', '563'), ('Didi Hirsch', 44, 'white', '54', '600'), ('TALHA ALI', 20, 'white', 'w-tw-54', '58')]),
        (2, 6, 'fortress.jpg', [('02 / RESPONSIVE WEB EXPERIENCE', 20, '0xbcef12', '54', '563'), ('Made for every screen.', 44, 'white', '54', '600'), ('TALHA ALI', 20, 'white', 'w-tw-54', '58')]),
        (3, 3, None, [('YOUR NEXT PROJECT', 23, '0xbcef12', '70', '90'), ('An idea worth building?', 76, 'white', '70', '260'), ('Let us make it happen.', 76, '0xbcef12', '70', '350'), ('talha-ali.com', 29, 'white', '70', '560')]),
    ]:
        if filename:
            inputs = ['-loop', '1', '-framerate', '30', '-i', str(assets / filename)]
            filters = ["scale=1920:-2", "zoompan=z='1+0.00018*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1280x720:fps=30", "drawbox=x=0:y=535:w=iw:h=185:color=black@0.82:t=fill"]
        else:
            inputs = ['-f', 'lavfi', '-i', f'color=c=0x080808:s=1280x720:r=30:d={duration}']
            filters = ['drawbox=x=70:y=220:w=90:h=4:color=0xbcef12:t=fill']
        filters.extend(title(*line) for line in lines)
        filters += [f'fade=t=in:st=0:d=0.3', f'fade=t=out:st={duration-0.3}:d=0.3', 'format=yuv420p']
        run([*inputs, '-vf', ','.join(filters), '-t', str(duration), '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '22', '-threads', '2', str(temp / f'{index}.mp4')])
    (temp / 'concat.txt').write_text('\n'.join(f"file '{temp / f'{i}.mp4'}'" for i in range(4)))
    run(['-f', 'concat', '-safe', '0', '-i', str(temp / 'concat.txt'), '-c', 'copy', '-movflags', '+faststart', str(assets / 'portfolio-showreel.mp4')])
    run(['-ss', '1.2', '-i', str(assets / 'portfolio-showreel.mp4'), '-frames:v', '1', '-q:v', '2', str(assets / 'showreel-poster.jpg')])
print('Created portfolio-showreel.mp4 and showreel-poster.jpg', flush=True)

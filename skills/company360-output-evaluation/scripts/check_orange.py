"""Motif document release gate. Input is the rendered delivery PDF. Exit 1 blocks release."""
import argparse,sys
from pathlib import Path
import fitz
from PIL import Image
import numpy as np

def check(path):
    with fitz.open(path) as pdf:
        if not len(pdf): return False, 'empty document'
        page=pdf[0]
        if not page.get_text().strip(): return False, 'title page has no extractable text; manual review required'
        pix=page.get_pixmap(matrix=fitz.Matrix(2,2),colorspace=fitz.csRGB,alpha=False)
        a=np.asarray(Image.frombytes('RGB',(pix.width,pix.height),pix.samples)).astype('int16')
        mask=(np.abs(a[:int(pix.height*.58)]-[255,91,31]).max(axis=2)<=36)
        minimum=max(120,int(pix.width*.2))
        for y in np.flatnonzero(mask.sum(axis=1)>=minimum):
            edges=np.where(np.diff(np.r_[False,mask[y],False]))[0]
            for left,right in zip(edges[::2],edges[1::2]):
                if right-left>=minimum and left>0 and right<pix.width:
                    return True,f'page 1; orange band x={left/2:.1f}..{right/2:.1f}, y={y/2:.1f} pt'
        return False,'visible orange title rule or shading missing; correct, render and retest'
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('pdfs',nargs='+',type=Path)
    failed=False
    for p in parser.parse_args().pdfs:
        ok,detail=check(p);print(('PASS' if ok else 'BLOCK'),p.name,detail);failed|=not ok
    sys.exit(int(failed))

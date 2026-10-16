#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile, BadZipFile
import re
import shutil
import subprocess
import sys
import tempfile

REQUIRED = ["index.html", "README.md", "RISK-REVIEW.md", "assets/css/styles.css", "assets/js/app.js"]
TEMP_PATTERNS = (".DS_Store", "Thumbs.db", "__pycache__", ".pyc", "~")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.refs=[]; self.links=[]; self.inputs=[]; self.labels=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if d.get("id"): self.ids.append(d["id"])
        for key in ("src", "href"):
            if d.get(key): self.refs.append((tag, key, d[key]))
        if tag == "a" and d.get("href"): self.links.append(d["href"])
        if tag in ("input", "select", "textarea") and d.get("id"): self.inputs.append(d["id"])
        if tag == "label" and d.get("for"): self.labels.append(d["for"])

def fail(errors, msg): errors.append(msg)
def external(ref): return ref.startswith(("http://", "https://", "mailto:", "tel:", "data:"))

def validate_dir(root: Path):
    errors=[]; warnings=[]; details=[]
    for rel in REQUIRED:
        if not (root/rel).is_file(): fail(errors, f"arquivo obrigatório ausente: {rel}")
    if errors: return errors, warnings, details
    html=(root/"index.html").read_text(encoding="utf-8")
    css=(root/"assets/css/styles.css").read_text(encoding="utf-8")
    js=(root/"assets/js/app.js").read_text(encoding="utf-8")
    p=Parser(); p.feed(html)
    if len(p.ids) != len(set(p.ids)): fail(errors, "IDs duplicados no HTML")
    for _,_,ref in p.refs:
        if ref.startswith("#"):
            if ref != "#" and ref[1:] not in p.ids: fail(errors, f"âncora sem destino: {ref}")
        elif not external(ref):
            if Path(ref).is_absolute(): fail(errors, f"caminho absoluto local: {ref}")
            elif not (root/ref).is_file(): fail(errors, f"referência HTML ausente: {ref}")
    for field in p.inputs:
        if field not in p.labels: warnings.append(f"campo sem label[for]: {field}")
    for ref in re.findall(r"url\(['\"]?([^)'\"]+)", css):
        if external(ref): continue
        target=(root/"assets/css"/ref).resolve()
        if not target.is_file(): fail(errors, f"asset CSS ausente: {ref}")
    for ident in re.findall(r"\$\(['\"]#([A-Za-z][\w:-]*)['\"]\)", js):
        if ident not in p.ids: fail(errors, f"JavaScript referencia ID ausente: {ident}")
    if 'name="viewport"' not in html and "name='viewport'" not in html: fail(errors, "meta viewport ausente")
    if "@media" not in css: fail(errors, "media queries ausentes")
    if "prefers-reduced-motion" not in css: warnings.append("prefers-reduced-motion ausente")
    node=shutil.which("node")
    if node:
        r=subprocess.run([node,"--check",str(root/"assets/js/app.js")],capture_output=True,text=True)
        if r.returncode: fail(errors, "erro de sintaxe JavaScript: "+(r.stderr.strip() or r.stdout.strip()))
    else: warnings.append("Node.js indisponível; sintaxe JavaScript não verificada")
    try:
        from PIL import Image
        for f in sorted((root/"assets/images").glob("*")):
            if not f.is_file(): continue
            try:
                with Image.open(f) as im: im.verify()
                with Image.open(f) as im:
                    details.append(f"imagem {f.name}: {im.width}x{im.height} {im.format}")
                    if im.width < 150 or im.height < 80: warnings.append(f"imagem pequena, revisar nitidez: {f.name} ({im.width}x{im.height})")
            except Exception as exc: fail(errors, f"imagem inválida {f.name}: {exc}")
    except ImportError: warnings.append("Pillow indisponível; imagens não verificadas")
    for f in root.rglob("*"):
        if f.is_file() and (f.name in TEMP_PATTERNS or f.suffix == ".pyc" or "__pycache__" in f.parts):
            fail(errors, f"arquivo temporário no projeto: {f.relative_to(root)}")
    return errors, warnings, details

def main(target: Path):
    temp=None
    try:
        if target.suffix.lower()==".zip":
            try:
                z=ZipFile(target); bad=z.testzip()
                if bad: raise SystemExit(f"ERRO: arquivo corrompido no ZIP: {bad}")
                names=z.namelist()
                extra=[n for n in names if n.startswith("/") or "../" in n]
                if extra: raise SystemExit("ERRO: caminhos inseguros no ZIP")
                temp=Path(tempfile.mkdtemp(prefix="webzip_validate_")); z.extractall(temp); z.close(); root=temp
            except BadZipFile as exc: raise SystemExit(f"ERRO: ZIP inválido: {exc}")
        else: root=target
        errors,warnings,details=validate_dir(root)
        print(f"Resultado: {len(errors)} erro(s), {len(warnings)} aviso(s)")
        for x in errors: print("ERRO:",x)
        for x in warnings: print("AVISO:",x)
        for x in details: print("INFO:",x)
        if errors: raise SystemExit(1)
    finally:
        if temp: shutil.rmtree(temp,ignore_errors=True)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("uso: validate_project.py <pasta-ou-zip>")
    main(Path(sys.argv[1]))

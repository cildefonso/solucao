# Checklist de qualidade e risco

## Estrutura e links
- [ ] ZIP íntegro
- [ ] Arquivos obrigatórios presentes
- [ ] IDs únicos
- [ ] `src`, `href`, âncoras e `url(...)` válidos
- [ ] Sem caminhos absolutos locais
- [ ] Sem arquivos temporários

## Arquivos de alto risco
- [ ] `app.js` passa em `node --check`
- [ ] Seletores JavaScript existem
- [ ] Regex e escapes revisados
- [ ] Listeners, modais, downloads e estados ARIA revisados
- [ ] `index.html` parseado
- [ ] Campos e labels revisados

## Arquivos de risco médio
- [ ] CSS possui breakpoints
- [ ] Sem overflow horizontal indevido
- [ ] Foco e redução de movimento presentes
- [ ] Recursos CSS com compatibilidade registrada
- [ ] Imagens válidas, proporcionais e com resolução adequada

## Entrega
- [ ] README completo
- [ ] `RISK-REVIEW.md` incluído
- [ ] Zero riscos altos conhecidos
- [ ] ZIP revalidado depois das correções

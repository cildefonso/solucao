# Solucao

**Transforme sistemas legados em especificações executáveis por agentes de IA.**

Sabe aquele sistema que ninguém quer tocar? O que tem 10 anos, roda em produção, gera dinheiro todos os dias, mas ninguém sabe ao certo *o que ele faz* por dentro? O Solucao foi feito para ele.

---

## O que é o Solucao?

O Solucao é um framework de engenharia solucao de especificações. Você o instala dentro do projeto legado, ativa um agente de IA que já usa no dia a dia, e ele coordena um time de especialistas para analisar o código e gerar especificações completas, rastreáveis e prontas para uso por qualquer agente codificador.

**Em outras palavras:** o Solucao transforma código sem documentação em contratos operacionais que um agente de IA consegue entender e usar para evoluir o sistema com segurança.

---

## Começo rápido

Na raiz do seu projeto:

```bash
npx solucao install
```

Depois, abra o projeto no seu agente de IA favorito e escolha o fluxo:

```
/solucao       # descobrir e especificar um sistema existente
/solucao-new   # transformar uma ideia nova em PRD e specs SDD
```

Pronto. O Solucao assume o volante e guia você até o fim.

---

## O que você vai encontrar aqui

<div class="grid cards" markdown>

- **Por que o Solucao existe**

    O problema que ele resolve e por que a solução importa.

    [:octicons-arrow-right-24: Ler mais](por-que-solucao.md)

- **Instalação**

    Dois minutos e você está pronto para começar.

    [:octicons-arrow-right-24: Instalar](instalacao.md)

- **Pipeline de análise**

    As 5 fases que transformam código em especificação.

    [:octicons-arrow-right-24: Ver pipeline](pipeline.md)

- **Agentes**

    7 Teams especializados: Core, New Project, Code Forward, Migration, Documentation, Pricing e Translators.

    [:octicons-arrow-right-24: Ver agentes](agentes/index.md)

- **Começar um projeto novo**

    Vá de uma ideia em uma linha até personas, PRD e specs SDD avaliadas.

    [:octicons-arrow-right-24: Usar /solucao-new](newproject/index.md)

</div>

---

## Garantia de segurança

!!! danger "💾 Faça backup do projeto antes de começar"
    Embora o Solucao nunca modifique seus arquivos, agentes de IA podem cometer erros. **Recomendamos fortemente:**

    1. **Versione o projeto no Git** — confirme que todos os arquivos estão commitados antes de iniciar a análise
    2. **Tenha o repositório no GitHub** (ou GitLab, Bitbucket) — para ter uma cópia remota segura
    3. **Faça uma cópia local da pasta** — um simples `cp -r meu-projeto meu-projeto-backup` protege contra qualquer imprevisto

    Se algo inesperado acontecer durante a análise, você pode restaurar o estado original com `git restore .` ou a partir da cópia de backup.

!!! warning "O Solucao nunca toca nos seus arquivos"
    Os agentes escrevem **apenas** em `.solucao/` e `_solucao_sdd/`. Nenhum arquivo do seu projeto é modificado, apagado ou sobrescrito. Nunca.

!!! info "Sem chaves de API"
    O Solucao não solicita, não armazena e não transmite chaves de API de nenhum serviço. A inteligência vem do agente que você já usa no ambiente como Claude Code, Codex, Gemini Cli e etc.

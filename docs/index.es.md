# Solucao

**Transforma sistemas heredados en especificaciones ejecutables para agentes de IA.**

¿Conoces ese sistema que nadie quiere tocar? El que lleva 10 años corriendo, genera dinero todos los días, pero nadie sabe bien qué hace por dentro. Solucao fue creado para él.

---

## ¿Qué es Solucao?

Solucao es un framework de ingeniería inversa de especificaciones. Lo instalas dentro del proyecto heredado, activas un agente de IA que ya usas, y él coordina un equipo de especialistas para analizar el código y generar especificaciones completas, trazables y listas para cualquier agente codificador.

**En otras palabras:** Solucao convierte código sin documentación en contratos operacionales que un agente de IA puede entender y usar para evolucionar el sistema con seguridad.

---

## Inicio rápido

En la raíz de tu proyecto:

```bash
npx github:cildefonso/solucao install
```

Luego abre el proyecto en tu agente de IA favorito y elige el flujo:

```
/solucao       # descubrir y especificar un sistema existente
/solucao-new   # convertir una idea nueva en PRD y specs SDD
```

Eso es todo. Solucao toma el volante y te guía hasta el final.

---

## Lo que encontrarás aquí

<div class="grid cards" markdown>

- **Por qué existe Solucao**

    El problema que resuelve y por qué importa.

    [:octicons-arrow-right-24: Leer más](por-que-solucao.md)

- **Instalación**

    Dos minutos y estás listo para empezar.

    [:octicons-arrow-right-24: Instalar](instalacao.md)

- **Pipeline de análisis**

    Las 5 fases que convierten código en especificación.

    [:octicons-arrow-right-24: Ver pipeline](pipeline.md)

- **Agentes**

    7 Teams especializados: Core, New Project, Code Forward, Migration, Documentation, Pricing y Translators.

    [:octicons-arrow-right-24: Ver agentes](agentes/index.md)

- **Empezar un proyecto nuevo**

    Pasa de una idea en una línea a personas, PRD y specs SDD evaluadas.

    [:octicons-arrow-right-24: Usar /solucao-new](newproject/index.md)

</div>

---

## Garantía de seguridad

!!! danger "💾 Haz una copia de seguridad antes de empezar"
    Aunque Solucao nunca modifica tus archivos, los agentes de IA pueden cometer errores. **Recomendamos fuertemente:**

    1. **Versiona el proyecto en Git** — asegúrate de que todos los archivos estén commiteados antes de iniciar el análisis
    2. **Ten el repositorio en GitHub** (o GitLab, Bitbucket) — para tener una copia remota segura
    3. **Haz una copia local de la carpeta** — un simple `cp -r mi-proyecto mi-proyecto-backup` protege contra cualquier imprevisto

    Si algo inesperado ocurre durante el análisis, puedes restaurar el estado original con `git restore .` o desde la copia de seguridad.

!!! warning "Solucao nunca toca tus archivos"
    Los agentes escriben **solo** en `.solucao/` y `_solucao_sdd/`. Ningún archivo de tu proyecto es modificado, eliminado o sobreescrito. Nunca.

!!! info "Sin claves de API"
    Solucao no solicita, no almacena ni transmite claves de API de ningún servicio. La inteligencia viene del agente que ya usas en tu entorno, como Claude Code, Codex, Gemini CLI, etc.

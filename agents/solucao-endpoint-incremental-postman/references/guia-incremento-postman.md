# Guia de Incremento Não-Destrutivo de Endpoints no Postman

Este guia detalha o processo de adição de novas rotas em coleções Postman já existentes sem risco de perda de requisições, variáveis ou scripts customizados.

---

## 1. Verificação Prévia de Existência do Arquivo

A skill incremental **nunca** deve criar uma coleção do zero silenciosamente. Ela pressupõe que o projeto já possui sua coleção base criada pela skill `solucao-endpoint-postman`:

```
Caminho Obrigatório: postman/<artifactId>.postman_collection.json
```

### Algoritmo de Verificação:

1. Obter `<artifactId>` do `pom.xml`.
2. Verificar existência com `Test-Path "postman\$artifactId.postman_collection.json"`.
3. Se não existir:
   - Apresentar alerta: *"Arquivo postman/<artifactId>.postman_collection.json não encontrado. Execute primeiro a skill solucao-endpoint-postman para gerar a coleção inicial."*

---

## 2. Estratégia de Mesclagem Não-Destrutiva

Ao adicionar endpoints de uma nova classe `Resource`:

### 2.1. Variáveis (`variable`)
- Mapear os parâmetros do novo endpoint.
- Para cada parâmetro que mereça virar variável (ex.: `contratoId`, `numeroProposta`):
  ```javascript
  const existe = colecao.variable.some(v => v.key === novaChave);
  if (!existe) {
      colecao.variable.push({
          key: novaChave,
          value: valorExemplo,
          type: "string"
      });
  }
  ```

### 2.2. Pastas e Itens (`item`)
- Obter o nome do grupo funcional a partir de `@Tag(name = "...")`.
- Localizar pasta correspondente:
  ```javascript
  let pasta = colecao.item.find(pasta => pasta.name === nomeTag);
  if (!pasta) {
      pasta = {
          name: nomeTag,
          item: []
      };
      colecao.item.push(pasta);
  }
  ```
- Para cada nova requisição a ser adicionada na pasta:
  - Verificar se já existe uma requisição com o mesmo `name` ou mesma combinação de `method` e `path`.
  - Se não existir, adicionar ao array `pasta.item`.
  - Se já existir, atualizar os detalhes mantendo headers ou testes customizados existentes.

---

## 3. Padrão de Requisições por Nova Classe Resource

Para cada novo Resource adicionado:

| Tipo de Requisição | Rota | Método | Resposta Esperada |
|---|---|---|---|
| **Health do Recurso** | `{{baseUrl}}/api/<recurso>/health` | `GET` | `200 OK` (retorna `"OK"`) |
| **Operação Principal (Sucesso)** | `{{baseUrl}}/api/<recurso>/v1/...` | `GET`/`POST`/`PUT` | `200 OK` ou `201 Created` |
| **Filtros Alternativos** | `{{baseUrl}}/api/<recurso>/v1/...` | `GET` | `200 OK` |
| **Validação - Sem Parâmetros** | `{{baseUrl}}/api/<recurso>/v1/...` | `GET`/`POST` | `400 Bad Request` |
| **Validação - Parâmetro Inválido** | `{{baseUrl}}/api/<recurso>/v1/...` | `GET`/`POST` | `400 Bad Request` |

---

## 4. Validação Pós-Incremento

Sempre execute a validação da sintaxe do JSON com PowerShell:

```powershell
Get-Content postman\<artifactId>.postman_collection.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
```

# Configurações do Opencode

Este repositório contém um backup das minhas configurações do Opencode, incluindo plugins, permissões e habilidades personalizadas.

## Estrutura

- `opencode.json` – Configuração principal do Opencode (schema, plugin, permissões, LSP).
- `package.json` – Dependências do Opencode (apenas o plugin de autenticação Gemini).
- `skills/` – Habilidades customizadas do Opencode, each skill contém um `SKILL.md` e recursos associados.
- `node_modules/` – Dependências instaladas (ignorado pelo Git).

## Habilidades incluídas

- `git-commit`: Executa commits com mensagens convencionais, staging inteligente e geração automática.
- `git-flow-branch-creator`: Cria branches seguindo o modelo Git Flow.
- `skill-creator`: Constrói e avalia habilidades para o Opencode.
- `sql-expert`: Orientação para escrever queries SQL limpas e performáticas.
- `vagrant-file-creator`: Auxilia na criação e otimização de Vagrantfiles.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/RafaelQSantos-RQS/opencode-config.git
   ```
2. Copie os arquivos para o diretório `~/.config/opencode/` (ou onde seu Opencode está configurado para ler).
3. Instale as dependências:
   ```bash
   bun install
   ```
4. Reinicie o Opencode para aplicar as configurações.

## Permissões

As permissões estão definidas em `opencode.json` – a maioria das ferramentas está configurada como `ask` (requer confirmação) para segurança.

## Notas

- O diretório `node_modules/` é ignorado pelo Git.
- As habilidades podem ser ativadas/desativadas conforme necessário.
- Mantenha este repositório privado se contiver informações sensíveis (embora não haja chaves ou tokens aqui).

---

Created with ❤️ for Opencode.
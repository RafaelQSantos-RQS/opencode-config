# Configurações do OpenCode

Este repositório contém um backup das minhas configurações do OpenCode, incluindo plugins, permissões e habilidades personalizadas.

## Estrutura

- `opencode.json` – Configuração principal do OpenCode (schema, plugin, permissões, LSP, MCP).
- `skills/` – Habilidades customizadas do OpenCode, cada skill contém um `SKILL.md` e recursos associados.

## Habilidades incluídas

- `git-commit`: Executa commits com mensagens convencionais, staging inteligente e geração automática.
- `git-flow-branch-creator`: Cria branches seguindo o modelo Git Flow.
- `skill-creator`: Constrói e avalia habilidades para o OpenCode.
- `sql-expert`: Orientação para escrever queries SQL limpas e performáticas.
- `vagrant-file-creator`: Auxilia na criação e otimização de Vagrantfiles.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/RafaelQSantos-RQS/opencode-config.git
   ```
2. Copie os arquivos para o diretório `~/.config/opencode/`:
   ```bash
   cp -r * ~/.config/opencode/
   ```
3. Reinicie o OpenCode para aplicar as configurações.

## Atualizar referências

As referências da skill `skill-creator` podem ser atualizadas com:
```bash
./skills/skill-creator/scripts/update-references.sh
```

## Permissões

As permissões estão definidas em `opencode.json` – a maioria das ferramentas está configurada como `ask` (requer confirmação) para segurança.

## Notas

- As habilidades podem ser ativadas/desativadas conforme necessário.
- Mantenha este repositório privado se contiver informações sensíveis (embora não haja chaves ou tokens aqui).

---

Created with ❤️ for OpenCode.
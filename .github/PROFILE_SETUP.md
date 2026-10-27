# Sincronização do perfil

Conta: https://github.com/ooguuiholiv

Para exibir este README no seu perfil, publique os arquivos no repositório
`ooguuiholiv/ooguuiholiv`, na branch padrão, e habilite o GitHub Actions.
Em **Actions → Update profile cards → Run workflow**, execute a primeira
atualização. O workflow também roda diariamente à meia-noite de Brasília
(03:00 UTC) e quando seus arquivos de automação são alterados.

O script `.github/scripts/sync-profile.py` consulta a API pública do GitHub
para atualizar nome, bio, localização, site e até seis repositórios públicos
não arquivados. Prioriza projetos próprios e depois estrelas. O repositório
do perfil não aparece na lista. O README é gerado: edite
`.github/profile-about.md` para personalizar a apresentação, stack e sistemas.
Esse conteúdo é preservado nas sincronizações diárias. Altere o script para
ajustar a estrutura das seções automáticas.

As estatísticas, linguagens, sequência, troféus e animação de contribuições
são gerados em `profile/`. Antes da primeira execução, o README usa serviços
externos para mostrar os cartões. Sua disponibilidade depende desses serviços.

O token automático do Actions é suficiente para o fluxo padrão. Para incluir
dados privados nas ações que os suportam, configure opcionalmente o secret
`README_STATS_TOKEN` com acesso aos dados desejados. Nunca adicione tokens aos
arquivos do repositório.

Atualização local dos dados públicos:

```sh
python .github/scripts/sync-profile.py
```

O clone mantém seu remote original; confira `git remote -v` antes de publicar
e aponte o destino para seu próprio repositório.

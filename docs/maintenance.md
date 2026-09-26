# Manutenção do perfil

O perfil usa Python 3.10+ e apenas a biblioteca padrão. Imagens e ícones essenciais ficam no próprio repositório. As ilustrações e os ícones funcionais foram criados para este perfil; os rótulos das tecnologias são texto, não selos de certificação.

## Editar

O conteúdo está em `profile.json`. Mantenha as versões `en` e `pt-BR` coerentes. Depois de editar, execute a partir da raiz:

```bash
python3 scripts/build_profile.py
python3 scripts/check_profile.py
python3 -m unittest discover -s examples/evaluation-lab -p 'test_*.py' -v
```

O gerador atualiza os dois READMEs e os SVGs. Arquivos de documentação e código da demonstração são editados diretamente. O gerador não modifica repositórios externos nem a conta do GitHub.

## Adicionar contatos

O campo `contact` aceita uma lista de objetos com `label` e `url`. Adicione apenas destinos atuais e verificados. O campo vazio omite a seção, evitando links fictícios.

## Adicionar projetos reais

`selected_projects` recebe objetos com `name`, `url` e `summary`, sendo `summary` um objeto com textos `en` e `pt-BR`. Inclua apenas trabalhos que possam ser publicados. A lista vazia omite a seção.

Projetos profissionais privados podem ser descritos em nível geral, respeitando o que pode ser divulgado. As notas incluídas neste pacote são referências independentes, não estudos de caso corporativos.

## Automação

O workflow verifica se os arquivos gerados estão atualizados, valida referências locais e SVGs e executa os testes e a demonstração. Ele é acionado por push, pull request ou manualmente. Não escreve na conta nem produz commits artificiais. A política de Dependabot acompanha a dependência do GitHub Actions mensalmente.

O checkout foi fixado ao commit oficial da versão v4.2.2, consultado em 26/09/2026. Confirme os resultados da primeira execução remota após publicar; os comandos foram executados localmente, mas o workflow ainda não foi executado na tua conta.

## Conferir a apresentação

O pacote inclui uma prévia HTML local. Ela aproxima o estilo do README e permite alternar idioma e tema. A renderização final deve ser conferida no GitHub, especialmente imagens em telas estreitas. O GitHub controla os estilos da página ao redor do README.

[Voltar ao perfil](../README.pt-BR.md)

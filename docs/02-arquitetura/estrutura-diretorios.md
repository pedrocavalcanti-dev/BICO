# Estrutura de diretórios

```text
Projeto-Bico/
├── bico_django/
│   ├── config/settings/       # base, development e production
│   ├── apps/                  # core, accounts e audit
│   ├── api/v1/                # API REST versionada
│   ├── templates/             # base e páginas públicas
│   ├── static/css/            # CSS servido pelo Django
│   └── manage.py
├── docs/                      # produto, arquitetura e operação
├── mobile/                    # reservado; Flutter não iniciado
├── .env.example
├── requirements*.txt
└── pyproject.toml
```

`.venv/` e `.env` são locais e ignorados pelo Git. O Django não pode ser movido para a raiz do repositório.

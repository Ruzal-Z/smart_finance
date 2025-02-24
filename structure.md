structure 

├── src/
│  ├── backend/
│  │   ├── __init__.py
│  │   ├── application/
│  │   │   ├── services/
│  │   │   │   └── __init__.py
│  │   │   └── __init__.py
│  │   └── infrastructure/
│  │       ├── repositories/
│  │       │   ├── postgresql/
│  │       │   │   ├── alembic/
│  │       │   │   ├── models/
│  │       │   │   ├── repository/
│  │       │   │   ├── schemas/
│  │       │   │   └── __init__.py
│  │       └── web/
│  │           ├── api/
│  │           │   └── api_v1
│  │           ├── app.py
│  │           └── config.py
│  └── frontend/
│      ├── ...
├── pyproject.toml
├── README.md
└── ...

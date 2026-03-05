# Desktop App em Python (Tkinter)

Este projeto é uma aplicação desktop simples em Python, usando **Tkinter**, sem dependências externas nem Docker.

---

## Requisitos

- **Windows 10/11**
- **Python 3.11+** instalado

Não é necessário Docker.

---

## Instalação do ambiente

No PowerShell:

```bash
cd C:\projeto
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

O ficheiro `requirements.txt` não tem dependências externas (Tkinter vem incluído com o Python).

---

## Correr a aplicação

Com o ambiente virtual ativo:

```bash
python main.py
```

Funcionalidade atual:

- Janela 800x600.
- Página inicial com fundo azul e botão **“Começar”**.
- Ao clicar em **“Começar”**, abre uma segunda página com texto e botão **“Voltar”** para regressar.

---

## Testes e qualidade de código

Ferramentas configuradas (em `requirements-dev.txt` e `pyproject.toml`):

- **pytest** – testes unitários (pasta `tests/`).
- **ruff** – linting.
- **black** – formatação automática.
- **mypy** – type checking.
- **build** – criação de distribuições (wheel/sdist).

Com o ambiente virtual ativo:

```bash
pytest          # testes
ruff check .    # lint
black .         # formatar
mypy .          # type-check
python -m build # build do projeto
```

---

## CI (GitHub Actions)

Se usares GitHub, o workflow em `.github/workflows/ci.yml`:

- Instala dependências.
- Corre ruff, black (check), mypy, pytest.
- Valida o build do projeto (`python -m build`).

Não há qualquer passo relacionado com Docker.


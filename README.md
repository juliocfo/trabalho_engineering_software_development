# Config Validator

Microsserviço de validação de trechos de configuração de rede (estilo Cisco IOS),
desenvolvido como trabalho final da disciplina **Engineering Software Development**.

Caminho escolhido: **Test Suite** (suíte de testes automatizados com pytest).

## Integrantes

- Julio Cezar (RM369185)
- Ailton Lima (RM365720)
- Kaue Abreu (RM368524)

## O que o serviço faz

Recebe um bloco de configuração como **texto puro** e valida, linha a linha:

- **VLAN** (`switchport access vlan <n>`) — precisa estar entre 1 e 4094.
- **Interface** (`interface <nome>`) — precisa seguir um padrão de nome reconhecido
  (ex: `GigabitEthernet0/1`, `TenGigE0/0/0/1`, `Vlan100`, `Loopback0`).
- **IPv4/CIDR** (`ip address <ip>/<prefixo>`) — precisa ser um endereço/prefixo IPv4 válido.
- **IPv6/CIDR** (`ipv6 address <ip>/<prefixo>`) — precisa ser um endereço/prefixo IPv6 válido.

O retorno é um relatório indicando se a configuração é válida como um todo e a lista
de erros encontrados (linha, tipo, mensagem).

## Stack

- Python 3
- FastAPI + Uvicorn (API HTTP mínima)
- pytest (Test Suite)

## Estrutura

```
src/config_validator/
    validator.py   # regras de validação e parsing do config
    api.py         # API FastAPI (POST /validate, GET /health)
tests/
    test_validator.py  # testes unitários das regras
    test_api.py         # testes da API
```

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# rodar a API
uvicorn src.config_validator.api:app --reload

# rodar os testes
pytest -v
```

### Exemplo de uso da API

```bash
curl -X POST http://127.0.0.1:8000/validate \
  -H "Content-Type: application/json" \
  -d '{"config": "interface GigabitEthernet0/1\n switchport access vlan 100\n ip address 10.0.0.1/24"}'
```

Veja `DOCUMENTACAO.md` para a descrição sucinta do que foi feito, e `EXEMPLOS.md` (+ pasta `examples/`) para blocos de configuração prontos para testar manualmente.

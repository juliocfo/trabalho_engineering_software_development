# Exemplos de Entrada para Teste

Esta pasta `examples/` traz blocos de configuração prontos para quem quiser testar ou avaliar
o Config Validator manualmente (via API ou importando `validate_config` direto em Python),
sem precisar escrever nada do zero.

## Como usar

Com a API rodando (`uvicorn src.config_validator.api:app --reload`), teste qualquer exemplo assim:

```bash
curl -X POST http://127.0.0.1:8000/validate \
  -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys;print(json.dumps({"config": open(sys.argv[1]).read()}))' examples/config_valido.txt)"
```

Troque `examples/config_valido.txt` pelo arquivo do exemplo que quiser testar.

Ou, sem subir a API, direto em Python:

```python
from src.config_validator.validator import validate_config

with open("examples/config_valido.txt") as f:
    print(validate_config(f.read()))
```

## Exemplos disponíveis

### 1. `config_valido.txt` — configuração 100% válida

```
interface GigabitEthernet0/1
 switchport access vlan 100
 ip address 10.0.0.1/24
!
interface GigabitEthernet0/2
 ipv6 address 2001:db8::1/64
```

Resultado esperado:

```json
{"valid": true, "checked_lines": 5, "errors": []}
```

### 2. `config_invalido_vlan.txt` — VLAN fora do range (1-4094)

```
interface GigabitEthernet0/1
 switchport access vlan 9000
```

Resultado esperado: `valid: false`, 1 erro do tipo `vlan` (VLAN 9000 fora do range).

### 3. `config_invalido_interface.txt` — nome de interface não reconhecido

```
interface PortaQualquer1
 switchport access vlan 10
```

Resultado esperado: `valid: false`, 1 erro do tipo `interface`.

### 4. `config_invalido_ipv4.txt` — endereço IPv4 inválido

```
interface GigabitEthernet0/1
 ip address 999.999.999.999/24
```

Resultado esperado: `valid: false`, 1 erro do tipo `ipv4`.

### 5. `config_invalido_ipv6.txt` — prefixo IPv6 fora do range (0-128)

```
interface GigabitEthernet0/1
 ipv6 address 2001:db8::1/200
```

Resultado esperado: `valid: false`, 1 erro do tipo `ipv6`.

### 6. `config_multiplos_erros.txt` — várias regras quebradas ao mesmo tempo

```
interface PortaInvalida
 switchport access vlan 9999
 ip address 999.999.999.999/24
 ipv6 address 2001:db8::1/200
```

Resultado esperado: `valid: false`, 4 erros (um de cada tipo: `interface`, `vlan`, `ipv4`, `ipv6`).

## Relação com os testes automatizados

Todos os cenários acima também estão cobertos por asserts em `tests/test_validator.py` e
`tests/test_api.py` — esses arquivos de exemplo servem para quem quiser testar manualmente
(via curl, Postman ou linha de comando), sem precisar rodar a suíte pytest.

# Documentação — Config Validator

## Objetivo

Este projeto é a entrega final da disciplina Engineering Software Development. Optamos por
desenvolver um microsserviço de **validação de configurações de rede** (Config Validator),
inspirado no trabalho real de revisão de mudanças em switches/roteadores. Como caminho de
avaliação, escolhemos a **Suíte de Testes** (Test Suite).

## O que foi feito

O microsserviço recebe um bloco de configuração em texto puro (formato Cisco IOS) e aplica
regras de validação sobre quatro tipos de diretiva: VLAN, nome de interface, endereço IPv4/CIDR
e endereço IPv6/CIDR. Cada linha reconhecida é validada isoladamente e o serviço devolve um
relatório consolidado (`valid`, `checked_lines`, `errors`) apontando exatamente qual linha e
qual regra falhou.

A exposição do serviço foi feita como uma API HTTP mínima usando **FastAPI**, com dois
endpoints: `GET /health` (checagem de disponibilidade) e `POST /validate` (recebe o texto de
configuração e retorna o relatório de validação).

## Suíte de Testes

Foram implementados **14 testes automatizados** com pytest, distribuídos em dois arquivos:

- `tests/test_validator.py` — 10 testes cobrindo as regras de negócio isoladamente: VLAN
  dentro/fora do range, VLAN não numérica, interface válida/inválida, IPv4 válido/inválido,
  IPv6 válido/inválido, e dois testes de configuração completa (uma válida e uma com múltiplos
  erros simultâneos).
- `tests/test_api.py` — 3 testes exercitando a API de ponta a ponta via `TestClient` do
  FastAPI (health check, validação de config válida e inválida pelo endpoint).

## Como executar

Instruções completas de instalação e execução estão no `README.md`.

"""
Config Validator
-----------------
Regras de validacao simples para trechos de configuracao de rede em estilo
Cisco IOS, recebidos como texto puro. Suporta VLAN, nome de interface,
IPv4/CIDR e IPv6/CIDR.
"""
import ipaddress
import re

VLAN_MIN = 1
VLAN_MAX = 4094

INTERFACE_PATTERN = re.compile(
    r"^(Ethernet|FastEthernet|GigabitEthernet|TenGigabitEthernet|TenGigE|"
    r"HundredGigE|TwentyFiveGigE|FortyGigE|Vlan|Loopback|Port-channel|"
    r"Tunnel|Serial|Management|mgmt)\d+(/\d+)*(\.\d+)?$",
    re.IGNORECASE,
)


def validate_vlan(vlan_str):
    """Valida se um numero de VLAN esta dentro do range permitido (1-4094)."""
    try:
        vlan = int(vlan_str)
    except (TypeError, ValueError):
        return False, f"VLAN '{vlan_str}' nao e um numero valido."
    if VLAN_MIN <= vlan <= VLAN_MAX:
        return True, None
    return False, f"VLAN {vlan} fora do range valido ({VLAN_MIN}-{VLAN_MAX})."


def validate_interface_name(name):
    """Valida se o nome da interface segue um padrao reconhecido (ex: GigabitEthernet0/1)."""
    if name and INTERFACE_PATTERN.match(name.strip()):
        return True, None
    return False, f"Nome de interface '{name}' nao segue um padrao reconhecido."


def validate_ip_cidr(ip_str):
    """
    Valida um endereco IP com prefixo CIDR, aceitando IPv4 e IPv6
    (ex: '10.0.0.1/24' ou '2001:db8::1/64').
    """
    try:
        interface = ipaddress.ip_interface(ip_str)
    except ValueError:
        return False, f"Endereco '{ip_str}' nao e um IPv4/IPv6 com CIDR valido."

    version = interface.version
    max_prefix = 32 if version == 4 else 128
    if not (0 <= interface.network.prefixlen <= max_prefix):
        return False, f"Prefixo CIDR invalido para IPv{version}: '{ip_str}'."
    return True, None


# --- Parsing e validacao de um bloco de configuracao completo ---

LINE_PARSERS = [
    (re.compile(r"^interface\s+(?P<value>\S+)", re.IGNORECASE), "interface"),
    (re.compile(r"^switchport\s+access\s+vlan\s+(?P<value>\S+)", re.IGNORECASE), "vlan"),
    (re.compile(r"^ip\s+address\s+(?P<value>\S+)", re.IGNORECASE), "ipv4"),
    (re.compile(r"^ipv6\s+address\s+(?P<value>\S+)", re.IGNORECASE), "ipv6"),
]

VALIDATORS = {
    "interface": validate_interface_name,
    "vlan": validate_vlan,
    "ipv4": validate_ip_cidr,
    "ipv6": validate_ip_cidr,
}


def parse_config(config_text):
    """
    Percorre o texto da configuracao linha a linha e identifica diretivas
    reconhecidas (interface, vlan, ip address, ipv6 address).
    Retorna uma lista de tuplas (numero_da_linha, tipo, valor, linha_bruta).
    """
    directives = []
    for line_number, raw_line in enumerate(config_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("!"):
            continue
        for pattern, directive_type in LINE_PARSERS:
            match = pattern.match(line)
            if match:
                directives.append((line_number, directive_type, match.group("value"), raw_line))
                break
    return directives


def validate_config(config_text):
    """
    Valida um bloco de configuracao de texto puro e retorna um relatorio:
    {
        "valid": bool,
        "checked_lines": int,
        "errors": [{"line": int, "type": str, "message": str, "raw": str}, ...]
    }
    """
    directives = parse_config(config_text)
    errors = []

    for line_number, directive_type, value, raw_line in directives:
        validator = VALIDATORS[directive_type]
        is_valid, message = validator(value)
        if not is_valid:
            errors.append({
                "line": line_number,
                "type": directive_type,
                "message": message,
                "raw": raw_line.strip(),
            })

    return {
        "valid": len(errors) == 0,
        "checked_lines": len(directives),
        "errors": errors,
    }

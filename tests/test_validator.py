from src.config_validator.validator import (
    validate_vlan,
    validate_interface_name,
    validate_ip_cidr,
    validate_config,
)


def test_validate_vlan_dentro_do_range():
    ok, msg = validate_vlan("100")
    assert ok is True
    assert msg is None


def test_validate_vlan_fora_do_range():
    ok, msg = validate_vlan("5000")
    assert ok is False
    assert "fora do range" in msg


def test_validate_vlan_nao_numerica():
    ok, msg = validate_vlan("abc")
    assert ok is False


def test_validate_interface_valida():
    ok, msg = validate_interface_name("GigabitEthernet0/1")
    assert ok is True
    assert msg is None


def test_validate_interface_invalida():
    ok, msg = validate_interface_name("PortaQualquer1")
    assert ok is False


def test_validate_ipv4_cidr_valido():
    ok, msg = validate_ip_cidr("10.0.0.1/24")
    assert ok is True


def test_validate_ipv4_cidr_invalido():
    ok, msg = validate_ip_cidr("10.0.0.999/24")
    assert ok is False


def test_validate_ipv6_cidr_valido():
    ok, msg = validate_ip_cidr("2001:db8::1/64")
    assert ok is True


def test_validate_ipv6_cidr_invalido():
    ok, msg = validate_ip_cidr("2001:db8::1/200")
    assert ok is False


def test_validate_config_completo_valido():
    config_text = """
    interface GigabitEthernet0/1
     switchport access vlan 100
     ip address 10.0.0.1/24
    !
    interface GigabitEthernet0/2
     ipv6 address 2001:db8::1/64
    """
    result = validate_config(config_text)
    assert result["valid"] is True
    assert result["checked_lines"] == 5
    assert result["errors"] == []


def test_validate_config_com_erros():
    config_text = """
    interface PortaInvalida
     switchport access vlan 9999
     ip address 999.999.999.999/24
    """
    result = validate_config(config_text)
    assert result["valid"] is False
    assert len(result["errors"]) == 3

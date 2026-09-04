#!/usr/bin/env python
"""
Script automatizado para executar testes do backend Arkheion

Uso:
    python backend/tests.py                 # Executa todos os testes
    python backend/tests.py --models        # Apenas testes de models
    python backend/tests.py --serializers   # Apenas testes de serializers
    python backend/tests.py --fast          # Execução paralela (mais rápido)
    python backend/tests.py --verbose       # Modo verboso
    python backend/tests.py --coverage      # Com cobertura de código
"""

import sys
import os
import subprocess


# Cores para output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(text):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    """Imprime informação"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def run_command(cmd, description):
    """Executa comando e retorna resultado"""
    print_info(f"Executando: {description}")
    print(f"{Colors.WARNING}Comando: {' '.join(cmd)}{Colors.ENDC}\n")

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print_success(f"{description} - PASSOU")
        return True
    else:
        print_error(f"{description} - FALHOU")
        return False


def get_base_command():
    """Retorna comando base do Django"""
    # Detecta se estamos no diretório do manage.py
    if os.path.exists("manage.py"):
        return ["python", "manage.py", "test"]
    else:
        # Assume que estamos em backend/ e manage.py está em ../
        return ["python", "../manage.py", "test"]


def run_all_tests(verbose=False, parallel=False, coverage=False):
    """Executa todos os testes"""
    print_header("EXECUTANDO TODOS OS TESTES DO BACKEND")

    cmd = get_base_command()
    cmd.append("backend.tests")

    if verbose:
        cmd.extend(["-v", "2"])

    if parallel:
        cmd.append("--parallel")

    if coverage:
        # Usar coverage se disponível
        cmd = ["coverage", "run", "--source=backend"] + cmd[1:]

    success = run_command(cmd, "Todos os testes")

    if coverage and success:
        print_info("Gerando relatório de cobertura...")
        subprocess.run(["coverage", "report"])
        subprocess.run(["coverage", "html"])
        print_success("Relatório HTML gerado em htmlcov/index.html")

    return success


def run_model_tests(verbose=False, parallel=False):
    """Executa apenas testes de models"""
    print_header("EXECUTANDO TESTES DE MODELS")

    test_modules = [
        (
            "backend.tests.test_models_basicos",
            "Models Básicos (Atributo, Perícia, Classe, etc.)",
        ),
        ("backend.tests.test_models_ficha", "Models de Ficha"),
    ]

    all_success = True
    for module, description in test_modules:
        cmd = get_base_command()
        cmd.append(module)

        if verbose:
            cmd.extend(["-v", "2"])

        if parallel:
            cmd.append("--parallel")

        success = run_command(cmd, description)
        all_success = all_success and success
        print()  # Linha em branco entre testes

    return all_success


def run_serializer_tests(verbose=False, parallel=False):
    """Executa apenas testes de serializers"""
    print_header("EXECUTANDO TESTES DE SERIALIZERS")

    test_modules = [
        ("backend.tests.test_serializers_auth", "Serializers de Autenticação"),
        ("backend.tests.test_serializers_basicos", "Serializers Básicos"),
        ("backend.tests.test_serializers_ficha", "Serializers de Ficha"),
    ]

    all_success = True
    for module, description in test_modules:
        cmd = get_base_command()
        cmd.append(module)

        if verbose:
            cmd.extend(["-v", "2"])

        if parallel:
            cmd.append("--parallel")

        success = run_command(cmd, description)
        all_success = all_success and success
        print()  # Linha em branco entre testes

    return all_success


def print_summary(success, test_type="todos os testes"):
    """Imprime resumo final"""
    print_header("RESUMO")

    if success:
        print_success(f"Todos {test_type} passaram com sucesso! 🎉")
        print(f"\n{Colors.OKGREEN}Status: OK ✓{Colors.ENDC}")
    else:
        print_error(f"Alguns {test_type} falharam.")
        print(f"\n{Colors.FAIL}Status: FALHOU ✗{Colors.ENDC}")
        print(
            f"\n{Colors.WARNING}Verifique os erros acima para mais detalhes.{Colors.ENDC}"
        )

    print()


def print_usage():
    """Imprime instruções de uso"""
    print(__doc__)
    print("\nExemplos:")
    print("  python backend/tests.py")
    print("  python backend/tests.py --models --verbose")
    print("  python backend/tests.py --serializers --fast")
    print("  python backend/tests.py --coverage")
    print()


def main():
    """Função principal"""
    args = sys.argv[1:]

    # Parse argumentos
    verbose = "--verbose" in args or "-v" in args
    parallel = "--fast" in args or "--parallel" in args
    coverage = "--coverage" in args
    models_only = "--models" in args
    serializers_only = "--serializers" in args
    show_help = "--help" in args or "-h" in args

    if show_help:
        print_usage()
        return 0

    print_header("SISTEMA DE TESTES AUTOMATIZADO - ARKHEION BACKEND")
    print_info(f"Diretório atual: {os.getcwd()}")
    print_info(f"Modo verboso: {'Ativado' if verbose else 'Desativado'}")
    print_info(f"Execução paralela: {'Ativada' if parallel else 'Desativada'}")
    print_info(f"Cobertura de código: {'Ativada' if coverage else 'Desativada'}")
    print()

    success = True
    test_type = "todos os testes"

    if models_only:
        test_type = "testes de models"
        success = run_model_tests(verbose, parallel)
    elif serializers_only:
        test_type = "testes de serializers"
        success = run_serializer_tests(verbose, parallel)
    else:
        success = run_all_tests(verbose, parallel, coverage)

    print_summary(success, test_type)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

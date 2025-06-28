#!/bin/bash

# Script para executar testes do Brain Agriculture Backend
# Suporta execução local e via Docker

echo "Executando testes do Brain Agriculture Backend"
echo "=================================================="

# Detectar se está rodando dentro do Docker
if [ -f /.dockerenv ] || [ -f /proc/1/cgroup ] && grep -q docker /proc/1/cgroup; then
    echo "Executando dentro do container Docker"
    DOCKER_MODE=true
else
    echo "Executando localmente"
    DOCKER_MODE=false
fi

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -u, --unit          Executa apenas testes unitários"
    echo "  -i, --integration   Executa apenas testes de integração"
    echo "  -c, --coverage      Executa testes com relatório de cobertura"
    echo "  -v, --verbose       Executa testes com saída verbosa"
    echo "  -f, --fast          Executa testes rapidamente (sem cobertura)"
    echo "  -d, --docker        Força execução via Docker (se disponível)"
    echo "  -l, --local         Força execução local"
    echo ""
    echo "Exemplos:"
    echo "  $0                  # Executa todos os testes"
    echo "  $0 -u              # Apenas testes unitários"
    echo "  $0 -c              # Com cobertura de código"
    echo "  $0 -v -c           # Verboso com cobertura"
    echo "  $0 -d              # Via Docker"
    echo "  $0 -d -u           # Via Docker, apenas unitários"
    echo ""
    echo "Docker Commands:"
    echo "  docker-compose -f docker-compose.test.yml --profile test up test-app"
    echo "  docker-compose -f docker-compose.test.yml --profile test up test-app-unit"
    echo "  docker-compose -f docker-compose.test.yml --profile test up test-app-integration"
}

# Processar argumentos
UNIT_ONLY=false
INTEGRATION_ONLY=false
COVERAGE=false
VERBOSE=false
FAST=false
FORCE_DOCKER=false
FORCE_LOCAL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--unit)
            UNIT_ONLY=true
            shift
            ;;
        -i|--integration)
            INTEGRATION_ONLY=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fast)
            FAST=true
            shift
            ;;
        -d|--docker)
            FORCE_DOCKER=true
            shift
            ;;
        -l|--local)
            FORCE_LOCAL=true
            shift
            ;;
        *)
            echo "Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Função para executar testes localmente
run_local_tests() {
    echo "Executando testes localmente..."
    
    # Verificar se o pytest está instalado
    if ! command -v pytest &> /dev/null; then
        echo "pytest não encontrado. Instalando dependências..."
        pip install -r requirements/development.txt
    fi
    
    # Configurar comando pytest
    PYTEST_CMD="pytest"
    
    # Adicionar opções baseadas nos argumentos
    if [ "$VERBOSE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD -v"
    fi
    
    if [ "$COVERAGE" = true ] && [ "$FAST" = false ]; then
        PYTEST_CMD="$PYTEST_CMD --cov=app --cov-report=term-missing --cov-report=html"
    fi
    
    if [ "$UNIT_ONLY" = true ]; then
        PYTEST_CMD="$PYTEST_CMD tests/unit/"
        echo "Executando apenas testes unitários..."
    elif [ "$INTEGRATION_ONLY" = true ]; then
        PYTEST_CMD="$PYTEST_CMD tests/integration/"
        echo "Executando apenas testes de integração..."
    else
        echo "Executando todos os testes..."
    fi
    
    # Executar os testes
    echo "Comando: $PYTEST_CMD"
    echo ""
    
    eval $PYTEST_CMD
    return $?
}

# Função para executar testes via Docker
run_docker_tests() {
    echo "Executando testes via Docker..."
    
    # Verificar se docker-compose está disponível
    if ! command -v docker-compose &> /dev/null; then
        echo "docker-compose não encontrado. Tentando execução local..."
        run_local_tests
        return $?
    fi
    
    # Verificar se o arquivo docker-compose.test.yml existe
    if [ ! -f "docker-compose.test.yml" ]; then
        echo "docker-compose.test.yml não encontrado. Tentando execução local..."
        run_local_tests
        return $?
    fi
    
    # Determinar qual serviço executar
    if [ "$UNIT_ONLY" = true ]; then
        SERVICE="test-app-unit"
        echo "Executando apenas testes unitários via Docker..."
    elif [ "$INTEGRATION_ONLY" = true ]; then
        SERVICE="test-app-integration"
        echo "Executando apenas testes de integração via Docker..."
    else
        SERVICE="test-app"
        echo "Executando todos os testes via Docker..."
    fi
    
    # Construir e executar
    echo "Construindo imagem de teste..."
    docker-compose -f docker-compose.test.yml build $SERVICE
    
    echo "Executando testes..."
    docker-compose -f docker-compose.test.yml --profile test up --abort-on-container-exit $SERVICE
    
    # Capturar código de saída
    EXIT_CODE=$(docker-compose -f docker-compose.test.yml --profile test ps -q $SERVICE | xargs docker inspect -f '{{.State.ExitCode}}')
    
    # Limpar containers
    echo "Limpando containers..."
    docker-compose -f docker-compose.test.yml --profile test down
    
    return $EXIT_CODE
}

# Decidir como executar os testes
if [ "$FORCE_DOCKER" = true ]; then
    echo "Forçando execução via Docker..."
    run_docker_tests
    EXIT_CODE=$?
elif [ "$FORCE_LOCAL" = true ]; then
    echo "Forçando execução local..."
    run_local_tests
    EXIT_CODE=$?
elif [ "$DOCKER_MODE" = true ]; then
    # Já está dentro do Docker, executar localmente
    run_local_tests
    EXIT_CODE=$?
else
    # Verificar se Docker está disponível e preferir Docker
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        echo "Docker disponível. Executando via Docker..."
        run_docker_tests
        EXIT_CODE=$?
    else
        echo "Docker não disponível. Executando localmente..."
        run_local_tests
        EXIT_CODE=$?
    fi
fi

echo ""
echo "=================================================="

# Verificar resultado
if [ $EXIT_CODE -eq 0 ]; then
    echo "Todos os testes passaram!"
    
    if [ "$COVERAGE" = true ] && [ "$FAST" = false ]; then
        echo ""
        echo "Relatório de cobertura gerado em: htmlcov/index.html"
        echo "Abra o arquivo no navegador para ver detalhes da cobertura"
    fi
else
    echo "Alguns testes falharam!"
    echo "Verifique os logs acima para mais detalhes"
fi

echo ""
echo "Finalizado com código de saída: $EXIT_CODE"
exit $EXIT_CODE 
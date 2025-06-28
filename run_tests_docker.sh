#!/bin/bash

# Script específico para executar testes via Docker
# Mais simples e direto para uso em CI/CD

echo "Executando testes via Docker - Brain Agriculture Backend"
echo "=========================================================="

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
    echo "  -b, --build         Reconstrói a imagem antes de executar"
    echo "  -k, --keep          Mantém containers rodando após testes"
    echo ""
    echo "Exemplos:"
    echo "  $0                  # Executa todos os testes"
    echo "  $0 -u              # Apenas testes unitários"
    echo "  $0 -c -b           # Com cobertura e rebuild"
    echo "  $0 -i -k           # Integração e manter containers"
}

# Processar argumentos
UNIT_ONLY=false
INTEGRATION_ONLY=false
COVERAGE=false
VERBOSE=false
BUILD=false
KEEP_CONTAINERS=false

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
        -b|--build)
            BUILD=true
            shift
            ;;
        -k|--keep)
            KEEP_CONTAINERS=true
            shift
            ;;
        *)
            echo "Opção desconhecida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose não encontrado!"
    echo "Instale o Docker e docker-compose para continuar"
    exit 1
fi

# Verificar se o arquivo docker-compose.test.yml existe
if [ ! -f "docker-compose.test.yml" ]; then
    echo "docker-compose.test.yml não encontrado!"
    echo "Verifique se o arquivo existe no diretório atual"
    exit 1
fi

# Determinar qual serviço executar
if [ "$UNIT_ONLY" = true ]; then
    SERVICE="test-app-unit"
    echo "Executando apenas testes unitários..."
elif [ "$INTEGRATION_ONLY" = true ]; then
    SERVICE="test-app-integration"
    echo "Executando apenas testes de integração..."
else
    SERVICE="test-app"
    echo "Executando todos os testes..."
fi

# Construir imagem se solicitado
if [ "$BUILD" = true ]; then
    echo "Construindo imagem de teste..."
    docker-compose -f docker-compose.test.yml build $SERVICE
    if [ $? -ne 0 ]; then
        echo "Falha ao construir imagem!"
        exit 1
    fi
fi

# Preparar comando docker-compose
COMPOSE_CMD="docker-compose -f docker-compose.test.yml --profile test"

# Adicionar opções baseadas nos argumentos
if [ "$VERBOSE" = true ]; then
    echo "Modo verboso ativado"
fi

if [ "$COVERAGE" = true ]; then
    echo "Relatório de cobertura será gerado"
fi

# Executar testes
echo "Iniciando containers e executando testes..."
echo "Serviço: $SERVICE"

if [ "$KEEP_CONTAINERS" = true ]; then
    echo "Containers serão mantidos após execução"
    $COMPOSE_CMD up $SERVICE
else
    echo "Containers serão removidos após execução"
    $COMPOSE_CMD up --abort-on-container-exit $SERVICE
fi

# Capturar código de saída
EXIT_CODE=$?

# Limpar containers se não foi solicitado manter
if [ "$KEEP_CONTAINERS" = false ]; then
    echo "Limpando containers..."
    $COMPOSE_CMD down
else
    echo "Containers mantidos. Use 'docker-compose -f docker-compose.test.yml down' para limpar"
fi

echo ""
echo "=========================================================="

# Verificar resultado
if [ $EXIT_CODE -eq 0 ]; then
    echo "Todos os testes passaram!"
    
    if [ "$COVERAGE" = true ]; then
        echo ""
        echo "Relatório de cobertura:"
        echo "   - HTML: htmlcov/index.html"
        echo "   - Terminal: Ver logs acima"
        echo "Para acessar o relatório HTML, copie a pasta htmlcov do container"
    fi
else
    echo "Alguns testes falharam!"
    echo "Verifique os logs acima para mais detalhes"
    
    if [ "$KEEP_CONTAINERS" = true ]; then
        echo "Containers mantidos para inspeção"
        echo "Use 'docker-compose -f docker-compose.test.yml logs $SERVICE' para ver logs"
    fi
fi

echo ""
echo "Finalizado com código de saída: $EXIT_CODE"
exit $EXIT_CODE 
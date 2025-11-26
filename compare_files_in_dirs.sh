#!/bin/bash

# Script genérico para comparar dos directorios de proyectos Python
# Excluye automáticamente: .git, virtualenv (bin/lib/include/share), 
# __pycache__, archivos compilados, y otros temporales

USE_BASENAME=false

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--basename)
            USE_BASENAME=true
            shift
            ;;
        *)
            if [ -z "$DIR1" ]; then
                DIR1="$1"
            elif [ -z "$DIR2" ]; then
                DIR2="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$DIR1" ] || [ -z "$DIR2" ]; then
    echo "Uso: $0 [-b|--basename] <directorio1> <directorio2>"
    echo ""
    echo "Opciones:"
    echo "  -b, --basename    Comparar solo por nombre de archivo, ignorando la ubicación"
    echo ""
    echo "Ejemplos:"
    echo "  $0 ~/omar ~/omar-claude"
    echo "  $0 -b ~/omar ~/omar-claude    # ignora si archivos se movieron de lugar"
    exit 1
fi

if [ ! -d "$DIR1" ]; then
    echo "Error: $DIR1 no existe o no es un directorio"
    exit 1
fi

if [ ! -d "$DIR2" ]; then
    echo "Error: $DIR2 no existe o no es un directorio"
    exit 1
fi

DIR1_NAME=$(basename "$DIR1")
DIR2_NAME=$(basename "$DIR2")

echo "====================================="
echo "Comparando proyectos Python:"
echo "  DIR1: $DIR1_NAME ($DIR1)"
echo "  DIR2: $DIR2_NAME ($DIR2)"
if $USE_BASENAME; then
    echo "  Modo: Comparación por NOMBRE DE ARCHIVO (ignorando ubicación)"
else
    echo "  Modo: Comparación por RUTA COMPLETA"
fi
echo "====================================="
echo ""

# Función para obtener lista de archivos excluyendo cosas irrelevantes
get_file_list() {
    local dir=$1
    find "$dir" -type f \
        ! -path "*/.git/*" \
        ! -path "*/bin/*" \
        ! -path "*/include/*" \
        ! -path "*/lib/*" \
        ! -path "*/lib64/*" \
        ! -path "*/share/*" \
        ! -path "*/.venv/*" \
        ! -path "*/venv/*" \
        ! -path "*/env/*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/.*cache*/*" \
        ! -path "*/.pytest_cache/*" \
        ! -path "*/.mypy_cache/*" \
        ! -path "*/node_modules/*" \
        ! -path "*/.tox/*" \
        ! -path "*/.eggs/*" \
        ! -path "*/dist/*" \
        ! -path "*/build/*" \
        ! -path "*/.coverage.*" \
        ! -name "*.pyc" \
        ! -name "*.pyo" \
        ! -name "*.so" \
        ! -name "*.egg-info" \
        ! -name ".DS_Store" \
        ! -name "*.swp" \
        ! -name "*.swo" \
        ! -name "*~" \
        ! -name ".coverage" \
        ! -name "pip-selfcheck.json" \
        | sed "s|^$dir/||" | sort
}

# Función para obtener solo basenames
get_basename_list() {
    local dir=$1
    get_file_list "$dir" | while read file; do
        basename "$file"
    done | sort | uniq
}

# Función para obtener lista de directorios excluyendo cosas irrelevantes
get_dir_list() {
    local dir=$1
    find "$dir" -type d \
        ! -path "*/.git*" \
        ! -path "*/bin" \
        ! -path "*/bin/*" \
        ! -path "*/include" \
        ! -path "*/include/*" \
        ! -path "*/lib" \
        ! -path "*/lib/*" \
        ! -path "*/lib64" \
        ! -path "*/lib64/*" \
        ! -path "*/share" \
        ! -path "*/share/*" \
        ! -path "*/.venv*" \
        ! -path "*/venv*" \
        ! -path "*/env" \
        ! -path "*/env/*" \
        ! -path "*/__pycache__*" \
        ! -path "*/.*cache*" \
        ! -path "*/node_modules*" \
        ! -path "*/.tox*" \
        ! -path "*/.eggs*" \
        ! -path "*/dist" \
        ! -path "*/dist/*" \
        ! -path "*/build" \
        ! -path "*/build/*" \
        | sed "s|^$dir/||" | grep -v "^\.$" | sort
}

echo "📁 DIRECTORIOS EN $DIR1_NAME:"
echo "--------------------------------------------------------"
get_dir_list "$DIR1"
echo ""

echo "📁 DIRECTORIOS EN $DIR2_NAME:"
echo "--------------------------------------------------------"
get_dir_list "$DIR2"
echo ""

if $USE_BASENAME; then
    # Modo basename: comparar solo nombres de archivo
    echo "📄 NOMBRES DE ARCHIVOS EN $DIR1_NAME (únicos):"
    echo "--------------------------------------------------------"
    DIR1_FILES=$(mktemp)
    get_basename_list "$DIR1" > "$DIR1_FILES"
    cat "$DIR1_FILES"
    echo ""
    echo "Total archivos únicos: $(wc -l < "$DIR1_FILES")"
    echo ""

    echo "📄 NOMBRES DE ARCHIVOS EN $DIR2_NAME (únicos):"
    echo "--------------------------------------------------------"
    DIR2_FILES=$(mktemp)
    get_basename_list "$DIR2" > "$DIR2_FILES"
    cat "$DIR2_FILES"
    echo ""
    echo "Total archivos únicos: $(wc -l < "$DIR2_FILES")"
    echo ""
else
    # Modo normal: comparar rutas completas
    echo "📄 ARCHIVOS EN $DIR1_NAME:"
    echo "--------------------------------------------------------"
    DIR1_FILES=$(mktemp)
    get_file_list "$DIR1" > "$DIR1_FILES"
    cat "$DIR1_FILES"
    echo ""
    echo "Total archivos: $(wc -l < "$DIR1_FILES")"
    echo ""

    echo "📄 ARCHIVOS EN $DIR2_NAME:"
    echo "--------------------------------------------------------"
    DIR2_FILES=$(mktemp)
    get_file_list "$DIR2" > "$DIR2_FILES"
    cat "$DIR2_FILES"
    echo ""
    echo "Total archivos: $(wc -l < "$DIR2_FILES")"
    echo ""
fi

echo "🔍 ANÁLISIS DE DIFERENCIAS:"
echo "=========================================="
echo ""

if $USE_BASENAME; then
    echo "❌ Archivos (por nombre) en $DIR1_NAME pero NO en $DIR2_NAME:"
else
    echo "❌ Archivos en $DIR1_NAME pero NO en $DIR2_NAME:"
fi
echo "------------------------------------------------------"
comm -23 "$DIR1_FILES" "$DIR2_FILES" | while read file; do
    echo "  - $file"
done
MISSING=$(comm -23 "$DIR1_FILES" "$DIR2_FILES" | wc -l)
echo "Total: $MISSING archivos"
echo ""

if $USE_BASENAME; then
    echo "➕ Archivos (por nombre) en $DIR2_NAME pero NO en $DIR1_NAME:"
else
    echo "➕ Archivos en $DIR2_NAME pero NO en $DIR1_NAME:"
fi
echo "------------------------------------------------------"
comm -13 "$DIR1_FILES" "$DIR2_FILES" | while read file; do
    echo "  + $file"
done
NEW=$(comm -13 "$DIR1_FILES" "$DIR2_FILES" | wc -l)
echo "Total: $NEW archivos"
echo ""

if $USE_BASENAME; then
    echo "✅ Nombres de archivos comunes:"
else
    echo "✅ Archivos comunes (misma ruta relativa):"
fi
echo "------------------------------------------------------"
COMMON=$(comm -12 "$DIR1_FILES" "$DIR2_FILES" | wc -l)
echo "Total: $COMMON archivos"
echo ""

# Limpieza
rm "$DIR1_FILES" "$DIR2_FILES"

echo "=========================================="
echo "RESUMEN:"
if $USE_BASENAME; then
    echo "  - Nombres solo en $DIR1_NAME: $MISSING"
    echo "  - Nombres solo en $DIR2_NAME: $NEW"
    echo "  - Nombres comunes: $COMMON"
else
    echo "  - Archivos solo en $DIR1_NAME: $MISSING"
    echo "  - Archivos solo en $DIR2_NAME: $NEW"
    echo "  - Archivos comunes: $COMMON"
fi
echo "=========================================="
echo ""
if [ $MISSING -gt 0 ]; then
    if $USE_BASENAME; then
        echo "⚠️  ATENCIÓN: Hay $MISSING nombre(s) de archivo en $DIR1_NAME que no están en $DIR2_NAME"
    else
        echo "⚠️  ATENCIÓN: Hay $MISSING archivo(s) en $DIR1_NAME que no están en $DIR2_NAME"
    fi
fi

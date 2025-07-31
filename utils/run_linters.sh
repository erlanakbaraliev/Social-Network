#!/bin/bash
TO_EXCLUDE=("__init__.py" "__pycache__")
IS_FAILURE=false


_run_pylint() {
    printf "%s\n" "Pylint check for $(basename "$dir")"
    pylint --output-format=colorized -j 0 "$dir"
}

_run_pycodestyle() {
    printf "%s\n" "Pycodestyle check for $(basename "$dir")"
    pycodestyle --max-line-length=120 --statistics --exclude=apps/core/migrations "$dir"
}

check_success() {
    return_code=$1
    if [[ "$IS_FAILURE" = false ]] && [[ ! "$return_code" = 0 ]]; then
        IS_FAILURE=true
        echo "Setting exit to 1"
    fi
}

for dir in $(pwd)/apps/*; do
    if [[ -d "$dir" ]] && [[ ! ${TO_EXCLUDE[*]} =~ $(basename "$dir") ]]; then
        _run_pycodestyle "$dir"
        check_success $?
        _run_pylint "$dir"
        check_success $?
    fi
done


[[ $IS_FAILURE == true ]] && exit 1 || exit 0
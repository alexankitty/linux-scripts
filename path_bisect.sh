#!/usr/bin/env bash
set -euo pipefail
shopt -s dotglob   # include hidden files in globs globally

trim() {
    printf '%s\n' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

BISECT_RESULT=""

#functions
bisect_path() {
    base_path=$(dirname "$1")
    folder=$(basename "$1")
    if [[ $folder == *"$delimiter"* ]]; then
        folder1="$(trim "${folder%%$delimiter*}")"
        folder2="$(trim "${folder##*$delimiter}")"
        new_path="$base_path/$folder1/$folder2"
        if [[ -n $debug ]]; then
            echo "folder: $folder" >&2
            echo "folder1: $folder1" >&2
            echo "folder2: $folder2" >&2
            echo "Bisecting path: $1" >&2
            echo "New path: $new_path" >&2
        fi
        if [[ -z $folder1 || -z $folder2 ]]; then
            echo "Warning: empty path component after bisect on '$folder', skipping" >&2
            BISECT_RESULT="$1"
            return
        fi
        mkdir -p "$(dirname "$new_path")"
        if [[ -d "$new_path" ]]; then
            echo "Merging: $new_path" >&2
            if [[ -n "$(ls -A "$1")" ]]; then
                mv "$1"/* "$new_path"
            fi
            rmdir "$1"
        else
            mv "$1" "$new_path"
        fi
        echo "moved: $1 -> $new_path" >&2
        BISECT_RESULT="$new_path"   # return new path
    else
        BISECT_RESULT="$1"          # return original, unchanged
    fi
}

dir_recurse() {
    local current="$1"
    bisect_path "$current"
    local new_path="$BISECT_RESULT"

    recurse_depth=$((recurse_depth + 1))
    if [[ $recurse_depth -le $depth || $depth -eq 0 ]]; then
        for item in "$new_path"/*; do
            [[ -e "$item" ]] || continue
            [[ -d "$item" ]] || continue
            dir_recurse "$item"
        done
    fi
    recurse_depth=$((recurse_depth - 1))
}

#init
paths=()
recurse_depth=0
debug=""
recursive=""
delimiter=""
depth=""

#args
while [[ $# -gt 0 ]]; do
    arg="$1"
    if [[ -z $arg ]]; then
        echo "Argument is empty"
        exit 1
    fi
    if [[ $arg == '-'* ]]; then
        case $arg in
            -r|--recursive)
                recursive=true
                shift
                ;;
            -d|--depth)
                if [[ -z "${2:-}" ]]; then
                    echo "--depth requires an argument"
                    exit 1
                fi
                depth=$2
                shift 2
                ;;
            -D|--delimiter)
                if [[ -z "${2:-}" ]]; then
                    echo "--delimiter requires an argument"
                    exit 1
                fi
                delimiter=$2
                shift 2
                ;;
            -h|--help)
                echo "Path bisect - Alexankitty"
                echo " -r/--recursive: Recursive search"
                echo " -d/--depth: Depth of recursive search (requires -r), default 1 set to 0 to recurse all levels"
                echo " -D/--delimiter: Delimiter to use for path bisection"
                echo " -h/--help: This help message"
                echo " -v/--verbose: Verbose output"
                printf "Usage: $0 [options] <path>\n"
                exit 0
                ;;
            -v|--verbose)
                debug=true
                shift
                ;;

            -*)
                echo "Unknown option: $arg"
                exit 1
                ;;
        esac
    else
        paths+=("$arg")
        shift
    fi
done
if [[ ${#paths[@]} -eq 0 ]]; then
    echo "No path specified"
    exit 1
fi
if [[ -z $delimiter ]]; then
    echo "No delimiter specified"
    exit 1
fi
if [[ -n $depth && ! $depth =~ ^[0-9]+$ ]]; then
    echo "Depth must be a non-negative integer"
    exit 1
fi

if [[ -z $depth ]]; then
    depth=1
fi

#debug
if [[ -n $debug ]]; then
    echo "Debug: $debug"
    if [[ $depth -eq 0 ]]; then
        echo "Depth: unlimited"
    else
        echo "Depth: $depth"
    fi
    echo "Recursive: $recursive"
    echo "Paths: ${paths[@]}"
    echo "Delimiter: $delimiter"
fi

for path in "${paths[@]}"; do
    if [[ -f "$path" ]]; then
      echo "Path $path is a file, skipping"
      continue
    fi
    if [[ $recursive ]]; then
        dir_recurse "$path"
    else
        bisect_path "$path"
    fi

done

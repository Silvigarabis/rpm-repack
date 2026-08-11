#!/bin/bash

set -eu -o pipefail

main(){
    work_config_default

    if ! parse_arg "$@"; then
        exit 2
    fi

    if [[ -v COMMAND_FUNC[$COMMAND] ]]; then
        work_config_setup
        "${COMMAND_FUNC[$COMMAND]}" "${OPTIONS[@]}"
    else
        "${INTERNAL_COMMAND_FUNC[$COMMAND]}" "${OPTIONS[@]}"
    fi
}

work_config_default(){
    SOURCES_DIR=sources
    SOURCE_GENERATORS_DIR=source-generators
    BUILD_DIR=makerpmpkg-build

    PROJECT_ROOT=
    PATH_PROJECT_SOURCES=
    PATH_PROJECT_SOURCE_GENERATORS=
    PATH_BUILD_DIR=
    SPEC_FILE=
    SPEC_FILE_SOURCE_NAME_LIST=()
    GENERATED_SRPM_PATH=
}

work_config_setup(){
    local spec_file_name
    spec_file_name="$(basename "$SPEC_FILE")"

    export PROJECT_ROOT="$(realpath -- "$(dirname -- "$SPEC_FILE")")"
    if [[ -z $BUILD_ROOT ]]; then
        BUILD_ROOT="$PWD"
    fi
    export BUILD_ROOT="$(realpath -- "$BUILD_ROOT")"

    export PATH_PROJECT_SOURCES="${PROJECT_ROOT}/${SOURCES_DIR}"
    export PATH_PROJECT_SOURCE_GENERATORS="${PROJECT_ROOT}/${SOURCE_GENERATORS_DIR}"

    export PATH_BUILD_DIR="${BUILD_ROOT}/${BUILD_DIR}"
    export PATH_RPMBUILD="$PATH_BUILD_DIR/rpmbuild"

    export PATH_RPMBUILD_RPMDIR="$(rpm_wrapper rpm --eval "%{_rpmdir}")"
    export PATH_RPMBUILD_SOURCEDIR="$(rpm_wrapper rpm --eval "%{_sourcedir}")"
    export PATH_RPMBUILD_SPECDIR="$(rpm_wrapper rpm --eval "%{_specdir}")"
    export PATH_RPMBUILD_SRCRPMDIR="$(rpm_wrapper rpm --eval "%{_srcrpmdir}")"
    export PATH_RPMBUILD_BUILDDIR="$(rpm_wrapper rpm --eval "%{_builddir}")"

    mkdir -p "$PATH_RPMBUILD" "$PATH_RPMBUILD_RPMDIR" "$PATH_RPMBUILD_SOURCEDIR" "$PATH_RPMBUILD_SPECDIR" "$PATH_RPMBUILD_SRCRPMDIR" "$PATH_RPMBUILD_BUILDDIR"

    export PATH_SOURCE_FILE_DEST_DIR="$PATH_RPMBUILD_SOURCEDIR"

    export PATH_SPEC_FILE="${PATH_RPMBUILD_SPECDIR}/${spec_file_name}"

    export PATH_SPEC_FILE_DMP="$PATH_BUILD_DIR/specfile.dmp"

    cp --update=all "$SPEC_FILE" "$PATH_SPEC_FILE"
    rpm_wrapper rpmspec -P "$PATH_SPEC_FILE" >"$PATH_SPEC_FILE_DMP"
}

rpm_wrapper(){
    "$1" --define "_topdir $PATH_RPMBUILD" "${@:2}"
}

script_config_default(){
    SCRIPT_NAME="makerpmpkg"

    GETOPT_OPT_LIST=(
        h   # help
        f:  # spec
        o:  # opt
    )

    GETOPT_LONG_OPT_LIST=(
        help
        spec-file:
        build-root:
        opt:
    )

    # shellcheck disable=SC2116
    GETOPT_OPT_STR=$(IFS="" echo "${GETOPT_OPT_LIST[*]}")
    # shellcheck disable=SC2116
    GETOPT_LONG_OPT_STR=$(IFS="," echo "${GETOPT_LONG_OPT_LIST[*]}")

    declare -gA COMMAND_FUNC=(
        ["inspect-source-list"]="inspect_rpmspec_source_name_list"
        ["generate-sources-dir"]="generate_sources_dir"
        ["srpm"]="generate_srpm"
        ["srpm-outpath"]="generate_srpm_outpath"
        ["rpmbuild"]="generate_srpm_and_build"
        ["mockbuild"]="generate_srpm_and_mockbuild"
    )

    declare -gA ACCEPT_REMAIN_ARGUMENT_FUNC=(
        [mockbuild]=y
    )

    declare -gA INTERNAL_COMMAND_FUNC=(
        ["help"]="script_help"
    )

    declare -g COMMAND=""
    declare -ga OPTIONS=()

    declare -gA SCRIPT_OPTS=(
        [srpm-use-cache]=y
        [override-dest-sources]=y
    )
}

script_update_opt(){
    local pair="$1"
    local key="${pair%%=*}" val="${pair#*=}"
    SCRIPT_OPTS["$key"]="$val"
}

parse_arg(){
    # ===== phase 0: init env =====

    declare show_help=n  # y / n
    declare spec_file=
    declare build_root=
    declare command=
    declare script_help_call=()
    declare options=()

    # ===== phase 1: getopt =====

    # 解析命令参数，在出错时退出
    if ARGS="$(getopt -o "$GETOPT_OPT_STR" -l "$GETOPT_LONG_OPT_STR" -n "$SCRIPT_NAME" -- "$@")"; then
        eval set -- "$ARGS"
    else
        script_help invalid_arguments
        return 2
    fi

    # 处理关联参数
    while (($# > 0)); do
        case "$1" in
            -h | --help ) show_help=y;; 
            -f | --spec-file ) shift; spec_file="$1";;
            --build-root ) shift; build_root="$1";;
            -o | --opt ) shift; script_update_opt "$1";;

            -- ) shift; break;;
        esac
        shift
    done

    # ===== phase 2: positional parsing =====

    # 将第一个参数作为命令
    if [[ -v 1 ]]; then
        command="$1"
        shift
    fi

    # 如果未使用关联参数定义文件，将第二个参数作为SPEC文件
    if [[ -z ${spec_file} && -v 1 ]]; then
        spec_file="$1"
        shift
    fi

    # 检查是否存在多余参数
    if [[ $# -gt 0 ]]; then
        if [[ -v ACCEPT_REMAIN_ARGUMENT_FUNC[$command] ]]; then
            options+=("$@")
        else
            script_help_call=( invalid_toomanyarguments )
        fi
    fi

    # ===== phase 3: validation =====

    # 检查是否要求展示帮助消息
    ## 使用此参数时会屏蔽其他错误，是有意为之
    if [[ ${show_help} = y ]]; then
        script_help_call=( normal )

    else {

        # 检查 SPEC 文件是否存在
        if [[ -z "${spec_file}" ]]; then
            script_help_call=( invalid_nospecfile )
        fi

        # 检查命令是否存在
        if [[ -z $command ]]; then
            # 未指定任何命令
            script_help_call=( invalid_nocommand )
        elif [[ ! -v COMMAND_FUNC[$command] ]]; then
            # 指定的命令不正确
            script_help_call=( invalid_command "$command" )
        fi

        # 检查指定的构建目录是否是普通目录
        if [[ -n ${build_root} && ! -d "${build_root}" ]]; then
            if [[ -e "${build_root}" ]]; then
                log_err "BUILDROOT cannot use '${build_root}': Not a directory"
                script_help_call=( invalid_not_a_directory "${build_root}")
            fi
        fi

    }
    fi

    # ===== phase 4: resolution =====

    if [[ ${#script_help_call[@]} -gt 0 ]]; then
        COMMAND=help
        OPTIONS=("${script_help_call[@]}")
    else
        SPEC_FILE="${spec_file}"
        BUILD_ROOT="${build_root}"
        COMMAND="$command"
        OPTIONS=("${options[@]}")
    fi
}

log(){
   printf '%s: %s\n' "$SCRIPT_NAME" "$*"
}

log_err(){
   log "$@" >&2
}

get_SPEC_FILE_SOURCE_NAME_LIST(){
    local spec_file="$PATH_SPEC_FILE" source_name source_name_list

    mapfile -td$'\n' source_name_list < <(
        {
            if command -v spectool &>/dev/null; then
                rpm_wrapper spectool --list-files --all "$spec_file"
            else
                rpm_wrapper rpmspec -P "$spec_file"
            fi
        } | awk -F': ' \
                '/^(Source|Patch)[0-9]*:/ {
                    sub(/^[ \t]+/, "", $2)
                    sub(/[ \t]+$/, "", $2)
                    print $2
            }'
        )

    for source_name in "${source_name_list[@]}"; do
        SPEC_FILE_SOURCE_NAME_LIST+=("$(basename -- "$source_name")")
    done
}

inspect_rpmspec_source_name_list(){
    get_SPEC_FILE_SOURCE_NAME_LIST
    printf '%s\n' "${SPEC_FILE_SOURCE_NAME_LIST[@]}"
}

generate_srpm_and_mockbuild(){
    generate_srpm
    if [[ -z ${GENERATED_SRPM_PATH:-} || ! -f ${GENERATED_SRPM_PATH:-} ]]; then
        log_err "cannot find srpm ${GENERATED_SRPM_NAME:-} at ${GENERATED_SRPM_PATH:-}" 
        return 1
    fi

    local comm=(mock rebuild "${GENERATED_SRPM_PATH}" "$@")

    log "[EXEC] ${comm[*]}"
    "${comm[@]}"

    log "[BUILD] mock done."
}

generate_srpm_and_build(){
    log "building $SPEC_FILE"

    generate_srpm

    if [[ -z ${GENERATED_SRPM_PATH:-} || ! -f ${GENERATED_SRPM_PATH:-} ]]; then
        log_err "cannot find srpm ${GENERATED_SRPM_NAME:-} at ${GENERATED_SRPM_PATH:-}" 
        return 1
    fi

    local comm=(rpm_wrapper rpmbuild --rebuild "${GENERATED_SRPM_PATH}")

    log "[RUN] ${comm[*]}"
    (
        set -x
        "${comm[@]}"
    )

    log "[BUILD] done. result rpms may found under $PATH_RPMBUILD_RPMDIR"
}

generate_srpm_outpath(){
    generate_srpm
    local outpath_fd="${SCRIPT_OPTS[srpm-outpath-fd]:-}"
    if [[ -n ${outpath_fd} ]]; then
        printf '%s\n' "$GENERATED_SRPM_PATH" >&${outpath_fd}
    else
        log_err "[SRPM OUTPATH] required srpm-outpath-fd opt not found"
        return 2
    fi
}

generate_srpm(){
    log "generating srpm"

    local srpm_name srpm_path
    srpm_name=$(rpm_wrapper rpmspec --srpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.src.rpm' "$PATH_SPEC_FILE")
    srpm_path="$PATH_RPMBUILD_SRCRPMDIR/${srpm_name}"

    if [[ ${SCRIPT_OPTS[srpm-use-cache]} = y && -f ${srpm_path} ]]; then
        log "[SRPM] CACHE USED."
    else
        generate_sources_dir
        log "start building srpm"
        rpm_wrapper rpmbuild -bs "$PATH_SPEC_FILE"
        log "[SRPM] done."
    fi

    GENERATED_SRPM_NAME="${srpm_name}"
    GENERATED_SRPM_PATH="$PATH_RPMBUILD_SRCRPMDIR/${srpm_name}"
}

generate_sources_dir(){
    get_SPEC_FILE_SOURCE_NAME_LIST
    local source_name dest_file

    local source_file_dest_dir="$PATH_SOURCE_FILE_DEST_DIR"
    mkdir -p "${source_file_dest_dir}" 

    log "[SOURCES]: dest dir: ${source_file_dest_dir}"

    for source_name in "${SPEC_FILE_SOURCE_NAME_LIST[@]}"; do
        dest_file="${source_file_dest_dir}/${source_name}"

        if [[ -e "${dest_file}" ]]; then
            if [[ ${SCRIPT_OPTS[override-dest-sources]} = y ]]; then
                rm -f "${dest_file}"
            else
                log "[SKIP EXISTS] ${source_name}"
                continue
            fi
        fi

        resolve_source "${source_name}" "${dest_file}"
    done

    log "[SOURCES]: generate completed"
}

resolve_source(){
    local source_name="$1"
    local dest_file="$2"

    local maybe_file="$PATH_PROJECT_SOURCES/${source_name}"
    local maybe_generator_dir="$PATH_PROJECT_SOURCE_GENERATORS/${source_name}"
    local maybe_generator_exec="${maybe_generator_dir}/generator"

    if [[ -f ${maybe_file} ]]; then
        log "[COPY] ${maybe_file} -> ${dest_file}"
        cp --update=none-fail --reflink=auto "$maybe_file" "$dest_file"
        log "[RESOLVED] ${source_name}"
        return
    fi

    if [[ -x ${maybe_generator_exec} && -f ${maybe_generator_exec} ]]; then
        log "[GEN] ${source_name} -> ${dest_file}"
        if (
            export GENERATE_SOURCE_NAME="${source_name}"
            export GENERATE_DEST_FILE="${dest_file}"
            export GENERATOR_DIR="${maybe_generator_dir}"
            export GENERATOR_WORKING_DIR="$PATH_BUILD_DIR/source-generators/${source_name}"

            generator_exec="$(realpath -- "$maybe_generator_exec")"

            set -x
            mkdir -p "$GENERATOR_WORKING_DIR"
            cd "$GENERATOR_WORKING_DIR"
            "${generator_exec}"
        ); then
            true
        else
            local generator_errcode=$?
            if [[ $generator_errcode -ne 0 ]]; then
                log_err "resolve_source ${source_name}: generator exited with code ${generator_errcode}"
                return 1
            fi
        fi


        if [[ -f ${dest_file} ]]; then
            log "[RESOLVED] ${source_name}"
            return 0
        else
            log_err "resolve_source ${source_name}: dest file '${dest_file}' not found after generator exited"
            return 1
        fi
    fi

    log_err "missing source: ${source_name}"
    return 1
}

script_help(){
    local reason="${1:-normal}"
    case "${reason}" in
        invalid_*) 
            case "${reason}" in
                invalid_command) log_err "invalid command" "'${2:-}'";;
                invalid_nocommand) log_err "no command specified.";;

                invalid_nospecfile) log_err "no SPEC file specified";;
                invalid_toomanyarguments) log_err "too many arguments";;

                invalid_arguments);;  # getopt will print invalid arguemnts
            esac

            log_err "use '${BASH_SOURCE[0]} --help' to get help."
            return 2
            ;;
    esac

    cat <<EOM
$SCRIPT_NAME: a rpm build helper script

Usage: $0

[COMMANDS]:
    inspect-source-list
    generate-sources-dir
    srpm
    rpmbuild

[OPTIONS]:
   -h, --help  display this help message
EOM
}

script_config_default
if [[ ${BASH_SOURCE[0]} = "$0" ]]; then
   main "$@"
else
   log_err "cannot run as source script"
   exit 2
fi

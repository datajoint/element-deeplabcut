#!/bin/bash
# For Github Action that doesn't support anchor yet...
# https://github.com/actions/runner/issues/1182
# yq is not the version from pypi with the same name.

export STAGE=${1:-prod}
# .yaml in .staging_workflows has to be named using a prefix, e.g., 'anchored_', this will be removed when normalizing
PREFIX=${2:-anchored_}
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

run_yq() {
	local src_file
	local filename
	local target
	for src_file in "${SCRIPT_DIR}"/*.y*ml; do
		[[ ! -f ${src_file} ]] && continue
		filename=$(basename "$src_file")
		target="${SCRIPT_DIR}"/../workflows/${filename#"$PREFIX"}
		envsubst '${STAGE}' <"$src_file" | yq e 'explode(.) | del(.anchor-*)' >"$target"
	done
}

run_yq
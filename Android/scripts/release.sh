#!/bin/bash

SCRIPT_DIR=$(dirname "$0")

DIR=$(
  cd "$SCRIPT_DIR" || exit
  pwd -P
) # Equals "path/to/this/directory"

PROJECT_ROOT="${DIR}/.."

# shellcheck disable=SC2002
sample_version_code=$(cat "${PROJECT_ROOT}"/sample/build.gradle | grep " versionCode " | sed -E "s/^.*versionCode //")
# shellcheck disable=SC2002
sdk_version_name=$(cat "${PROJECT_ROOT}"/version.gradle | grep "versionName" | sed "s/.*versionName.*\"\(.*\).*\".*/\1/")

echo "Sample version code: ${sample_version_code}"
echo "SDK version name: ${sdk_version_name}"

path_output="$PROJECT_ROOT/release/msdk_${sample_version_code}_${sdk_version_name}"
filename_code_zip="msdk_${sample_version_code}_${sdk_version_name}_source_code.zip"
apk_name="msdk_demo_${sample_version_code}_${sdk_version_name}-release.apk"
git_current_branch=$(git rev-parse --abbrev-ref HEAD)

echo "Current branch: ${git_current_branch}"
echo "Script path: $DIR"
echo "Project root path: $PROJECT_ROOT"

function setup() {
  if [[ -d "$path_output" ]]; then
    rm -rf "$path_output"
  fi
  mkdir -p "$path_output"
}

function compress_code() {
  echo "Compressing codes..."
  path="${path_output}/${filename_code_zip}"
  # shellcheck disable=SC2091
  $(cd "$PROJECT_ROOT" && git archive --format zip --output "${path}" "$git_current_branch")
  echo "Please find codes here: ${path}"
}

function generate_apk() {
  echo "Generate APK..."

  GRADLEW="${PROJECT_ROOT}/gradlew"

  if ("$GRADLEW" -p "$PROJECT_ROOT" clean); then
    echo "Assemble release..."
    if ("$GRADLEW" -p "$PROJECT_ROOT" assembleRelease); then
      cp "${PROJECT_ROOT}/sample/build/outputs/apk/release/${apk_name}" "${path_output}"
    else
      exit 1
    fi
  else
    exit 1
  fi
}

function release() {
  cd "$path_output" || exit
  release_file_name="MSDK-Android-${sdk_version_name}.zip"
  zip -r "$release_file_name" .

  source_codes_path="${path_output}/${filename_code_zip}"
  rm -rf "$source_codes_path"
  apk_path="${path_output}/${apk_name}"
  rm -rf "${apk_path}"

  cd - || exit
}

setup
compress_code
generate_apk
release

tput setaf 2
echo "Please find files here: ""${path_output}"

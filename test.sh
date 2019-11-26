function process() {
  echo "=============================================================================="
  echo "==================Testing $1====================="
  if ! python3 main.py $1; then
    >&2 echo "Error on file $1"
  fi
}

echo "======Running tests======="
for i in $(find ./test -name '*.ot')
do
  process $i
done
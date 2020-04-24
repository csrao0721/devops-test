# Use `sam build` to get dependencies
sam build -b ./build --use-container -m ./requirements.txt

# Move dependencies into our layer directory
mv ./build/ServiceApiFunction/PIL ./src/
mv ./build/ServiceApiFunction/Pillow* ./src/

# Remove the build directory and its contents
rm -rf ./build
SET full_image_name=gcr.io/test-vms/tarsan/trainmodel:%images_tag%

echo IMAGE TO BUILD: %full_image_name%

docker build -t %full_image_name% .
docker push %full_image_name%

sed -e "s|__IMAGE_NAME__|%full_image_name%|g" component_template.yaml > component.yaml
type component.yaml 

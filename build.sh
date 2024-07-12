# Comando para criar imagem rpcavaco/postgis:12-3.0

podman build -t rpcavaco/mapml_panel -f ./Dockerfile
## Se não existir a referencia no namespace docker.io/library a esta imagem
## executar:
# podman tag rpcavaco/postgis:latest docker.io/library/rpc-postgis-latest


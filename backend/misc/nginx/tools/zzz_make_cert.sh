./create_self_signed_cert.sh "/C=CN/ST=Guangdong/L=Shenzhen/O=xdevops/OU=xdevops/CN=server.facemagi.com"
chmod 644 server.key

mkdir -p ../cert ../log
mv server.* ../cert


yum groupinstall "Development Tools" -y

yum install pcre-devel pcre openssl-devel openssl -y

git clone git://github.com/arut/nginx-rtmp-module.git

wget http://nginx.org/download/nginx-1.19.8.tar.gz
tar xzf nginx-1.19.8.tar.gz
cd nginx-1.19.8

./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
make
make install

ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx
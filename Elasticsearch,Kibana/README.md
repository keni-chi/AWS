# Elasticsearch

## 概要
以下、やってみたこと。
logstashかfluentdでどちらかまたは両方で構築して動作させたが、忘れた。

- Elasticsearch

- EC2上でpythonで実行し、Elasticsearchへデータ保存

- logstashを用いたTwitterデータの収集

- Kibanaで見える化

- fluentd

- 以下はlogstashメモ。

■EC2準備
・ec2-userでリモートログイン
ssh -i mykey.pem ec2-user@[Public IP]

・rootユーザに昇格
[ec2-user@ip-***-***-***-*** ~]$ sudo su -

・パスワード変更
[ec2-user@ip-***-***-***-*** ~]$ passwd
Changing password for user root.
New password: （パスワード入力）
[root@ip-***-***-***-*** ~]#

■以下具体的な流れメモ
sudo su
yum update -y
yum -y install java-1.8.0-openjdk-devel
sudo su -
alternatives --config java
java -version
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
ls /etc/yum.repos.d/

cat << _FIN_ > /etc/yum.repos.d/logstash.repo
[logstash-5.x]
name=Elastic repository for 5.x packages
baseurl=https://artifacts.elastic.co/packages/5.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
_FIN_

[logstash-6.x]
name=Elastic repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md

cat /etc/yum.repos.d/logstash.repo
yum install logstash -y
/usr/share/logstash/bin/logstash --version
/usr/share/logstash/bin/logstash-plugin install logstash-output-amazon_es

■ES構築
mkdir logstas
vi logstash.yml
vi  /etc/logstas/logstash.yml

TWI_KEY={xxxxx}
TWI_KYE_SEC={xxxxx}
TWI_TOKEN={xxxxx}
TWI_TOKEN_SEC={xxxxx}
ES_EDP=https://search-movies-{xxxxx}.ap-northeast-1.es.amazonaws.com
ES_REG=es:ap-northeast-1


書き込み権限のないユーザでファイルを編集してしまったとき 
参考: http://jsapachehtml.hatenablog.com/entry/2014/11/23/124350
:w !sudo tee %


cat << _FIN_ > /etc/logstash/conf.d/twitter.conf
input {
  twitter {
    consumer_key => "{xxxxx}"
    consumer_secret => "{xxxxx}"
    oauth_token => "{xxxxx}"
    oauth_token_secret => "{xxxxx}"
    keywords => ["aws"]
    full_tweet => true
  }
}
output {
    amazon_es {
        hosts => ["search-twitter-{xxxxx}.ap-northeast-1.es.amazonaws.com"]
        region => "ap-northeast-1"
        aws_access_key_id => '{xxxxx}'
        aws_secret_access_key => '{xxxxx}'
        index => "twitter"
        document_type => "stream"
    }
    stdout { }
}
_FIN_

cat /etc/logstash/conf.d/twitter.conf

/usr/share/logstash/bin/logstash --path.settings /etc/logstash -f /etc/logstash/conf.d/twitter.conf

■ブラウザでkibana起動
Index patternを  .kibana に設定
Time Filter field name は　　url.createDate　に設定

■ES構築、セキュリティグループでVPC内ならＯＫの設定後、以下で確認
dig +short arn:aws:es:ap-northeast-1:{account_id}:domain/practice01

curl -XPUT https://search-movies-{xxxxx}.ap-northeast-1.es.amazonaws.com/movies/movie/1 -d '{"director": "Burton, Tim", "genre": ["Comedy","Sci-Fi"], "year": 1996, "actor": ["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"], "title": "Mars Attacks!"}' -H 'Content-Type: application/json'
curl -XGET 'https://search-movies-{xxxxx}.ap-northeast-1.es.amazonaws.com/movies/_search?q=mars'

■アクセスポリシー
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "es:*",
      "Resource": "arn:aws:es:ap-northeast-1:{account_id}:domain/movies/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "{ip}"
        }
      }
    }
  ]
}

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "*"
        ]
      },
      "Action": [
        "es:*"
      ],
      "Resource": "arn:aws:es:ap-northeast-1:{acount_id}:domain/movies/*"
    }
  ]
}


- 以下はfluentdメモ。

■参考
http://blog.serverworks.co.jp/tech/2015/10/15/play-with-fluentd/
https://qiita.com/Dalice/items/28a55c5f82481aebe04f
http://www.k-staging.com/?p=1427
https://qiita.com/Salinger/items/9d47ced748ff7191570a

■構築メモ
sudo yum install httpd -y
curl -L https://td-toolbelt.herokuapp.com/sh/install-redhat-td-agent2.sh | sh
sudo chkconfig td-agent on
sudo mkdir -p /etc/td-agent/conf.d
sudo td-agent-gem install fluent-plugin-record-reformer
sudo td-agent-gem list --local |grep fluent-plugin
apachectl -v
cd tmp
mkdir fluent
cd fluent
mkdir logpos

sudo /etc/init.d/td-agent start
sudo /etc/init.d/td-agent status

sudo td-agent-gem install fluent-plugin-twitter　　#失敗
sudo /usr/sbin/td-agent-gem install fluent-plugin-s3　　#失敗

sudo yum -y install openssl-devel libcurl libcurl-devel gcc-c++
sudo td-agent-gem install eventmachine
sudo td-agent-gem install fluent-plugin-twitter

sudo vi /etc/td-agent/td-agent.conf

<source>
  type twitter
  consumer_key {xxxxx}
  consumer_secret {xxxxx}
  oauth_token {xxxxx}
  oauth_token_secret {xxxxx}
  tag input.twitter.sampling
  timeline sampling
  lang ja
  output_format nest
</source>

<match input.twitter.sampling>
  type copy

  <store>
    type s3
    aws_key_id {xxxxx}
    aws_sec_key {xxxxx}
    s3_bucket {bucketName}
    s3_region ap-northeast-1
    s3_enpoint s3-ap-northeast-1.amazonaws.com
    path streaming_api_logs/
    buffer_path /var/log/td-agent/s3
    time_slice_format %Y%m%d%H
    s3_object_key_format %{path}%{time_slice}_%{index}_%{hostname}.%{file_extension}
    time_slice_wait 5m
    buffer_chunk_limit 256M

    utc
  </store>
</match>

sudo /etc/init.d/td-agent start
sudo /etc/init.d/td-agent stop
tail /var/log/td-agent/td-agent.log

■試行錯誤？メモ
<source>
  type tail
  format apache2
  path /var/log/httpd/access_log
  tag test.apache.access
  pos_file /tmp/fluent/logpos/access_log.pos
  types code:integer,size:integer
</source>

<match **>
  type forward

  <server>
    name fluent01
    host 172.31.6.241
    port 24224
  </server>
</match>


<source>
  type forward
  port 24224
  bind 0.0.0.0
</source>

<match test.apache.*>
  type copy

  <store>
    type s3
    aws_key_id {xxx}
    aws_sec_key {xxx}
    s3_bucket {bucketName}
    s3_region ap-northeast-1
    s3_object_key_format %{path}%{time_slice}/%{index}.%{hostname}.%{file_extension}
    path access-logs/
    buffer_path /tmp/fluent/s3
    time_slice_format %Y%m%d-%H
    time_slice_wait 10m
    utc
    format json
    include_time_key true
  </store>
</match>


■しばらくしてから
sudo yum install httpd -y
curl -L https://td-toolbelt.herokuapp.com/sh/install-redhat-td-agent2.sh | sh
sudo chkconfig td-agent on
sudo mkdir -p /etc/td-agent/conf.d
sudo td-agent-gem install fluent-plugin-record-reformer
sudo td-agent-gem list --local |grep fluent-plugin
apachectl -v

sudo yum -y install openssl-devel libcurl libcurl-devel gcc-c++
sudo td-agent-gem install eventmachine
sudo td-agent-gem install fluent-plugin-twitter
sudo /usr/sbin/td-agent-gem install fluent-plugin-s3

cd /tmp
mkdir fluent
cd fluent
mkdir logpos

sudo vi /etc/td-agent/td-agent.conf

■設定は別ファイル参照
セキュリティグループでinboundの24224を開けておく(TCP,UDP両方)
sudo /etc/init.d/td-agent start
sudo /etc/init.d/td-agent status
sudo /etc/init.d/td-agent stop
sudo /etc/init.d/td-agent restart

tail /var/log/td-agent/td-agent.log

ここまででS3保存完了

■その他メモ
グローバルIP調査
curl inet-ip.info
sudo td-agent-gem install fluent-plugin-elasticsearch

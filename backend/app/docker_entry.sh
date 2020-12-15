echo '生产版本 docker 内开始执行……'

echo '启动工作引擎……'
/app/run_engine.sh 2>&1 &

sleep 20

echo '启动 API 服务……'
/app/run_web.sh 2>&1 &

while [ 1 ]
do
  echo 'web running ...'
  sleep 30
done


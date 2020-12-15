USE_SCRIPT=./demo_single_path.sh
#USE_SCRIPT=./demo_dual_path.sh
bash $USE_SCRIPT

sed 's/^\.\/data\/demo\///g' result/demo_result.list | sed 's/ 1/  1/g' | sed 's/ 0/ -1/g' > result/demo_result_final.list

echo ''
echo '面部特征判断结果已输出到文件：result/demo_result_final.list'
echo '请将相应的行手工导入目标文件：../../../Anno/list_attr_celeba.txt'

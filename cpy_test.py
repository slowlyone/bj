import  os
import multiprocessing

#from multiprocessing import Pool

def copy_file(old_folder_name,new_folder_name,file_name,queue):
	'''完成文件复制 '''
	#print('%s--'%file_name )
	#print("==>模拟copy文件:从%s-->%s 文件名是%s"%(old_folder_name,new_folder_name,file_name))
	
	old_f=open(old_folder_name+'/'+file_name,'rb')
	
	content=old_f.read()	

	#print(content)
	old_f.close()

	new_f=open(new_folder_name+'/'+file_name,'wb')
	new_f.write(content)	
	new_f.close()
	
	#拷贝完一个文件就，写入Queue
	queue.put(file_name)
	
def  main():
	#1、获取用户要copy对文件夹名字
	old_folder_name = input('copy文件夹名字')
	
	#2、创建一个文件夹
	try:
		new_folder_name= old_folder_name + '[附件]'
		os.mkdir(new_folder_name )
	
	except:
		
		pass

	#4、获取文件夹 对所有待copy 对文件名字 listdir(), 如果有成千上万个文件
	# for 循环将上万次， 所以 使用进程池， 将任务放到进程池中
	
	#定义queue,传入进程池里
	queue = multiprocessing.Manager().Queue()
	
	
	file_names = os.listdir(old_folder_name)   #字符串列表
	#print(file_names)

	#4复制原文件夹中对文件， 到新的文件夹中对文件
	
	#创建进程池
	po = multiprocessing.Pool(5)	
	#向进程池中添加，copy 文件对任务
	for  file_name in file_names:
		po.apply_async(copy_file, args=(old_folder_name ,new_folder_name ,file_name,queue))
	
	po.close()
	#po.join()	
	#设置进度条，子进程一个ok，就+1;使用进程间通信Queue, Manager().Queue()
	all_file_num = len(file_names)
	copy_ok_num =0
	while True:
		
		file_name = queue.get()
		
		copy_ok_num +=1
		
		#print('拷贝进度为:%.2f %%'%(copy_ok_num*100/all_file_num))
		print('\r拷贝进度为:%.2f %%' %(copy_ok_num *100/all_file_num),end="")
	
	
		if copy_ok_num >= all_file_num:
			break
	print()


if __name__ =="__main__":
	main()

import re
import os

for file in os.listdir(os.getcwd()):
	if file.endswith( ".plt" ):
		#First trim off shit at top and last bracket
		lines = open( file ).readlines()
		open( file, 'w' ).writelines( lines[26:-1])
		
		#Then reformat actual data 
		dataList = []
		hwFile = open( file )

		for element in hwFile:
			dataList.append( element )

		for i in range( 0, len( dataList ) ):
			dataList[i] = dataList[i].strip('\t')
			dataList[i] = dataList[i].lstrip()
			dataList[i] = re.sub(r'\n', ' ', dataList[i] )
			dataList[i] = re.sub(r'   ', ' ', dataList[i] )
			dataList[i] = re.sub(r'  ', ' ', dataList[i] )
			
		newFile = open( file + '_e.plt', 'w')
		counter = 1

		for i in range( 0, len( dataList ) ):
			newFile.write( dataList[i] ) 
			if ( (counter % 8 == 0) ):
				newFile.write('\n')
			counter += 1

	

	
	
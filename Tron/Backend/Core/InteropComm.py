import array

class InteropComm(object):
	"""
	Implements Communication methods and functions for 
	the Interoperability tests
	"""

	def matrix_split(self, matrix: list, max_size: tuple) -> dict:
		"""
		Split the given matrix into the parts, 
		which have maximum size max_size
			Args:
			Returns:
			Raises:
		"""
		# check if the matrix just consist of int 
		# if not all(isinstance(item, int) for item in list):
		# 	raise TypeError

		if  (type(max_size[0]) != int) | (type(max_size[1]) != int):
			raise TypeError
		else:
			if (max_size[0] > len(matrix)) | (max_size[1] > len(matrix[0])):
				raise ValueError

		matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #initialize Array for splitted matrices
		dictionary = {(0,0):matrixArray}
		matrixRowCount            = len(matrix)
		matrixColumnCount         = len(matrix[0])
		#calculate new, splitted matrix dimensions
		splittedMatrixRowCount    = matrixRowCount // max_size[0] # how much Rows has the matrix, that consist of splitted parts
		splittedMatrixColumnCount = matrixColumnCount // max_size[1] # how much Columns has the matrix, that consist of splitted parts

		#check if one extra iteration for "smaller" child matrices needed
		if (matrixRowCount - splittedMatrixRowCount * max_size[0]) > 0: splittedMatrixRowCount += 1
		if (matrixColumnCount - splittedMatrixColumnCount * max_size[1]) > 0: splittedMatrixColumnCount += 1

		currentRow                = 0 # Row Counter for the loop
		currentColumn             = 0 # Cloumn Counter for the loop

		currentSplittedMatrixRow = 0
		currentSplittedMatrixColumn = 0

		
		for currentSplittedMatrixRow in range (0, splittedMatrixRowCount):
			for currentSplittedMatrixColumn in range (0, splittedMatrixColumnCount):
				# process each "Child" of the Mother matrix
				matrixArray = self.processChildMatrix(currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount)
				newDictElement = {(currentSplittedMatrixRow,currentSplittedMatrixColumn) : matrixArray}
				dictionary.update(newDictElement)
				#matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #reset Array for splitted matrices

		
		return dictionary

	def processChildMatrixOld (self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount):
		"""
		wright down all the Elements of the "Child" Matrix
		"""
		 

		#calculate Row und Column Size for the Child matrix
		childMatrixRowCount = matrixRowCount - (currentSplittedMatrixRow + 1) * max_size[0] + 1
		childMatrixColumnCount = matrixColumnCount - (currentSplittedMatrixColumn + 1) * max_size[1] + 1

		#initialize child matrix 
		matrixArray = [[0 for x in range(childMatrixColumnCount)] for y in range(childMatrixRowCount)]

		# right down all the arguments to the child matrix array
		#iterate on rows
		for currentRow in range (currentSplittedMatrixRow * max_size[0] , (currentSplittedMatrixRow+1) * max_size[0]):
			
			#calculate current row of child matrix
			currentChildRow = currentRow - max_size[0]*currentSplittedMatrixRow

			#check if current child row not out of range
			if currentChildRow >= childMatrixRowCount:
				break
			


			# iterate on columns
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], (currentSplittedMatrixColumn + 1) * max_size[1]):

				#calculate current column of child matrix
				currentChildColumn = currentColumn - max_size[0]*currentSplittedMatrixColumn

				#check if current child column not out of range
				if currentChildColumn >= childMatrixColumnCount:
					break


				#right down mother element into child matrix
				matrixArray[currentChildRow][currentChildColumn] = matrix[currentRow][currentColumn]

					
		return matrixArray


	def processChildMatrix(self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount):
		"""
		wright down all the Elements of the "Child" Matrix
		"""

		childMatrix: list
		
		childSize = self.getChildSize (matrixRowCount, matrixColumnCount, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size)

		childMatrix = [[0 for x in range( childSize[1] )] for y in range( childSize[0] )]

		# right down all the arguments to the child matrix array
		#iterate on rows
		

		for currentRow in range (currentSplittedMatrixRow * max_size[0] , currentSplittedMatrixRow * max_size[0] + childSize[0] ):
			
			#calculate current row of child matrix
			currentChildRow = currentRow - max_size[0] * currentSplittedMatrixRow

			#check if current child row not out of range
			if currentChildRow >= childSize[0]:
				break

			# iterate on columns
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], currentSplittedMatrixColumn * max_size[1] + childSize[1] ):

				#calculate current column of child matrix
				currentChildColumn = currentColumn - max_size[1]*currentSplittedMatrixColumn

				#check if current child column not out of range
				if currentChildColumn >= childSize[1]:
					break

				#right down mother element into child matrix
				childMatrix[currentChildRow][currentChildColumn] = matrix[currentRow][currentColumn]

		return childMatrix

 
	def getChildSize (self, matrixRowCount, matrixColumnCount, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size):
		"""
		calculates the size of the Child matrix in the current position of the Mother matrix
			Returns: childSize tuple
		"""
		#row
		rowDifference = (currentSplittedMatrixRow + 1) * max_size[0] - matrixRowCount

		if rowDifference > 0:
			childSizeRow = max_size[0] - rowDifference
		else: 
			childSizeRow = max_size[0]

		#column
		columnDifference = (currentSplittedMatrixColumn + 1 ) * max_size[1] - matrixRowCount

		if columnDifference > 0:
			childSizeColumn = max_size[1] - columnDifference
		else:
			childSizeColumn = max_size[1]


		# childSizeRow = matrixRowCount - (currentSplittedMatrixRow + 1) * max_size[0] + 1
		# childSizeColumn = matrixColumnCount - (currentSplittedMatrixColumn + 1) * max_size[1] + 1

		childSize = (childSizeRow, childSizeColumn)

		if childSize[0] < 1 | childSize[1] < 1 :
			raise ValueError

		if childSize[0] < max_size[0] | childSize[1] < max_size[1] :
			raise ValueError

		return childSize

	def takeMotherElementToChild (self, currentChildRow, currentChildColumn, currentRow, currentColumn):
		pass



	def matrix_collapse(self, splitted_matrix: dict) -> list:
		"""
		Build the splitted matrix together
		"""
		motherMatrix: list

		#calculate the dimension of the future new mother matrix
		lastTuple = splitted_matrix.keys()[-1]
		splittedMatrixRowCount, splittedMatrixColumnCount = lastTuple
		
		for currentSplit in range (0,len(splitted_matrix)):
			
			matrixString = splitted_matrix.values[currentSplit]
			for currentCharacterCounter in range (0, len(matrixString - 1)):
				currentCharacter = matrixString [currentCharacterCounter]
				if (currentCharacter != ",") & (currentCharacter != ";"): 
					motherMatrix[motherRow][motherColumn] = int(currentCharacter)

		return motherMatrix





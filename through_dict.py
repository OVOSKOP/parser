def updateDict(dictTo, dictFrom):
	for item in dictFrom:
		if item in dictTo:
			dictTo[item].update(dictFrom[item])
		else:
			dictTo.update({item: dictFrom[item]})

	return dictTo

# dict1 = {
# 	'body' : {
# 		'display': 'block',
# 		'margin': '8px'
# 	},
# 	'div': {
# 		'display': 'block'
# 	}
# }

# dict2 = {
# 	'div': {
# 		'display': 'inline-block',
# 		'color': 'white'
# 	},
# 	'a': {
# 		'color': 'white'
# 	}
# }

# dict1 = updateDict(dict1, dict2)
# print(dict1)

def process(menu, clarifai_descpt, tod):
	total = 0
	for key, value in clarifai_descpt.items():
		key_match = {}
		for i, val in enumerate(value):
			for k, v in menu.items():
				for mg in v.menuGroup:
					key_match[v.name] = inner_array = [0]*10
					if tod in mg:
						if val in v.description or val in key:
							key_match[v.name][i] = 1
		sorted_key_match = sorted(key_match.items(), key=lambda y: y.count(1), reverse=True)
		# print menu[sorted_key_match[4][0]].name,menu[sorted_key_match[4][0]].price,menu[sorted_key_match[4][0]].description
		total += float(menu[sorted_key_match[4][0]].price.split("$")[-1])
	return total
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
		print(key_match)			
		sorted_key_match = sorted(key_match.items(), key=lambda y: y.count(1), reverse=True)
		total += float(menu[sorted_key_match[0][0]].price.split("$")[1])
	return total
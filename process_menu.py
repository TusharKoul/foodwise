def process(menu, clarifai_descpt, tod):
	price_dist = {}
	total = 0
	for key, value in clarifai_descpt.items():
		print '1'
		key_match = {}
		for i, val in enumerate(value):
			for k, v in menu.items():
				for mg in v.menuGroup:
					print '2'
					key_match[v.name] = inner_array = [0]*10
					if tod in mg:
						if val in v.description or val in key:
							key_match[v.name][i] = 1
					else:
						if val in v.description or val in key:
							key_match[v.name][i] = 1
		sorted_key_match = sorted(key_match.items(), key=lambda y: y.count(1), reverse=True)
		j = 0
		print '3'
		while not menu[sorted_key_match[j][0]].price:
			j += 1
		total += float(menu[sorted_key_match[j][0]].price.split("$")[-1])
		price_dist[menu[sorted_key_match[j][0]].key] = menu[sorted_key_match[j][0]].price
		print '4'
	return total, price_dist
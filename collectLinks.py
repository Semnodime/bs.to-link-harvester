#!/usr/bin/env python3

import urllib.request
import re
import sys

encoding = 'utf-8'
domain = 'https://bs.to/'
series_path = 'serie/'
series_name = sys.argv[1]
listfile_name = "downloadlist_" + series_name
debug = True

def get(url):
	try:
		return urllib.request.urlopen(url).read().decode(encoding)
	except:
		print('---Network ERROR---')
		print('HTTP Request of', url, 'failed')

def main():
	try:
		listfile = open(listfile_name, 'a')
		series_url = domain + series_path + series_name
		print(series_name, '(', series_url, ')')
		print('│')
		print('├──', '[Collecting Seasons]')
		r = get(series_url)
		seasons_iter = re.finditer(r'<a href="(?P<season_path>' + series_path + series_name + r'/(?P<season_num>\d+))">', r, re.S)

		for season_match in seasons_iter:
			season_url = domain + season_match.group('season_path')
			season_num = season_match.group('season_num')
			print('├──', 'Season', season_num, '(',season_url,')')


			print('│  ', '│  ')
			print('│  ', '├──', '[Collecting Episodes]')
			r = get(season_url)
			episodes_iter = re.finditer(r'<tr>[^<]*<td>[^<]*<a href="(?P<episode_path>.*?)"[^>]*>(?P<episode_num>\d*)</a>.*?<td class="nowrap">(?P<episode_dl_links>.*?)</td>[^<]*</tr>', r, re.S)
			
			for episode_match in episodes_iter:
				episode_num = episode_match.group('episode_num')
				episode_url = domain + episode_match.group('episode_path')
				episode_dl_links = episode_match.group('episode_dl_links')
				print('│  ', '├──', 'Episode', episode_num, '(',episode_url,')')
				

				print('│  ', '│  ', '│  ')
				print('│  ', '│  ', '├──', '[Collecting Download Links]')
				dl_links_iter = re.finditer(r'title="(?P<dl_link_hoster>[^<]*?)".*?href="(?P<dl_link_path>.*?)"', episode_dl_links, re.S)

				first_dl_link = ''
				for dl_link_match in dl_links_iter:
					dl_link_hoster = dl_link_match.group('dl_link_hoster')	
					dl_link_url = domain + dl_link_match.group('dl_link_path')	
					print('│  ', '│  ', '├──', dl_link_hoster, '\t(', dl_link_url,')')	

					r = get(dl_link_url)
					outlink_match = re.search(r'https?://bs.to/out/\d*', r)
					if outlink_match:
						outlink_url = outlink_match.group()
						print('│  ', '│  ', '│  ', '>>>', outlink_url)
					else:
						print('│  ', '│  ', '│  ', '>>>', 'Error transforming Link')
					if outlink_url and not first_dl_link:
						first_dl_link = dl_link_url + ' >>>> ' +  outlink_url + ' >{out}> ' + outlink_url 
						
				listfile.write(first_dl_link + '\n') 
		listfile.close()

	except Exception as e:
		print("An exception occured. Quiting...")
		if debug:
			print('---DEBUGGING INFO---')
			print(e)


main()
print('---Logfile--->>>', listfile_name, "<<<---")

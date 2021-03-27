import scrapy
import sys
sys.path.append('../')
import items

class BiatSpider(scrapy.Spider):
	name = 'biat'
	download_delay = 0.5
	randomize_download_delay = True
	def start_requests(self):
		zero_giver = lambda s: '0'*(len(s)==1)+s
		url_etap_template = 'http://biathlonresults.com/modules/sportapi/api/Competitions?RT=385698&EventId=BT2021SWRLCP{}'
		
		for i in range(11):
			url_etep = url_etap_template.format(zero_giver(str(i)))
			yield scrapy.Request(url = url_etep,
									callback = self.parse_etap)
	def parse_etap(self, response):
		descriptions = response.xpath('//Competition/ShortDescription/text()').getall()
		locations = response.xpath('//Competition/Location/text()').getall()
		RaceIds = response.xpath('//Competition/RaceId/text()').getall()
		start_times = response.xpath('//Competition/StartTime/text()').getall()
		url_competition_results = 'http://biathlonresults.com/modules/sportapi/api/Results?RT=385698&RaceId={}'

		for desc,loc,time, RaceId in zip(descriptions,locations,start_times, RaceIds):
			yield scrapy.Request(url = url_competition_results.format(RaceId),
									callback = self.parse_competition,
									cb_kwargs = {'description':desc,
												 'location':loc,
												 'start_time':time})

	def parse_competition(self,response,description,location,start_time):
		names = response.xpath('//ResultRow/Name/text()').getall()
		start_orders = response.xpath('//ResultRow/StartOrder/text()').getall()
		result_orders = response.xpath('//ResultRow/ResultOrder/text()').getall()
		nats = response.xpath('//ResultRow/Nat/text()').getall()
		shootings = response.xpath('//ResultRow/Shootings/text()').getall()
		totals = response.xpath('//ResultRow/ShootingTotal/text()').getall()
		total_times = response.xpath('//ResultRow/TotalTime/text()').getall()

		for name,start_order,result_order,nat,shooting,total,total_time in zip(names,start_orders,
																		result_orders,nats,
																		shootings,totals,total_times):
			yield {'description': description,
					'location':location,
					'start_time':start_time,
					'name':name,
					'start_order':start_order,
					'result_order':result_order,
					'nat':nat,
					'shooting':shooting,
					'total':total,
					'total_time':total_time}



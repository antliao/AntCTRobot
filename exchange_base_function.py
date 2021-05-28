import time
import ccxt

class CryptoExchange:
	def __init__(self, exchange_id: str, apiK: str, secK: str):  
		self.exchange_id = exchange_id
		exchange_class = getattr(ccxt, exchange_id)
		exchange = exchange_class({
			'apiKey': apiK,
			'secret': secK,
		})
		self.exchange = exchange  
		self.exchange.load_markets()  

# Robot to check the trend(CT -> Check Trend)
class AntCTRobot():
	def __init__(self, exchange: CryptoExchange, notice): 
		self.exchange = exchange
		self.notice = notice

	def set_rule(self, symbol: str, timeframe: int, diff: float):
		self.rule_symbol = symbol
		self.rule_timeframe = timeframe  # seconds
		self.rule_diff  = diff # the diff of begin and end every timeframe
		print("rule symbol: " + self.rule_symbol)
		print("rule timeframe: " + str(self.rule_timeframe))
		print("rule diff: " + str(self.rule_diff))

	def action(self):

		# make the standard output clear
		print("\n\n")
		print("-----------------------------------------------")

		content = ''
		h_price = float(self.__head_price)
		t_price = float(self.__tail_price)

		content = content + self.__head_price + " ===> " + self.__tail_price + "\n\n"
		content = content + self.__head_time + " ===> " + self.__tail_time + "\n\n"

		sbj = ''
		if(h_price >= t_price):
			result = h_price - t_price
			if(result >= self.rule_diff):
				sbj = self.rule_symbol + " was down " + str(result)
				content = sbj + "\n\ndiff: " + str(result) + "\n\n" + content
				self.notice.send(sbj, content)
		else:
			result = t_price - h_price
			if(result >= self.rule_diff):
				sbj = self.rule_symbol + " was up " + str(result)
				content = sbj + "\n\ndiff: " + str(result) + "\n\n" + content
				self.notice.send(sbj, content)

		print(content)

	def get_localtime(self):
		localtime = time.localtime()
		result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
		return result

	def run(self):
		start = 0
		self.__head_price = 0
		self.__tail_price = 0
		while 1:
			data = self.exchange.exchange.fetch_tickers()
			if(start == 0):
				self.__head_price = data[self.rule_symbol]['info']['price']
				self.__head_time = self.get_localtime()
				start = 1
			elif(start == 1):
				self.__tail_price = data[self.rule_symbol]['info']['price']
				self.__tail_time = self.get_localtime()

				self.action()

				self.__head_price = data[self.rule_symbol]['info']['price']
				self.__head_time = self.get_localtime()

			time.sleep(self.rule_timeframe)

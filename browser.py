from selenium import webdriver # ブラウザ
# ブラウザを表示しないために使用
from selenium.webdriver.chrome.options import Options as C_Options
from selenium.webdriver.firefox.options import Options as F_Options

browswer = webdriver

def headlessSetup(browserPath:str, headless:bool=True, visible:bool=False, sandbox:bool=True):
	global browser

	# ヘッドレスブラウザの起動処理
	print("[browser.py headlessSetup]headlessSetup...")
	try: # 起動できれば続行　できなければ終了処理
		if 'chromedriver' in browserPath:
			# ヘッドレスブラウザのオプション設定
			options = C_Options()
			if headless:
				options.add_argument('--headless') # ヘッドレス動作（必須）
			if not visible:
				options.add_argument('--disable-gpu') # 非表示
			if sandbox:
				options.add_argument('--no-sandbox')
			browser = webdriver.Chrome(browserPath, chrome_options=options)
		elif 'geckodriver' in browserPath:
			# ヘッドレスブラウザのオプション設定
			options = F_Options()
			options.add_argument('-headless')
			
	except Exception as e:
		print("[browser.py headlessSetup]Error")
		print(e)
		print("[browser.py headlessSetup]==========")
		return False
	else:
		print("[browser.py headlessSetup]Done")
		return True

def browserQuit():
	print("[browser.py browserQuit]headlessQuit...")
	try:
		browser.close()
		browser.quit()
		print("[browser.py browserQuit]Done")
	except Exception as e:
		print("[browser.py browserQuit]Error")
		print(e)

def getXPathArray(target:str,err:bool=True):
	try:
		return browser.find_elements_by_xpath(target)
	except Exception as e:
		if err:
			print(f'[browser.py getPathArray]Error return \'\'')
			print(e)
		return ''

def getXPath(target:str,err:bool=True):
	"""XPath"""
	try:
		return browser.find_element_by_xpath(target)
	except Exception as e:
		if err:
			print(e)
		return None

def getXPathAttribute(target:str,attribute:str,err:bool=True):
	try:
		return browser.find_element_by_xpath(target).get_attribute(attribute)
	except Exception as e:
		if err:
			print(f'[browser.py getXPathAttribute]Error return None')
			print(e)
		return None

def clickXPath(target,err:bool=True)->bool:
	"""XPathで指定したパスをクリック"""
	try:
		browser.find_element_by_xpath(target).click()
	except Exception as e:
		if err:
			print(e)
		return False
	return True

def getXPathText(target:str,err:bool=True)->str:
	try:
		return browser.find_element_by_xpath(target).text
	except Exception as e:
		if err:
			print(f'[browser.py getXPathText]Error return \'\'')
			print(e)
		return ''

def back():
	browser.back()

def jumpURL(target:str,err:bool=True)->bool:
	"""URL"""
	global browser
	#print(f'[browser.py jumpURL]URL:{target}')
	try:
		browser.get(target)
		return True
	except Exception as e:
		if err:
			print(f'[browser.py jumpURL]Error return False')
			print(e)
		return False


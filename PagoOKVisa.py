import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select

print "Iniciando Webdriver"

try:
	driver = webdriver.Chrome('/home/juan/Automation/chromedriver')
except Exception, e:
	print e
	sys.exit
	

driver.get('http://localhost:19001/forms/test/TestCompra-Dist.html')
site = '28464383'
random_op = 'visa ' + str(int(time.time()))
mail = 'morton@redb.ee'
titular = 'Santiago Figueroa'
card = '4509790112684851'
doc = '33333333'
street = 'Evergreen Terrace'
door = '742'
birthdate = '03101986'


nrocomercio = driver.find_element_by_name('NROCOMERCIO')
nrocomercio.send_keys(site)
nrooperacion = driver.find_element_by_name('NROOPERACION')
nrooperacion.send_keys(random_op)
emailcliente = driver.find_element_by_name('EMAILCLIENTE')
emailcliente.send_keys(mail)
time.sleep(2)
nrocomercio.submit()
time.sleep(2)
nombreentarjeta = driver.find_element_by_name('NOMBREENTARJETA')
nombreentarjeta.send_keys(titular)
nrotarjeta = driver.find_element_by_name('NROTARJETA')
nrotarjeta.send_keys(card)
nrodoc = driver.find_element_by_name('NRODOC')
nrodoc.send_keys(doc)
combomes = Select(driver.find_element_by_id('idComboMes'))
combomes.select_by_value('01');
comboano = Select(driver.find_element_by_id('idComboAno'))
comboano.select_by_value('30');
calle = driver.find_element_by_name('CALLE')
calle.send_keys(street)
nropuerta = driver.find_element_by_name('NROPUERTA')
nropuerta.send_keys(door)
fechanacimiento = driver.find_element_by_name('FECHANACIMIENTO')
fechanacimiento.send_keys(birthdate)
fechanacimiento.submit()
time.sleep(30)

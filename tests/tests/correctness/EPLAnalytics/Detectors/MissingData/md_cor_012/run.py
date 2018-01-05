# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(Xclock=True)
		self.injectAnalytic(correlator)
		self.injectMissingData(correlator)
		self.ready(correlator)
		correlator.receive(filename='OutputIndividual.evt', channels=['OutputIndividual'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic MissingData started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('OutputIndividual.evt', expr='com.industry.analytics\.Data', condition='==3', timeout=5)

		
	def validate(self):
		self.assertDiff('OutputIndividual.evt', 'OutputIndividual.evt')
		self.assertDiff('correlator.out', 'correlator.log',
						includes=['MissingDataService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	

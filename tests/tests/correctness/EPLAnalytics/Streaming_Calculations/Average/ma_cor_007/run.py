# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectAverage(correlator)
		self.ready(correlator)
		correlator.receive(filename='MovingAverages.evt', channels=['Output1'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Average started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('MovingAverages.evt', expr='com.industry.analytics\.Data', condition='==14', timeout=5)

		
	def validate(self):
		self.assertDiff('MovingAverages.evt', 'MovingAverages.evt')
		self.checkSanity()	

import re


class SensitivityPredictorBase:
	def is_sensitive(self, query: str) -> bool:
		# Zip Code-like
		if re.search("\\d{5}", query) is not None:
			return True
		return False


SensitivityPredictor: SensitivityPredictorBase

try:
	import tensorflow as tf
	class RNNPredictor(SensitivityPredictorBase):
		def is_sensitive(self, query: str) -> bool:
			if super().is_sensitive(query):
				return True
			
			return False
	
	SensitivityPredictor = RNNPredictor()
except ImportError:
	# Fallback to fake predictor
	print("TensorFlow not installed -- Falling back to placebo predictor")
	SensitivityPredictor = SensitivityPredictorBase()
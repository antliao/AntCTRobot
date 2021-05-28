import abc
from playsound import playsound

class Notice(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def send(self, subject, message):
		return NotImplemented

class alarm_sound(Notice):
	def send(self, subject, message):
		playsound("piano.wav")

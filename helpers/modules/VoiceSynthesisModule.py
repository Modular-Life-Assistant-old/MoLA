from helpers.modules.NotificationModule import NotificationModule


class VoiceSynthesisModule(NotificationModule):
    voice_quality = 0

    def send(self, msg):
        """ Send message."""
        self.textToSpeak(msg)

    def textToSpeak(self, msg):
        """ transform test to sound."""
        raise NotImplementedError()

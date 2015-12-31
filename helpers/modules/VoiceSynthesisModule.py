from helpers.modules.BaseModule import BaseModule


class VoiceSynthesisModule(BaseModule):
    voice_quality = 0

    def notification_event(self, event):
        """Receive notification."""
        msg = event.kwargs.get('msg', None)

        if msg:
            self.textToSpeak(msg)

    def textToSpeak(self, msg):
        """ transform test to sound."""
        raise NotImplementedError()

from pybricks import ev3brick as brick
from pybricks.parameters import SoundFile
from pybricks.tools import print, wait

game_over_sounds = [
    SoundFile.GAME_OVER,
    SoundFile.CRYING,
    SoundFile.OUCH,
    SoundFile.KUNG_FU,
    SoundFile.FANFARE]

ball_hit_sound = SoundFile.SONAR


class AudioManager:
    def play_sound(self, sound):
        print("playing " + sound)
        brick.sound.file(sound)
        wait(300)
        #self.play_sound(game_over_sounds[0])
        #self.play_sound(ball_hit_sound)
        # Audio must be mono. 8bit unsigned and 16bit signed confirmed to play
        ##brick.sound.file('Audio/dundundunnn_16bit.wav')

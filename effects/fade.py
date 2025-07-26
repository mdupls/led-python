from effect import BaseEffect

class FadeEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None, fade_in=True):
        super().__init__()
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()
        self.brightness = 0 if fade_in else 255
        self.fade_direction = 1 if fade_in else -1 # 1 for fade in, -1 for fade out
        self.step = 5
        
    def update(self):
        # Scale base color by current brightness
        scaled = self._scale_color(self.color, self.brightness)
        for i in range(self.num_pixels):
            self.pixels[i] = scaled

        # Update brightness
        self.brightness += self.step * self.fade_direction

        if self.brightness >= 255:
            self.brightness = 255
            self.fade_direction = -1  # start fading out
        elif self.brightness <= 0:
            self.brightness = 0
            self.fade_direction = 1   # start fading in
            self._change_color()

    def _change_color(self):
        if self.color_fn is not None:
            self.color = self.color_fn()

    def _scale_color(self, color, brightness):
        # brightness: 0–255
        r = (color[0] * brightness) // 255
        g = (color[1] * brightness) // 255
        b = (color[2] * brightness) // 255
        return (r, g, b, 0)
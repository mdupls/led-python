from effect import BaseEffect

class FadeEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None, step=5):
        super().__init__()
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()
        self.brightness = 0
        self.step = step
        self.direction = 1  # 1 for fade in, -1 for fade out

    def scale_color(self, color, brightness):
        # brightness: 0–255
        r = (color[0] * brightness) // 255
        g = (color[1] * brightness) // 255
        b = (color[2] * brightness) // 255
        return (r, g, b, 0)

    def update(self):
        # Scale base color by current brightness
        scaled = self.scale_color(self.color, self.brightness)
        for i in range(self.num_pixels):
            self.strip[i] = scaled

        # Update brightness
        self.brightness += self.step * self.direction

        if self.brightness >= 255:
            self.brightness = 255
            self.direction = -1  # start fading out
        elif self.brightness <= 0:
            self.brightness = 0
            self.direction = 1   # start fading in
            if self.color_fn is not None:
                self.color = self.color_fn()
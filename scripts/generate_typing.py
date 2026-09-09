"""Generate a typing-animation GIF with gradient text for GitHub README."""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math


def hex_to_rgb(h):
    return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def make_gradient_bg(w, h, c1, c2, angle=135):
    """Create a full-frame gradient image."""
    rad = math.radians(angle)
    img = Image.new("RGB", (w, h))
    px = img.load()
    denom = w * abs(math.cos(rad)) + h * abs(math.sin(rad)) or 1
    for y in range(h):
        for x in range(w):
            t = (x * math.cos(rad) + y * math.sin(rad)) / denom
            t = max(0, min(1, t))
            px[x, y] = lerp(c1, c2, t)
    return img


def main():
    W, H = 900, 70
    C1 = hex_to_rgb("#F0FF00")
    C2 = hex_to_rgb("#58CFFB")
    BG = (13, 17, 23)  # GitHub dark

    en = "Exploring more possibilities in the AI era."
    cn = "「探索AI时代的更多可能」"

    font_en = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
    font_cn = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)

    # Measure text
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    en_box = tmp.textbbox((0, 0), en, font=font_en)
    cn_box = tmp.textbbox((0, 0), cn, font=font_cn)
    en_w, en_h = en_box[2] - en_box[0], en_box[3] - en_box[1]
    cn_w, cn_h = cn_box[2] - cn_box[0], cn_box[3] - cn_box[1]

    # Phase helpers
    def phase(t):
        """Return (text, font, w, h, full_len, progress) for frame at time t in [0,1]."""
        if t < 0.05:
            return en, font_en, en_w, en_h, len(en), 0.01
        elif t < 0.45:
            return en, font_en, en_w, en_h, len(en), (t - 0.05) / 0.4
        elif t < 0.50:
            return en, font_en, en_w, en_h, len(en), 1.0
        elif t < 0.88:
            return cn, font_cn, cn_w, cn_h, len(cn), (t - 0.50) / 0.38
        else:
            return cn, font_cn, cn_w, cn_h, len(cn), 1.0

    frames = []
    fps = 20
    total_frames = 120  # 6 seconds
    grad_bg = make_gradient_bg(W, H, C1, C2)

    for i in range(total_frames):
        t = i / total_frames
        text, font, tw, th, full, prog = phase(t)
        nchars = max(0, min(full, int(prog * full + 0.5)))

        # Base frame
        frame = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(frame)

        # Render displayed text as a mask
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        x = (W - tw) // 2
        y = (H - th) // 2
        displayed = text[:nchars]
        md.text((x, y), displayed, font=font, fill=255)

        # Apply gradient via mask
        f_arr = np.array(frame)
        g_arr = np.array(grad_bg)
        m_arr = np.array(mask)
        for c in range(3):
            f_arr[:, :, c] = np.where(m_arr > 0, g_arr[:, :, c], f_arr[:, :, c])

        frame = Image.fromarray(f_arr)
        draw = ImageDraw.Draw(frame)

        # Blinking cursor
        cursor_active = (i // 6) % 2 == 0  # blink every ~0.3s
        if cursor_active:
            cx = x + int(tw * prog) if prog <= 1 else x + tw
            draw.rectangle([cx, y, cx + 3, y + th], fill=C2)

        frames.append(frame)

    out = "typing-animation.gif"
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=1000//fps, loop=0)
    print(f"Generated: {out} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
